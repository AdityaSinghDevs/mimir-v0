import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from typing import Any

def load_model_and_tokenizer(model_name : str, torch_dtype : str,
                             device_map: str)-> Any:
    
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype = torch_dtype,
        device_map = device_map
    )

    tokenizer = AutoTokenizer.from_pretrained(model_name)

    return [model, tokenizer]

