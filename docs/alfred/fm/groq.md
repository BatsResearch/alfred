# Groq

[Alfred Index](../../README.md#alfred-index) / [Alfred](../index.md#alfred) / [Fm](./index.md#fm) / Groq

> Auto-generated documentation for [alfred.fm.groq](../../../alfred/fm/groq.py) module.

- [Groq](#groq)
  - [GroqModel](#groqmodel)
    - [GroqModel()._generate_batch](#groqmodel()_generate_batch)
    - [GroqModel()._groq_query](#groqmodel()_groq_query)
    - [GroqModel()._score_batch](#groqmodel()_score_batch)
    - [GroqModel().chat](#groqmodel()chat)

## GroqModel

[Show source in groq.py:27](../../../alfred/fm/groq.py#L27)

A wrapper for the OpenAI API.

This class provides a wrapper for the OpenAI API for generating completions.

#### Signature

```python
class GroqModel(APIAccessFoundationModel):
    def __init__(
        self, model_string: str = "llama3-8b-8192", api_key: Optional[str] = None
    ): ...
```

### GroqModel()._generate_batch

[Show source in groq.py:100](../../../alfred/fm/groq.py#L100)

Generate completions for a batch of prompts using the Groq API.

This function generates completions for a batch of prompts using the Groq API.
The generated completions are returned in a list of `CompletionResponse` objects.

#### Arguments

- `batch_instance` - A list of prompts for which to generate completions.
:type batch_instance: List[str]
- `kwargs` - Additional keyword arguments to pass to the Groq API.
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

### GroqModel()._groq_query

[Show source in groq.py:34](../../../alfred/fm/groq.py#L34)

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
def _groq_query(
    self,
    query_string: Union[str, List[Dict]],
    temperature: float = 0.0,
    max_tokens: int = 10,
    model: Optional[str] = None,
) -> str: ...
```

### GroqModel()._score_batch

[Show source in groq.py:125](../../../alfred/fm/groq.py#L125)

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

### GroqModel().chat

[Show source in groq.py:157](../../../alfred/fm/groq.py#L157)

Launch an interactive chat session with the Anthropic API.

#### Signature

```python
def chat(self, **kwargs: Any): ...
```