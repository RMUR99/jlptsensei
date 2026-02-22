from openai import OpenAI 
from core.prompt_builder import build_system_prompt
from dotenv import load_dotenv
load_dotenv()  # loads .env

import json


client = OpenAI()


def generate_reply(messages, level, strict=False):
    system_prompt = build_system_prompt(level, strict)

    messages = [{"role": "system", "content": system_prompt}] + messages

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        response_format={"type": "json_object"}
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except Exception as e:
        print("JSON error:", e)
        print("Raw output:", content)

        return {
            "reply": content,
            "vocabulary": [],
            "grammar_points": []
        }

