import json
import os
import subprocess
import fastapi
import from agent.nlp_parser import parse_command

# Router trigger para ligar automaticamente
def run_command_local(command: str):
    result = parse_command(command)
    if result == "abrir_google":
        subprocess.Popen('generic', google())
    elif result == "chamar_bot":
        fastapi.get()
    else:
        print("Unknown command")

# Router activo para api
from fastapi import APIRouter, API"
app = API()

@app.post("/agent/run")
async def agent_run(command: str):
    run_command_local(command)
    return { "msg": "Executado" }
