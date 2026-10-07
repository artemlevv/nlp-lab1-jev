"""System II. An LLM writes a reply to the ticket."""

import os

from openai import OpenAI

from .system_one import Triage

SYSTEM_PROMPT = (
    "You are a polite customer support agent for a SaaS product. "
    "Write a short, helpful reply to the customer's ticket. "
    "Reply in the same language as the ticket. Do not invent facts about "
    "the customer's account; if information is missing, ask for it."
)


class ReplyWriter:
    def __init__(self) -> None:
        self.client = OpenAI(
            api_key=os.environ["OPENAI_API_KEY"],
            base_url=os.environ.get("OPENAI_BASE_URL") or None,
        )
        self.model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

    def draft_reply(self, ticket: str, triage: Triage) -> str:
        context = (
            f"Department: {triage.department}. "
            f"Urgency: {triage.urgency_label}. "
            f"Language: {triage.language}."
        )
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "system", "content": context},
                {"role": "user", "content": ticket},
            ],
        )
        return completion.choices[0].message.content.strip()
