from typing import Any


def chat_builder(model: Any, tokenizer : Any, messages : list)->Any:

    text = tokenizer.apply_chat_template(
        messages,
        tokenize = False,
        add_generation_prompt = True
    )

    inputs  = tokenizer(text, return_tensors="pt").to(model.device)

    return inputs

def generate_response(inputs: Any, model: Any,
                      tokenizer : Any, do_sample: bool,
                       max_tokens, temperature: float,
                       top_p : float)->Any:
    
    outputs  = model.generate(
        **inputs,
        max_new_tokens = max_tokens,
        do_sample = do_sample,
        temperature = temperature,
        top_p = top_p
    )

    generated_ids = outputs[:, inputs.input_ids.shape[-1]:]

    response = tokenizer.decode(generated_ids[0], skip_special_tokens=True)

    return response

