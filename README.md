# nlp-lab1-jev

Homework 1 for the NLP Systems course. A small support-ticket triage tool built on System I + System II.

- **System I** is [Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev). It doesn't generate text. It answers typed questions (`Choice`, `Score`, `Noul`) and gives a probability for each answer.
- **System II** is a regular LLM (any OpenAI-compatible API). It writes replies to the customer.

## How it works

Each ticket goes to Jev once with five questions. Which department should handle it, how urgent it is, what language it's in, whether it's spam, and whether it needs a detailed answer (see `triage/system_one.py`).

Based on those answers, `triage/pipeline.py` does one of four things:

- Spam is dropped
- If Jev isn't sure about the department, the ticket goes to a human
- Complex or urgent tickets get a personal reply from the LLM (`triage/system_two.py`)
- Everything else gets a template reply

Only complex or urgent tickets reach the LLM, the rest is handled by Jev alone.

## Running

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add TYPESAFE_API_KEY and OPENAI_API_KEY
```

```bash
python main.py                    # run on data/tickets.json
python main.py --system-one-only  # Jev only, no LLM
python main.py --text "I can't log in"
```

Sample tickets in `data/tickets.json` are in English and Ukrainian.
