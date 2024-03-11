# Cohere

[Alfred Index](../../README.md#alfred-index) / [Alfred](../index.md#alfred) / [Fm](./index.md#fm) / Cohere

> Auto-generated documentation for [alfred.fm.cohere](../../../alfred/fm/cohere.py) module.

- [Cohere](#cohere)
  - [CohereModel](#coheremodel)
    - [CohereModel()._cohere_embedding_query](#coheremodel()_cohere_embedding_query)
    - [CohereModel()._cohere_query](#coheremodel()_cohere_query)
    - [CohereModel()._encode_batch](#coheremodel()_encode_batch)
    - [CohereModel()._generate_batch](#coheremodel()_generate_batch)
    - [CohereModel()._score_batch](#coheremodel()_score_batch)

## CohereModel

[Show source in cohere.py:12](../../../alfred/fm/cohere.py#L12)

A wrapper for the OpenAI API.

This class provides a wrapper for the OpenAI API for generating completions.

#### Signature

```python
class CohereModel(APIAccessFoundationModel):
    def __init__(self, model_string: str = "xlarge", api_key: Optional[str] = None): ...
```

### CohereModel()._cohere_embedding_query

[Show source in cohere.py:82](../../../alfred/fm/cohere.py#L82)

Encode a single query to get the embedding through the foundation model

#### Arguments

- `query_string` - The prompt to be used for the query
:type query_string: str

#### Returns

The embeddings
Type: *str*

#### Signature

```python
def _cohere_embedding_query(self, query_string: str) -> torch.Tensor: ...
```

### CohereModel()._cohere_query

[Show source in cohere.py:19](../../../alfred/fm/cohere.py#L19)

Run a single query through the foundation model

#### Arguments

- `query_string` - The prompt to be used for the query
:type query_string: str
- `temperature` - The temperature of the model
:type temperature: float
- `max_tokens` - The maximum number of tokens to be returned
:type max_tokens: int
- `model` - The model to be used
:type model: str

#### Returns

The generated completion
Type: *str*

#### Signature

```python
def _cohere_query(
    self,
    query_string: str,
    temperature: float = 0.0,
    max_tokens: int = 10,
    model: str = "xlarge",
    **kwargs: Any
) -> str: ...
```

### CohereModel()._encode_batch

[Show source in cohere.py:153](../../../alfred/fm/cohere.py#L153)

Generate embeddings for a batch of prompts using the Cohere API.

This function generates embeddings for a batch of prompts using the Cohere API.
The generated embeddings are returned in a list of `torch.Tensor` objects.

#### Arguments

- `batch_instance` - A list of prompts
:type batch_instance: List[str]
- `kwargs` - Additional keyword arguments to pass to the Cohere API.
:type kwargs: Any

#### Returns

A list of `torch.Tensor` objects containing the generated embeddings.
Type: *List[torch.Tensor]*

#### Signature

```python
def _encode_batch(self, batch_instance: [List[str]], **kwargs) -> List[torch.Tensor]: ...
```

### CohereModel()._generate_batch

[Show source in cohere.py:124](../../../alfred/fm/cohere.py#L124)

Generate completions for a batch of prompts using the Cohere API.

This function generates completions for a batch of prompts using the Cohere API.
The generated completions are returned in a list of `CompletionResponse` objects.

#### Arguments

- `batch_instance` - A list of prompts for which to generate completions.
:type batch_instance: List[str]
- `kwargs` - Additional keyword arguments to pass to the Cohere API.
:type kwargs: Any

#### Returns

A list of `CompletionResponse` objects containing the generated completions.
Type: *List[CompletionResponse]*

#### Signature

```python
def _generate_batch(
    self, batch_instance: List[str], **kwargs
) -> List[CompletionResponse]: ...
```

### CohereModel()._score_batch

[Show source in cohere.py:50](../../../alfred/fm/cohere.py#L50)

Tentative solution for scoring candidates.

#### Arguments

- `batch_instance` - A list of prompts for which to generate candidate preferences.
:type batch_instance: List[str] or List[Tuple]
- `scoring_instruction` - The instruction prompt for scoring
:type scoring_instruction: str

#### Signature

```python
def _score_batch(
    self,
    batch_instance: Union[List[Tuple[str, str]], List[str]],
    scoring_instruction: str = "Instruction: Given the query, choose your answer from [[label_space]]:\nQuery:\n",
    **kwargs
) -> List[RankedResponse]: ...
```