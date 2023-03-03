import logging
from typing import Optional, List, Any

from transformers import AutoTokenizer

from alfred.fm.model import LocalAccessFoundationModel
from .response import CompletionResponse

logger = logging.getLogger(__name__)


class ONNXModel(LocalAccessFoundationModel):
    """
     The ONNXMOdel class is a wrapper for ONNX models based on fastT5
     https://github.com/Ki6an/fastT5
     Currently it only supports T5-based models.
    """
    def __init__(self,
                 model_string: Optional[str] = None,
                 local_path: Optional[str] = None):
        """
        Constructor for ONNXModel.
        It wraps the fastT5 library to load ONNX models.

        :param model_string: model string for the HuggingFace model
        :type model_string: str
        :param local_path: (optional) local path to store the model
        :type local_path: Optional[str]
        """
        try:
            from fastt5 import get_onnx_model
        except ImportError:
            raise ImportError("Please install fastt5 to use ONNXModel")
        self.model_string = local_path if local_path else model_string
        super().__init__(model_string, local_path)

        self.model = get_onnx_model(self.model_string)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_string)

    def _generate_batch(
        self,
        batch: List[str],
        **kwargs: Any,
    ):
        tokens = self.tokenizer(batch,
                                return_tensors="pt",
                                padding=True,
                                truncation=True)
        output = self.model.generate(input_ids=tokens.input_ids,
                                     attention_mask=tokens.attention_mask)
        texts = self.tokenizer.decode(output.squeeze(),
                                      skip_special_tokens=True)
        return [CompletionResponse(prediction=text) for text in texts]
