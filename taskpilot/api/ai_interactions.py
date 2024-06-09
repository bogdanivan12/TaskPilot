import openai

from typing import List, Dict, Tuple, Optional

from taskpilot.common import config_info


def get_openai_client() -> openai.OpenAI:
    """Get the OpenAI client"""
    client = openai.OpenAI(api_key=config_info.OPENAI_API_KEY)
    return client


def get_openai_response(prompt: str,
                        system_prompt: Optional[str] = None,
                        chat_history: Optional[List[Dict[str, str]]] = None
                        ) -> Tuple[str, List[Dict[str, str]]]:
    """Get the OpenAI response to a prompt"""
    if chat_history is None:
        chat_history = []
    if system_prompt is not None:
        chat_history.append(
            {
                "role": "system",
                "content": system_prompt
            }
        )
    chat_history.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    client = get_openai_client()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=chat_history
    )
    response_dict = response.dict()
    response_choices = response_dict.get("choices", [])
    response_message = (
        response_choices[0]["message"]["content"]
        if len(response_choices) > 0
        else "Unable to generate response"
    )

    chat_history.append(
        {
            "role": "assistant",
            "content": response_message
        }
    )
    return response_message, chat_history
