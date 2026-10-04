from google import genai
from google.genai import types
from pydantic import BaseModel, Field
import streamlit as st


class PromptEnhancement(BaseModel):
    improved_prompt: str = Field(description=(
        "Rewrite the raw prompt into a more practical version of itself. Define a role, and a task to the model to which the prompt would be given. If more data or contex is needed write [INCOMPLETE INFORMATION] for that data. Do not make any assumptions or defaults just take the data given from the raw prompt. The prompt must state an explixit amount of word limit. The user's facts should be placed under triple single quotes."
    ))
    changes_made: list[str] = Field(description=(
        "One short item per change. Name the technique applied and why it helps."
    ))
    needed_context: list[str] = Field(description=(
        "Missing details the user should supply, most important first, maximum 5. "
        "Flag any contradictory instructions found in the raw prompt. "
        "If nothing is missing, return an empty list."
    ))


client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])


def enhance(raw_prompt: str, context: str) -> PromptEnhancement:
    contents = f'''Raw prompt to improve:
"""
{raw_prompt}
"""

Context about the task:
"""
{context}
"""'''

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=(
                "You are an expert prompt engineer. Your job is to IMPROVE the user's "
                "raw prompt, not to execute it. Never answer the raw prompt yourself."
            ),
            response_mime_type="application/json",
            response_schema=PromptEnhancement,
        ),
    )
    return response.parsed


if __name__ == "__main__":
    result = enhance(
        raw_prompt="help me write a cold email to get a job",
        context="2nd-year B.Tech student. Want a summer internship at an AI startup. "
                "Built a deployed LLM app. No internship experience yet.",
    )

    print("=== IMPROVED PROMPT ===")
    print(result.improved_prompt)
    print("\n=== CHANGES MADE ===")
    for item in result.changes_made:
        print("-", item)
    print("\n=== NEEDED CONTEXT ===")
    for item in result.needed_context:
        print("-", item)