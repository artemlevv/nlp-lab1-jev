"""Decides what to do with a ticket based on Jev's answers."""

from dataclasses import dataclass

from .system_one import Triage, triage

SPAM_THRESHOLD = 0.8
MIN_ROUTING_CONFIDENCE = 0.6
COMPLEXITY_THRESHOLD = 0.5
URGENT_SCORE = 1.5

TEMPLATES = {
    "uk": "Дякуємо за звернення! Ваш запит передано до {department}. Ми відповімо найближчим часом.",
    "en": "Thank you for contacting us! Your request was forwarded to the {department} team. We will reply shortly.",
}

DEPARTMENT_NAMES_UK = {
    "billing": "відділу оплат",
    "technical": "технічної підтримки",
    "account": "служби підтримки акаунтів",
    "sales": "відділу продажів",
}


@dataclass
class Outcome:
    ticket: str
    triage: Triage
    action: str
    reply: str | None = None


def process(ticket: str, jev, writer=None) -> Outcome:
    result = triage(jev, ticket)

    if result.spam_probability > SPAM_THRESHOLD:
        return Outcome(ticket, result, "discard (spam)")

    if result.department_confidence < MIN_ROUTING_CONFIDENCE:
        return Outcome(ticket, result, "human review (low confidence)")

    needs_llm = result.complexity_probability > COMPLEXITY_THRESHOLD or result.urgency >= URGENT_SCORE
    if needs_llm and writer is not None:
        return Outcome(ticket, result, "System II reply", writer.draft_reply(ticket, result))

    if result.language == "uk":
        reply = TEMPLATES["uk"].format(department=DEPARTMENT_NAMES_UK[result.department])
    else:
        reply = TEMPLATES["en"].format(department=result.department)
    return Outcome(ticket, result, "template reply", reply)
