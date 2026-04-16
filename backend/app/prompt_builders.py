from __future__ import annotations

import typing

def build_generation_request_prompt(
    *,
    user_prompt: str,
    keyword: str,
    domain: str,
    brand: str,
    project: typing.Optional[str],
    iteration_number: int,
) -> str:
    """Single edit point for the first GPT/Gemini request in every iteration.

    Change this function if you want to alter what the generation models receive
    for iteration 1, 2, and 3. Right now it intentionally sends only the raw
    Prompt field from the UI.
    """

    _ = (keyword, domain, brand, project, iteration_number)
    return user_prompt.strip()
