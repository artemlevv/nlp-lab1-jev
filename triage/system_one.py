"""System I. Jev answers typed questions about a ticket."""

from dataclasses import dataclass

from typesafe_sdk import Choice, Noul, Score, TypeSafeClient

DEPARTMENTS = {
    "billing": "Payments, refunds, invoices, subscription charges",
    "technical": "Bugs, errors, integrations, app not working",
    "account": "Login, password, profile, account deletion",
    "sales": "Pricing questions, plans, demos, partnerships",
}

URGENCY_LEVELS = [
    "Can wait: general question, no impact",
    "Soon: something is inconvenient but works",
    "Now: customer is blocked or losing money",
]

LANGUAGES = {
    "uk": "Ukrainian",
    "en": "English",
    "other": "Any other language",
}

QUESTIONS = {
    "department": Choice(
        instructions="Which team should handle this support ticket?",
        criteria=DEPARTMENTS,
    ),
    "urgency": Score(
        instructions="How urgent is this ticket for the customer?",
        criteria=URGENCY_LEVELS,
    ),
    "language": Choice(
        instructions="In which language is the ticket written?",
        criteria=LANGUAGES,
    ),
    "is_spam": Noul(
        instructions="The message is spam, advertising, or unrelated to our product",
    ),
    "needs_explanation": Noul(
        instructions=(
            "Answering requires a detailed, personalised explanation "
            "rather than a short standard template reply"
        ),
    ),
}


@dataclass
class Triage:
    department: str
    department_confidence: float
    urgency: float
    language: str
    spam_probability: float
    complexity_probability: float

    @property
    def urgency_label(self) -> str:
        return URGENCY_LEVELS[round(self.urgency)].split(":")[0]


def triage(client: TypeSafeClient, ticket: str) -> Triage:
    response = client.system_one({"ticket": ticket}, QUESTIONS)
    department = response.choices["department"]
    return Triage(
        department=department.choice,
        department_confidence=department.confidence,
        urgency=response.scores["urgency"].score,
        language=response.choices["language"].choice,
        spam_probability=response.nouls["is_spam"].noul,
        complexity_probability=response.nouls["needs_explanation"].noul,
    )
