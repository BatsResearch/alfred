# Anthropic

[Alfred Index](../../README.md#alfred-index) / [Alfred](../index.md#alfred) / [Fm](./index.md#fm) / Anthropic

> Auto-generated documentation for [alfred.fm.anthropic](../../../alfred/fm/anthropic.py) module.

- [Anthropic](#anthropic)
  - [AnthropicModel](#anthropicmodel)
    - [AnthropicModel()._anthropic_query](#anthropicmodel()_anthropic_query)
    - [AnthropicModel()._generate_batch](#anthropicmodel()_generate_batch)
    - [AnthropicModel()._score_batch](#anthropicmodel()_score_batch)
    - [AnthropicModel().chat](#anthropicmodel()chat)

## AnthropicModel

[Show source in anthropic.py:45](../../../alfred/fm/anthropic.py#L45)

A wrapper for the anthropic API.

This class provides a wrapper for the anthropic API for generating completions.

#### Signature

```python
class AnthropicModel(APIAccessFoundationModel):
    def __init__(
        self, model_string: str = "claude-3-opus-20240229", api_key: Optional[str] = None
    ): ...
```

### AnthropicModel()._anthropic_query

[Show source in anthropic.py:52](../../../alfred/fm/anthropic.py#L52)

Run a single query through the foundation model

#### Arguments

- `query` - The prompt to be used for the query
:type query: Union[str, List]
- `temperature` - The temperature of the model
:type temperature: float
- `max_tokens` - The maximum number of tokens to be returned
:type max_tokens: int
- `model` - The model to be used
:type model: str
- `kwargs` - Additional keyword arguments
:type kwargs: Any

#### Returns

The generated completion
Type: *str*

#### Signature

```python
def _anthropic_query(
    self,
    query: Union[str, List],
    temperature: float = 0.0,
    max_tokens: int = 32,
    model: str = "claude-3-opus-20240229",
    **kwargs: Any
) -> str: ...
```

### AnthropicModel()._generate_batch

[Show source in anthropic.py:147](../../../alfred/fm/anthropic.py#L147)

Generate completions for a batch of prompts using the anthropic API.

This function generates completions for a batch of prompts using the anthropic API.
The generated completions are returned in a list of `CompletionResponse` objects.

#### Arguments

- `batch_instance` - A list of prompts for which to generate completions.
:type batch_instance: List[str]
- `kwargs` - Additional keyword arguments to pass to the anthropic API.
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

### AnthropicModel()._score_batch

[Show source in anthropic.py:176](../../../alfred/fm/anthropic.py#L176)

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

### AnthropicModel().chat

[Show source in anthropic.py:208](../../../alfred/fm/anthropic.py#L208)

Launch an interactive chat session with the Anthropic API.

#### Signature

```python
def chat(self, **kwargs: Any): ...
```