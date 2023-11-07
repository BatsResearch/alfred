import logging
import re
from typing import Optional, List, Tuple, Any

import torch
from PIL import Image

from .model import LocalAccessFoundationModel
from .response import CompletionResponse

logger = logging.getLogger(__name__)


class HuggingFaceDocumentModel(LocalAccessFoundationModel):
    """
    The HuggingFaceModel class is a wrapper for HuggingFace Document Models
    For now, this class serves as an abstraction for DocumentQA-based prompted labelers.

    Currently supports:
       - Donut        (MIT License)
       - LayoutLM     (MIT License)
       - LayoutLMv2   (CC BY-NC-SA 4.0)
       - LayoutLMv3   (CC BY-NC-SA 4.0)
    """

    def __init__(
        self,
        model_string: str,
        local_path: Optional[str] = None,
        **kwargs: Any,
    ):
        """
        Constructor for HuggingFaceDocumentModel

        :param model_string: model string for the HuggingFace model
        :type model_string: str
        :param local_path: (optional) local path to store the model
        :type local_path: Optional[str]
        """
        super().__init__(model_string, local_path)
        self.multimodal_mode = "autoregressive"
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        model_string_lowered = model_string.lower()

        self.model_type = ""
        if "layoutlm" in model_string_lowered:
            from transformers import pipeline

            self.pipe = pipeline(
                "document-question-answering",
                model=model_string,
            )
            self.model_type = "layoutlm"
        elif "donut" in model_string_lowered:
            from transformers import DonutProcessor, VisionEncoderDecoderModel

            self.processor = DonutProcessor.from_pretrained(
                model_string, cache_dir=local_path
            )
            self.model = VisionEncoderDecoderModel.from_pretrained(
                model_string, cache_dir=local_path
            ).to(self.device)
            self.model_type = "donut"
            self.model.eval()
        else:
            raise NotImplementedError(
                f"Model {model_string} is not currently supported for document processing. Please choose from the following: donut, layoutlm, layoutlmv2, layoutlmv3"
            )

    def _generate_batch(
        self,
        batch_instance: List[Tuple[Image.Image, str]],
        **kwargs,
    ):
        """
        Scores a batch of instances

        :param batch_instance: batch of instances
        :type batch_instance: Tuple[List[Image.Image], List[str]]
        :param kwargs: (optional) additional arguments
        :type kwargs: Dict
        :return: list of CompletionResponse
        :rtype: List[CompletionResponse]
        """
        max_new_tokens = kwargs.get("max_new_tokens", 512)
        if self.model_type == "donut":
            responses = []
            for image, prompt in batch_instance:
                decoder_input_ids = self.processor.tokenizer(
                    f"<s_docvqa><s_question>{prompt}</s_question><s_answer>",
                    add_special_tokens=False,
                    return_tensors="pt",
                ).input_ids

                pixel_values = self.processor(image, return_tensors="pt").pixel_values

                outputs = self.model.generate(
                    pixel_values.to(self.device),
                    decoder_input_ids=decoder_input_ids.to(self.device),
                    max_length=max_new_tokens,
                    pad_token_id=self.processor.tokenizer.pad_token_id,
                    eos_token_id=self.processor.tokenizer.eos_token_id,
                    use_cache=True,
                    bad_words_ids=[[self.processor.tokenizer.unk_token_id]],
                    return_dict_in_generate=True,
                )

                sequence = self.processor.batch_decode(outputs.sequences)[0]
                sequence = sequence.replace(
                    self.processor.tokenizer.eos_token, ""
                ).replace(self.processor.tokenizer.pad_token, "")
                sequence = re.sub(r"<.*?>", "", sequence, count=1).strip()
                response = self.processor.token2json(sequence)["answer"]
                responses.append(CompletionResponse(prediction=response))
            return responses
        elif self.model_type == "layoutlm":
            responses = []
            for image, prompt in batch_instance:
                response = self.pipe(image, prompt)[0]["answer"]
                responses.append(CompletionResponse(prediction=response))
            return responses
