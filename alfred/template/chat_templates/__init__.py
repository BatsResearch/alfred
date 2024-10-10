from functools import wraps
from typing import Union, Dict

system_instruction = """You are an AI assistant designed to answer questions based on specific templates. Your task is to:

1. Carefully analyze the context of each question presented to you.
2. Choose the most appropriate answer from the options provided.
3. Ensure your selection accurately reflects the question's context and intent.
4. Avoid assumptions beyond the information given in the question.

Respond only with the selected answer option, without additional explanation."""

chat_templates = {
    "llama": {
        "system": f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>{system_instruction}<|eot_id|>\n",
        "prefix": " <|start_header_id|>user<|end_header_id|> ",
        "suffix": " <|eot_id|>\n\n<|start_header_id|>assistant<|end_header_id|> ",
    },
    "mistral": {
        "system": "",
        "prefix": " <s>[INST] ",
        "suffix": " [/INST] ",
    },
    "gemma": {
        "system": "",
        "prefix": " <start_of_turn>user ",
        "suffix": " <end_of_turn>\n\n<start_of_turn>assistant ",
    },
    "phi": {
        "system": f"<|system|>{system_instruction}<|end|>",
        "prefix": "<|user|> ",
        "suffix": " <|end|>\n\n<|assistant|> ",
    },
    "qwen": {
        "system": f"<|im_start|>{system_instruction}<|im_end|>",
        "prefix": " <|im_start|>user ",
        "suffix": " <|im_end|>\n\n<|im_start|>assistant ",
    },
    "alpaca": {
        "system": f"<|system|>{system_instruction}<|endoftext|>",
        "prefix": " <|user|> ",
        "suffix": " <|endoftext|>\n\n<|assistant|> "
    },
    "default": {
        "system": "",
        "prefix": "",
        "suffix": "",
    }
}