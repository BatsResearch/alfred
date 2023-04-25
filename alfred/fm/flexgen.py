import logging
from typing import List, Union, Any

from alfred.fm.model import LocalAccessFoundationModel
from .response import CompletionResponse

logger = logging.getLogger(__name__)

from flexgen.flex_opt import (Policy, OptLM, CompressionConfig)
from transformers import AutoTokenizer


class FlexGenModel(LocalAccessFoundationModel):
    """
    FlexGenModel wraps a FlexGen model. FlexGen is used for High-throughput generative inference with single GPU.

    Currently, FlexGen supports OPT style models.

    source: https://github.com/FMInference/FlexGen
    paper: https://arxiv.org/pdf/2303.06865.pdf
    """

    def __init__(self, model: str, local_dir: str, model_string: str,
                 policy: Union[List, Policy] = (100, 0, 100, 0, 100, 0), offload_dir: str = "./flexgen_offload_cache",
                 **kwargs: Any):
        """
        Initialize a FlexGenModel.

        :param model: (optional) The path to the model.
        :type model: str
        """
        self.model_string = model
        super().__init__(model_string)

        _policy = policy if isinstance(policy, Policy) else Policy(1, 1,
                                                                   policy[0], policy[1], policy[2], policy[3],
                                                                   policy[4], policy[5],
                                                                   overlap=True, sep_layer=True,
                                                                   pin_weight=kwargs.get("cpu_cache_compute", True),
                                                                   cpu_cache_compute=kwargs.get("cpu_cache_compute",
                                                                                                False),
                                                                   attn_sparsity=1.0,
                                                                   compress_weight=kwargs.get("compress_weight", False),
                                                                   comp_weight_config=CompressionConfig(
                                                                       num_bits=4, group_size=64,
                                                                       group_dim=0, symmetric=False),
                                                                   compress_cache=kwargs.get("compress_cache", False),
                                                                   comp_cache_config=CompressionConfig(
                                                                       num_bits=4, group_size=64,
                                                                       group_dim=2, symmetric=False))
        self.model = OptLM(model, offload_dir, local_dir, _policy)
        self.tokenizer = AutoTokenizer.from_pretrained(model, padding_side="left")
        self.tokenizer.add_bos_token = False
        self.stop = self.tokenizer("\n").input_ids[0]

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

        max_length = kwargs.get("max_length", 128)
        temperature = kwargs.get("temperature", 0)
        max_new_tokens = kwargs.get("max_new_tokens", 16)
        do_sample = kwargs.get("do_sample", False)

        output_ids_list = []
        for instance in batch_instance:
            inputs = self.tokenizer(instance, padding="max_length", max_length=max_length)
            output_ids_list.append(
                self.model.generate(
                    inputs.input_ids,
                    do_sample=do_sample,
                    temperature=temperature,
                    max_new_tokens=max_new_tokens,
                    stop=self.stop,
                )
            )
        return [CompletionResponse(prediction=text) for text in
                self.tokenizer.batch_decode(output_ids_list,
                                            skip_special_tokens=True)]
