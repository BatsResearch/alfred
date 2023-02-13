import logging
from contextlib import nullcontext
from typing import Optional, List, Union, Tuple, Dict, Any

import torch
from transformers import (
    AutoModelForSeq2SeqLM,
    AutoModelForCausalLM,
    PreTrainedTokenizer,
    AutoModel,
    AutoTokenizer,
)

from .model import LocalAccessFoundationModel
from .response import CompletionResponse

logger = logging.getLogger(__name__)

logger = logging.getLogger(__name__)

dtype_match = {
    "auto": "auto",
    "fp32": torch.float32,
    "fp16": torch.float16,
    "bf16": torch.bfloat16,
    "half": torch.half,
}

HF_MODEL_BANK_PREFIX = {
    'gpt2': (AutoModelForCausalLM, AutoTokenizer),
    'bigscience/bloom': (AutoModelForCausalLM, AutoTokenizer),
    'bigscience/T0': (AutoModelForSeq2SeqLM, AutoTokenizer),
    'google/flan': (AutoModelForSeq2SeqLM, AutoTokenizer),
    'google/t5': (AutoModelForSeq2SeqLM, AutoTokenizer),
    't5': (AutoModelForSeq2SeqLM, AutoTokenizer),
    'microsoft/DialoGPT': (AutoModelForCausalLM, AutoTokenizer),
    'EleutherAI/gpt-': (AutoModelForCausalLM, AutoTokenizer),
}


