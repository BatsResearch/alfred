# Openai

[Alfred Index](../../README.md#alfred-index) / [Alfred](../index.md#alfred) / [Fm](./index.md#fm) / Openai

> Auto-generated documentation for [alfred.fm.openai](../../../alfred/fm/openai.py) module.

- [Openai](#openai)
  - [OpenAIModel](#openaimodel)
    - [OpenAIModel()._encode_batch](#openaimodel()_encode_batch)
    - [OpenAIModel()._generate_batch](#openaimodel()_generate_batch)
    - [OpenAIModel()._openai_embedding_query](#openaimodel()_openai_embedding_query)
    - [OpenAIModel()._openai_query](#openaimodel()_openai_query)
    - [OpenAIModel()._score_batch](#openaimodel()_score_batch)
    - [OpenAIModel().chat](#openaimodel()chat)

## OpenAIModel

[Show source in openai.py:66](../../../alfred/fm/openai.py#L66)

A wrapper for the OpenAI API.

This class provides a wrapper for the OpenAI API for generating completions.

#### Signature

```python
class OpenAIModel(APIAccessFoundationModel):
    def __init__(
        self, model_string: str = "text-davinci-002", api_key: Optional[str] = None
    ): ...
```

### OpenAIModel()._encode_batch

[Show source in openai.py:256](../../../alfred/fm/openai.py#L256)

Generate embeddings for a batch of prompts using the OpenAI API.

This function generates embeddings for a batch of prompts using the OpenAI API.
The generated embeddings are returned in a list of `torch.Tensor` objects.

#### Arguments

- `batch_instance` - A list of prompts
:type batch_instance: List[str]
- `kwargs` - Additional keyword arguments to pass to the OpenAI API.
:type kwargs: Any

#### Returns

A list of `torch.Tensor` objects containing the generated embeddings.
Type: *List[torch.Tensor]*

#### Signature

```python
def _encode_batch(self, batch_instance: [List[str]], **kwargs) -> List[torch.Tensor]: ...
```

### OpenAIModel()._generate_batch

[Show source in openai.py:231](../../../alfred/fm/openai.py#L231)

Generate completions for a batch of prompts using the OpenAI API.

This function generates completions for a batch of prompts using the OpenAI API.
The generated completions are returned in a list of `CompletionResponse` objects.

#### Arguments

- `batch_instance` - A list of prompts for which to generate completions.
:type batch_instance: List[str] or List[Tuple]
- `kwargs` - Additional keyword arguments to pass to the OpenAI API.
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

### OpenAIModel()._openai_embedding_query

[Show source in openai.py:150](../../../alfred/fm/openai.py#L150)

Run a single query to get the embedding through the foundation model

#### Arguments

- `query_string` - The prompt to be used for the query
:type query_string: str

#### Returns

The embeddings
Type: *str*

#### Signature

```python
@retry(
    num_retries=3,
    wait_time=0.1,
    exceptions=(
        AuthenticationError,
        APIConnectionError,
        APITimeoutError,
        RateLimitError,
        APIError,
        BadRequestError,
        APIStatusError,
    ),
)
def _openai_embedding_query(self, query_string: str, **kwargs: Any) -> torch.Tensor: ...
```

### OpenAIModel()._openai_query

[Show source in openai.py:73](../../../alfred/fm/openai.py#L73)

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
@retry(
    num_retries=3,
    wait_time=0.1,
    exceptions=(
        AuthenticationError,
        APIConnectionError,
        APITimeoutError,
        RateLimitError,
        APIError,
        BadRequestError,
        APIStatusError,
    ),
)
def _openai_query(
    self,
    query: Union[str, List, Tuple],
    temperature: float = 0.0,
    max_tokens: int = 64,
    **kwargs: Any
) -> str: ...
```

### OpenAIModel()._score_batch

[Show source in openai.py:288](../../../alfred/fm/openai.py#L288)

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

### OpenAIModel().chat

[Show source in openai.py:317](../../../alfred/fm/openai.py#L317)

Launch an interactive chat session with the OpenAI API.

#### Signature

```python
def chat(self, **kwargs: Any): ...
```