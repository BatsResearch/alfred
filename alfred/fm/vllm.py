import logging
from typing import List, Any, Union, Optional, Tuple, Dict

from .model import LocalAccessFoundationModel
from .response import CompletionResponse

logger = logging.getLogger(__name__)


import torch

try:
    from vllm import LLM, SamplingParams
except ImportError:
    raise ImportError("Please install VLLM with `pip install vllm`")


class vLLMModel(LocalAccessFoundationModel):
    """
    vLLMModel wraps a vLLM model. vLLM is a fast and easy-to-use library for LLM inference.

    source: https://github.com/vllm-project/vllm
    """

    def __init__(self, model: str, local_path: str = None, **kwargs: Any):
        """
        Initialize a VLLM with MultiGPU.

        :param model: (optional) The path to the model.
        :type model: str
        """
        self.model_string = model
        super().__init__(model)
        self.gpu_count = torch.cuda.device_count()
        self.model = LLM(
            local_path if local_path is not None else model,
            tensor_parallel_size=self.gpu_count,
        )

    def _generate_batch(
        self,
        batch_instance: List[str],
        **kwargs: Any,
    ) -> List[CompletionResponse]:
        """
        Generate completions for a batch of queries.

        :param batch_instance: A list of queries.
        :type batch_instance: List[str]
        :param kwargs: Additional keyword arguments.
        :return: A list of `CompletionResponse` objects with the same prediction content as the input.
        :rtype: List[CompletionResponse]
        """

        temperature = kwargs.get("temperature", 0)
        max_new_tokens = kwargs.get("max_new_tokens", 16)
        top_k = kwargs.get("top_k", -1)

        sampling_params = SamplingParams(
            temperature=temperature, max_tokens=max_new_tokens, top_k=top_k
        )

        return [
            CompletionResponse(prediction=output.outputs[0].text)
            for output in self.model.generate(batch_instance, sampling_params)
        ]

    def _score_batch(
        self,
        batch: Union[List[str], List[Tuple[str, str]]],
        candidate: Optional[List[str]] = None,
        hidden_state: bool = False,
        tokenized: bool = False,
        **kwargs: Any,
    ) -> List[Dict[str, Any]]:
        """
        Score a batch of prompts and candidates using the vLLM model.

        :param batch: A list of prompts or a list of tuples of prompts and candidates.
        :param candidate: A list of candidates to rank. If not provided, it's extracted from batch.
        :param hidden_state: Whether to return the encoder hidden state (not supported in vLLM).
        :param tokenized: Whether the input is already tokenized (not supported in vLLM).
        :return: A list of dictionaries containing the log probability scores for each candidate.
        """

        def _process_logprobs(logprobs):
            return [
                max(token_dict.values(), key=lambda x: x.logprob).logprob
                if token_dict is not None
                else 0
                for token_dict in logprobs
            ]

        if tokenized:
            raise ValueError("vLLM does not support pre-tokenized input.")

        if candidate is None:
            if isinstance(batch[0], tuple):
                prompts, candidates = zip(*batch)
            else:
                raise ValueError(
                    "If batch is a list of strings, candidate must be provided."
                )
        else:
            prompts = batch
            candidates = candidate

        sampling_params = SamplingParams(
            temperature=0.0,
            max_tokens=1,
            prompt_logprobs=0,
        )

        # Generate logprobs for prompts and prompt+candidates
        prompt_outputs = self.model.generate(prompts, sampling_params)
        full_outputs = self.model.generate(
            [f"{p} {c}" for p, c in zip(prompts, candidates)], sampling_params
        )

        results = []
        for prompt_output, full_output, candidate in zip(
            prompt_outputs, full_outputs, candidates
        ):
            prompt_logprobs = _process_logprobs(prompt_output.prompt_logprobs)
            full_logprobs = _process_logprobs(full_output.prompt_logprobs)

            # Calculate log probability of the candidate
            candidate_tokens = self.tokenizer.encode(candidate)
            candidate_logprob = sum(full_logprobs[-len(candidate_tokens) :])

            # Subtract the prompt logprob to get conditional probability
            prompt_logprob = sum(prompt_logprobs[-len(candidate_tokens) :])
            score = candidate_logprob - prompt_logprob

            results.append(
                {
                    "logit": score,
                    "candidate": candidate,
                    "hidden_state": None,  # vLLM doesn't provide hidden states
                }
            )
        return results
