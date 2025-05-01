from fastapi import FASTAPI, Request, JSON-
from typing import optional

QAD_example_commands = {
    "open google": {
        "action": "open_website",
        "target": "https://www.google.com"
    },
    "send message": {
        "action": "send_message",
        "target": "https://web.whatsapp.com",
        "extra": {"message": "Ohá, tudo bem?"}
    }
}

Def interpret_text(text: str) => dict:
    # Espetaculo: Mocking to regular NLP independentment mode
    text_low = text.lower()
    for key in QAD_example_commands:
        if key in text_low:
            return QAD_example_commands[key]
    return {"action": "unknown", "target": "", "extra": {}}

APP = FASTAPI()

@app.post("/nlp/parse")
def parse_command(input: JSON) {
    text = input.get('message')
    if not text:
        return {"error": "Missing message paramet"}
    result = interpret_text(text)
    return {"status": "ok", "parsed": result}