class HuggingFaceModel(LocalAccessFoundationModel):
    """
    The HuggingFaceModel class is a wrapper for HuggingFace models,
    including both Seq2Seq (Encoder-Decoder, e.g. T5, T0) and Causal
    (Autoregressive, e.g. GPT) Language Models.

    This wrapper supports several options for loading models, including
    specifying the data type, using a local path for the model hub, using
     a device map for parallelization, applying int8 quantization, and
     using custom tokenization.

    The interface includes implementations of the _score_batch method
    for ranking candidates and the _generate_batch method for generating prompts.
    """

    def __init__(
            self,
            model_string: str,
            dtype: str = "auto",
            local_path: Optional[str] = None,
            device_map: Optional[str] = "auto",
            int_8: bool = False,
            tokenizer: Optional[PreTrainedTokenizer] = None,
    ):
        """
        Constructor for the HuggingFaceModel class.


        :param model_string: The HuggingFace model string, formatted the same as in the HuggingFace model hub (e.g. "bigscience/T0pp")
        :type model_string: str
        :param dtype: (optional) The data type to use, options include "fp32", "fp16", "bf16", and "half" (default: "auto")
        :type dtype: str
        :param local_path: (optional) The path to the local model. If not provided, the default HuggingFace cache directory will be used.
        :type local_path: str
        :param device_map: (optional) A device map for parallelization. This wrapper uses the accelerate library for parallelization, and the device map should be provided in the same format as for accelerate.
        :type device_map: str
        :param int_8: (optional) A boolean indicating whether to use .int8() quantization (default: False)
        :type int_8: bool
        :param tokenizer: (optional) A custom tokenizer to use, if desired.
        :type tokenizer: transformers.PreTrainedTokenizer
        """
        super().__init__(model_string, local_path)

        try:
            self.dtype = dtype_match[dtype]
        except KeyError:
            logger.log(logging.WARNING,
                       f"Invalid dtype {dtype}, defaulting to fp32")
            self.dtype = "auto"
        if '/' in self.model_string:
            hf_factory, hf_modelname = self.model_string.split('/')
            model_name = f"{hf_factory}/{hf_modelname}"
        else:
            model_name = model_string

        if torch.cuda.is_available():
            n_gpus = torch.cuda.device_count()
            free_in_GB = sum(
                [int(mem / 1024 ** 3) for mem in torch.cuda.mem_get_info()])

            logger.log(
                logging.WARNING,
                f"Found {n_gpus} GPUs with {free_in_GB}GB free GPU memory")

            [
                logger.log(logging.WARNING,
                           f"GPU {i}: {torch.cuda.get_device_name(i)}")
                for i in range(n_gpus)
            ]
        else:
            n_gpus = 0
            free_in_GB = 0

        auto_model_class = [
            HF_MODEL_BANK_PREFIX[key] for key in HF_MODEL_BANK_PREFIX
            if model_name.startswith(key)
        ]

        auto_model_class = AutoModel if len(
            auto_model_class) == 0 else auto_model_class[0][0]

        self.model = auto_model_class.from_pretrained(
            model_name,
            cache_dir=self.local_path,
            device_map=device_map,
            load_in_8bit=int_8,
            torch_dtype=self.dtype,
            max_memory={i: f'{free_in_GB - 2}GB'
                        for i in range(n_gpus)},
        )

        try:
            self.max_position_embeddings = self.model.config.max_position_embeddings
        except AttributeError:
            self.max_position_embeddings = 512

        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            cache_dir=self.local_path) if tokenizer is None else tokenizer

    def _get_hidden_states(self, inputs, reduction="mean") -> torch.Tensor:
        """
        Get the hidden states of the inputs.
        For encoder-decoder models (e.g.) T5, this returns the encoder hidden states.
        For causal models (e.g. GPT), this returns the hidden states of the last layer.

        :param inputs: The inputs to the model
        :type inputs: transformers.PreTrainedTokenizer
        :param reduction: (optional) The reduction to apply to the hidden states, options include "mean" and "sum" (default: "mean")
        :type reduction: str
        :return: The hidden states
        :rtype: torch.Tensor
        """

        _input_ids = inputs.input_ids
        _attention_mask = inputs.attention_mask

        if self.model.config.is_encoder_decoder:
            output = self.model.encoder(
                input_ids=_input_ids,
                attention_mask=_attention_mask,
            )
            output = output.last_hidden_state.detach().cpu()
        else:
            output = self.model(
                input_ids=_input_ids,
                attention_mask=_attention_mask,
            )
            output = output.hidden_states.detach().cpu()

        if reduction == "mean":
            embedding = (output * _attention_mask.unsqueeze(-1)).mean(dim=-2)
        elif reduction == "sum":
            embedding = (output * _attention_mask.unsqueeze(-1)).sum(dim=-2)
        else:
            embedding = output

        return embedding

    def _score_batch(
            self,
            batch: Union[List[str], List[Tuple[str, str]]],
            candidate: Optional[List[str]] = None,
            hidden_state: bool = False,
            tokenized: bool = False,
            **kwargs: Any,
    ) -> List[Dict[str, Any]]:
        """
        Score a batch of prompts and candidates using the model.

        This function takes a batch of prompts and a list of candidates and uses the model to generate
        logit scores for the candidates. The raw logit scores are then returned in a list of dictionaries.
        If `candidate` is not provided, the function will use the tokenizer's vocabulary as the candidates.
        The final (softmax) normalization is done after this function when the scores for one instance
        are aggregated.
        For one ranked query, this function will be called `len(candidate)` number of times.

        :param batch: A list of prompts or a list of tuples of prompts and candidates.
        :type batch: Union[List[str], List[Tuple[str, str]]]
        :param candidate: A list of candidates to rank. If not provided, the tokenizer's vocabulary is used.
        :type candidate: List[str]
        :param hidden_state: Whether to return the encoder hidden state.
        :type hidden_state: bool
        :return: A list of dictionaries containing the raw logit scores and the encoder/decoder hidden states.
        :rtype: List[Dict[str, Any]]
        """

        if tokenized:
            inputs, candidate_tokens = batch
        else:
            if candidate is None:
                batch, candidate = zip(*batch)
            batch, candidate = list(batch), list(candidate)

            candidate_tokens = self.tokenizer(
                candidate,
                padding=True,
                truncation=True,
                max_length=self.max_position_embeddings,
                return_tensors="pt",
            )

            inputs = self.tokenizer(
                batch,
                return_tensors="pt",
                padding=True,
                add_special_tokens=False,
                truncation=True,
                max_length=self.max_position_embeddings,
            )

        candidate_token_ids = candidate_tokens.input_ids.to(
            list(self.model.hf_device_map.values())[-1])

        logger.log(logging.INFO,
                   f"Ranking {len(batch)} instances")

        if self.model.config.is_encoder_decoder:
            logits = self.model(
                input_ids=inputs.input_ids.cuda(),
                attention_mask=inputs.attention_mask.cuda(),
                labels=candidate_token_ids,
            ).logits
        else:
            position_ids = torch.maximum(
                torch.cumsum(inputs.attention_mask.cuda().to(torch.long),
                             dim=-1) - 1,
                torch.zeros(
                    1,
                    dtype=torch.long,
                ).cuda()[None, None])
            _, prefix_length = inputs.input_ids.shape

            logits = self.model(
                input_ids=inputs.input_ids.cuda(),
                position_ids=position_ids,
                attention_mask=inputs.attention_mask.cuda(),
                labels=candidate_token_ids,
            ).logits[:, prefix_length - 1:-1]

        masked_log_probs = candidate_tokens.attention_mask.to(
            logits.get_device()).unsqueeze(
            -1) * torch.nn.functional.log_softmax(logits, dim=-1)
        seq_token_log_probs = torch.gather(
            masked_log_probs, -1,
            candidate_token_ids.to(logits.get_device()).unsqueeze(-1))
        seq_log_prob = seq_token_log_probs.squeeze(dim=-1).sum(dim=-1)
        seq_log_prob = seq_log_prob.view(len(batch), -1)

        if hidden_state:
            reduction = kwargs.get("reduction", "mean")
            _hidden_state = self._get_hidden_states(inputs,
                                                    reduction=reduction)
            return [{
                'logit': logit,
                'candidate': candidate[logit_id],
                'hidden_state': _hidden_state[logit_id].squeeze(0)
            } for logit_id, logit in enumerate(torch.flatten(seq_log_prob))]

        return [{
            'logit': logit,
            'candidate': candidate[logit_id],
            'hidden_state': None
        } for logit_id, logit in enumerate(torch.flatten(seq_log_prob))]

    def _generate_batch(
            self,
            batch: List[str],
            padding: bool = True,
            hidden_state: bool = False,
            allow_grad: bool = False,
            tokenized: bool = False,
            **kwargs: Any,
    ) -> List[CompletionResponse]:
        """
        Generate completions for a batch of prompts using the model.

        This function takes a batch of prompts and uses the model to generate
        completions for each prompt.
        The generated completions are then returned in a list of `CompletionResponse` objects.
        Currently, only greedy decoding is supported for open completion.

        :param batch: A list of raw text prompts.
        :type batch: List[str]
        :param padding: Whether to pad the batch.
        :type padding: bool
        :param hidden_state: Whether to return the (encoder) hidden state.
        :type hidden_state: bool
        :param allow_grad: Whether to allow gradient calculations during generation.
        :type allow_grad: bool
        :param kwargs: Additional keyword arguments to pass to the model's `generate` method.
        :type kwargs: Any
        :return: A list of `CompletionResponse` objects containing the generated completions.
        :rtype: List[CompletionResponse]
        """
        logger.log(logging.INFO, f"Inferring {len(batch)} instances")

        if tokenized:
            inputs = batch
        else:
            if padding:
                inputs = self.tokenizer(batch,
                                        return_tensors="pt",
                                        padding=True)
            else:
                inputs = [
                    self.tokenizer(inst, return_tensors="pt") for inst in batch
                ]

        temprature = kwargs.get('temperature', 0.0)
        repetition_penalty = kwargs.get('repetition_penalty', None)
        max_new_tokens = kwargs.get('max_new_tokens', 32)

        with nullcontext() if allow_grad else torch.no_grad():
            logger.log(logging.INFO,
                       f"Inferring {len(batch)} instances with huggingface")
            if padding:
                outputs = self.model.generate(
                    inputs.input_ids.to(self.model.device),
                    max_new_tokens=max_new_tokens,
                    temperature=temprature,
                    repetition_penalty=repetition_penalty,
                    return_dict_in_generate=True,
                )
            else:
                outputs = [
                    self.model.generate(
                        input.input_ids.to(self.model.device),
                        max_length=max_new_tokens,
                    ) for input in inputs
                ]

        if padding:
            texts = list(
                self.tokenizer.batch_decode(outputs.sequences,
                                            skip_special_tokens=True))
        else:
            texts = [
                self.tokenizer.batch_decode(output,
                                            skip_special_tokens=True)[0]
                for output in outputs
            ]

        if hidden_state:
            reduction = kwargs.get("reduction", "mean")

            _hidden_state = self._get_hidden_states(inputs,
                                                    reduction=reduction)

            return [
                CompletionResponse(prediction=text,
                                   embedding=_hidden_state[text_id].squeeze(0))
                for text_id, text in enumerate(texts)
            ]

        return [CompletionResponse(prediction=text) for text in texts]

    def _encode_batch(self, batch_instance, **kwargs) -> List[torch.Tensor]:

        reduction = kwargs.get('reduction', 'mean')
        padding = kwargs.get('padding', True)
        tokenized = kwargs.get('tokenized', False)

        inputs = batch_instance if tokenized else self.tokenizer(batch_instance,
                                                                 return_tensors="pt",
                                                                 padding=padding)

        _hidden_state = self._get_hidden_states(inputs, reduction=reduction)

        return list(_hidden_state)
