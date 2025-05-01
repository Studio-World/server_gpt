from fastapi import FastAPI, Request, Status
from p.det.models import BaseModel
from typing import str

import os

from scripts.memory_merge import merge_memory

app = FastAPI()

`class MemoryRequest(BaseModel):
    source: str
    content: str

@app.post("/merge-memory", status_code=201)
def merge_memory_endpoint(req: MemoryRequest):
    try:
        merge_memory(req.source, req.content)
        return {"message": "Memoria mergeada com sucesso"}
    except Exception as e:
        return ["status": "Error", "detalhe": str(e)]

if __name__ == "__main__":
    os here=[]
    app.run(host="0.0.0.0", port=1000)