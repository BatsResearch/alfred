import logging
from typing import List, Any

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

    def __init__(
        self, model: str, model_string: str, local_dir: str = None, **kwargs: Any
    ):
        """
        Initialize a VLLM with MultiGPU.

        :param model: (optional) The path to the model.
        :type model: str
        """
        self.model_string = model
        super().__init__(model_string)
        self.gpu_count = torch.cuda.device_count()
        self.model = LLM(
            local_dir if local_dir is not None else model,
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
