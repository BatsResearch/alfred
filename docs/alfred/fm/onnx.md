# Onnx

[Alfred Index](../../README.md#alfred-index) /
[Alfred](../index.md#alfred) /
[Fm](./index.md#fm) /
Onnx

> Auto-generated documentation for [alfred.fm.onnx](../../../alfred/fm/onnx.py) module.

- [Onnx](#onnx)
  - [ONNXModel](#onnxmodel)

## ONNXModel

[Show source in onnx.py:12](../../../alfred/fm/onnx.py#L12)

The ONNXMOdel class is a wrapper for ONNX models based on fastT5
https://github.com/Ki6an/fastT5
Currently it only supports T5-based models.

#### Signature

```python
class ONNXModel(LocalAccessFoundationModel):
    def __init__(
        self, model_string: Optional[str] = None, local_path: Optional[str] = None
    ):
        ...
```

#### See also

- [LocalAccessFoundationModel](./model.md#localaccessfoundationmodel)