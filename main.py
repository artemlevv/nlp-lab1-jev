"""Support ticket triage with Jev (System I) and an LLM (System II)."""

import argparse
import json
import time
from pathlib import Path

from dotenv import load_dotenv
from typesafe_sdk import TypeSafeClient

from triage.pipeline import process
from triage.system_two import ReplyWriter


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file", default="data/tickets.json", help="JSON list of tickets")
    parser.add_argument("--text", help="process a single ticket instead of the file")
    parser.add_argument("--system-one-only", action="store_true", help="use Jev only, skip the LLM")
    args = parser.parse_args()

    load_dotenv()
    jev = TypeSafeClient()
    writer = None if args.system_one_only else ReplyWriter()
    tickets = [args.text] if args.text else json.loads(Path(args.file).read_text(encoding="utf-8"))

    for index, ticket in enumerate(tickets, start=1):
        started = time.perf_counter()
        outcome = process(ticket, jev, writer)
        elapsed = time.perf_counter() - started
        t = outcome.triage

        print(f"#{index} {ticket}")
        print(
            f"   System I: department={t.department} ({t.department_confidence:.2f}), "
            f"urgency={t.urgency:.2f} [{t.urgency_label}], language={t.language}, "
            f"spam={t.spam_probability:.2f}, complex={t.complexity_probability:.2f}"
        )
        print(f"   Action:   {outcome.action}  ({elapsed:.2f}s)")
        if outcome.reply:
            print(f"   Reply:    {outcome.reply}")
        print()


if __name__ == "__main__":
    main()
