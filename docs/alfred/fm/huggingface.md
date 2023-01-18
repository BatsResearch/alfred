# Huggingface

[Alfred Index](../../README.md#alfred-index) /
[Alfred](../index.md#alfred) /
[Fm](./index.md#fm) /
Huggingface

> Auto-generated documentation for [alfred.fm.huggingface](../../../alfred/fm/huggingface.py) module.

- [Huggingface](#huggingface)
  - [HuggingFaceModel](#huggingfacemodel)

## HuggingFaceModel

[Show source in huggingface.py:40](../../../alfred/fm/huggingface.py#L40)

The HuggingFaceModel class is a wrapper for HuggingFace models,
including both Seq2Seq (Encoder-Decoder, e.g. T5, T0) and Causal
(Autoregressive, e.g. GPT) Language Models.

This wrapper supports several options for loading models, including
specifying the data type, using a local path for the model hub, using
 a device map for parallelization, applying int8 quantization, and
 using custom tokenization.

The interface includes implementations of the _score_batch method
for ranking candidates and the _generate_batch method for generating prompts.

#### Signature

```python
class HuggingFaceModel(LocalAccessFoundationModel):
    def __init__(
        self,
        model_string: str,
        dtype: str = "auto",
        local_path: Optional[str] = None,
        device_map: Optional[str] = "auto",
        int_8: bool = False,
        tokenizer: Optional[PreTrainedTokenizer] = None,
    ):
        ...
```


