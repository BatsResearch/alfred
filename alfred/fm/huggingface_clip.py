import logging
from typing import Optional, List, Tuple

import torch
from PIL import Image
from transformers import AutoProcessor, CLIPModel, ChineseCLIPModel

from alfred.fm.model import LocalAccessFoundationModel
from alfred.fm.response import RankedResponse

logger = logging.getLogger(__name__)


class HuggingFaceCLIPModel(LocalAccessFoundationModel):

    def __init__(self, model_string: str, local_path: Optional[str] = None):
        super().__init__(model_string, local_path)
        self.model = ChineseCLIPModel.from_pretrained(model_string, cache_dir=local_path) \
            if "clip" in model_string else CLIPModel.from_pretrained(model_string, cache_dir=local_path)
        self.processor = AutoProcessor.from_pretrained(model_string, cache_dir=local_path)
        self.tokenizer = None
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.model.eval()

    def _score_batch(
            self,
            batch_instance: Tuple[List[Image], List[str]],
            **kwargs,
    ):
        return_image_features = kwargs.get("return_image_features", False)
        return_raw_logits = kwargs.get("raw_logits", False)

        image, text = batch_instance
        text = self.processor(text, padding=True, truncation=True, return_tensors="pt").to(self.device)
        image = self.processor(image, padding=True, truncation=True, return_tensors="pt").to(self.device)

        image_features = self.model.get_image_features(**image)
        image_features = image_features / image_features.norm(p=2, dim=-1, keepdim=True)

        text_features = self.model.get_text_features(**text)
        text_features = text_features / text_features.norm(p=2, dim=-1, keepdim=True)

        logits_per_image = image_features @ text_features.t()
        logits_per_text = logits_per_image.t()

        logits = logits_per_text if return_raw_logits else logits_per_text.softmax(dim=-1)
        prediction = [text[i] for i in logits.argmax(dim=-1)]

        return [RankedResponse(
            prediction=prediction[i],
            scores={candidate: logits[i][cidx] for cidx, candidate in enumerate(text)},
            embeddings=image_features[i] if return_image_features else None
        )
            for i in range(len(prediction))]
