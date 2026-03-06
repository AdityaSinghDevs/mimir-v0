import os
from core.paths import PROMPTS

def load_prompt(prompt_type : str)->str:

    prompt_file = prompt_type + ".txt"
    prompt_path = os.path.join(PROMPTS, prompt_file)

    with open(prompt_path, "r") as f:
        prompt  = [f.read()]

    return prompt

def prompt_builder(prompt_type: str, incident : dict):

    logs_text  = "\n".join(incident["logs"])

    system_prompt = load_prompt(prompt_type=prompt_type)

    user_prompt= f""" 
    Incident ID : {incident["id"]}

    Incident Description :
    {incident["description"]}

    Incident Logs:
    {logs_text}
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    return messages
    



           

    



