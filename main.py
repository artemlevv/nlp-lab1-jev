"""Support ticket classification with Jev (System I)."""

import argparse
import json
from pathlib import Path

from dotenv import load_dotenv
from typesafe_sdk import TypeSafeClient

from triage.system_one import triage


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file", default="data/tickets.json", help="JSON list of tickets")
    parser.add_argument("--text", help="process a single ticket instead of the file")
    args = parser.parse_args()

    load_dotenv()
    jev = TypeSafeClient()
    tickets = [args.text] if args.text else json.loads(Path(args.file).read_text(encoding="utf-8"))

    for index, ticket in enumerate(tickets, start=1):
        t = triage(jev, ticket)
        print(f"#{index} {ticket}")
        print(
            f"   System I: department={t.department} ({t.department_confidence:.2f}), "
            f"urgency={t.urgency:.2f} [{t.urgency_label}], language={t.language}, "
            f"spam={t.spam_probability:.2f}, complex={t.complexity_probability:.2f}"
        )
        print()


if __name__ == "__main__":
    main()
