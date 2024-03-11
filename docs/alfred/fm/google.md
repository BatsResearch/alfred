# Google

[Alfred Index](../../README.md#alfred-index) / [Alfred](../index.md#alfred) / [Fm](./index.md#fm) / Google

> Auto-generated documentation for [alfred.fm.google](../../../alfred/fm/google.py) module.

- [Google](#google)
  - [GoogleModel](#googlemodel)
    - [GoogleModel()._encode_batch](#googlemodel()_encode_batch)
    - [GoogleModel()._generate_batch](#googlemodel()_generate_batch)
    - [GoogleModel()._google_genai_embedding_query](#googlemodel()_google_genai_embedding_query)
    - [GoogleModel()._google_genai_query](#googlemodel()_google_genai_query)
    - [GoogleModel()._score_batch](#googlemodel()_score_batch)
    - [GoogleModel().chat](#googlemodel()chat)

## GoogleModel

[Show source in google.py:33](../../../alfred/fm/google.py#L33)

A wrapper for the Google API.

This class provides a wrapper for the Google API for generating completions.

#### Signature

```python
class GoogleModel(APIAccessFoundationModel):
    def __init__(
        self, model_string: str = "gemini-pro", api_key: Optional[str] = None
    ): ...
```

### GoogleModel()._encode_batch

[Show source in google.py:214](../../../alfred/fm/google.py#L214)

Generate embeddings for a batch of prompts using the Google API.

This function generates embeddings for a batch of prompts using the Google API.
The generated embeddings are returned in a list of `torch.Tensor` objects.

#### Arguments

- `batch_instance` - A list of prompts
:type batch_instance: List[str]
- `kwargs` - Additional keyword arguments to pass to the Google API.
:type kwargs: Any

#### Returns

A list of `torch.Tensor` objects containing the generated embeddings.
Type: *List[torch.Tensor]*

#### Signature

```python
def _encode_batch(self, batch_instance: [List[str]], **kwargs) -> List[torch.Tensor]: ...
```

### GoogleModel()._generate_batch

[Show source in google.py:159](../../../alfred/fm/google.py#L159)

Generate completions for a batch of prompts using the Google API.

This function generates completions for a batch of prompts using the Google API.
The generated completions are returned in a list of `CompletionResponse` objects.

#### Arguments

- `batch_instance` - A list of prompts for which to generate completions.
:type batch_instance: List[str] or List[Tuple]
- `kwargs` - Additional keyword arguments to pass to the Google API.
:type kwargs: Any

#### Returns

A list of `CompletionResponse` objects containing the generated completions.
Type: *List[CompletionResponse]*

#### Signature

```python
def _generate_batch(
    self, batch_instance: Union[List[str], Tuple], **kwargs
) -> List[CompletionResponse]: ...
```

### GoogleModel()._google_genai_embedding_query

[Show source in google.py:84](../../../alfred/fm/google.py#L84)

Run a single query to get the embedding through the foundation model

#### Arguments

- `query_string` - The prompt to be used for the query
:type query_string: str

#### Returns

The embeddings
Type: *str*

#### Signature

```python
@retry(num_retries=3, wait_time=0.1, exceptions=Exception)
def _google_genai_embedding_query(
    self, query_string: str, **kwargs: Any
) -> torch.Tensor: ...
```

### GoogleModel()._google_genai_query

[Show source in google.py:40](../../../alfred/fm/google.py#L40)

Run a single query through the foundation model

#### Arguments

- `query` - The prompt to be used for the query
:type query: Union[str, List]
- `temperature` - The temperature of the model
:type temperature: float
- `max_tokens` - The maximum number of tokens to be returned
:type max_tokens: int
- `kwargs` - Additional keyword arguments
:type kwargs: Any

#### Returns

The generated completion
Type: *str*

#### Signature

```python
@retry(num_retries=3, wait_time=0.1, exceptions=Exception)
def _google_genai_query(
    self,
    query: Union[str, List, Tuple],
    temperature: float = 0.0,
    max_tokens: int = 64,
    **kwargs: Any
) -> str: ...
```

### GoogleModel()._score_batch

[Show source in google.py:184](../../../alfred/fm/google.py#L184)

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

### GoogleModel().chat

[Show source in google.py:246](../../../alfred/fm/google.py#L246)

Launch an interactive chat session with the Google API.

#### Signature

```python
def chat(self, **kwargs: Any): ...
```