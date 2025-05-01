# main_web.py
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os, json, sqlite3, logging

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PUBLIC_DOMAIN = "https://www.carlosdev.app.br"
GITHUB_PLUGIN_URL = f"{PUBLIC_DOMAIN}/github-ai-plugin.json"
GITHUB_YAML_URL = f"{PUBLIC_DOMAIN}/api.github.com.yaml"
GOOGLE_DRIVE_YAML_URL = f"{PUBLIC_DOMAIN}/google-drive-api.yaml"

DB_PATH = "/mnt/data/memory.db"
CHATLOG_PATH = "/mnt/data/chatlog.jsonl"

@app.get("/")
def root():
    return {"status": "✅ Servidor leve ativo - carlosdev.app.br"}

@app.get("/.well-known/api-config")
def api_config():
    return {
        "github_spec": GITHUB_YAML_URL,
        "drive_spec": GOOGLE_DRIVE_YAML_URL,
        "plugin_version": "1.0.0",
        "plugin_manifest": GITHUB_PLUGIN_URL
    }

@app.get("/config/{file_name}")
def serve_yaml(file_name: str):
    file_path = f"/home/carlos/public_yaml/{file_name}"
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="text/yaml")
    return {"error": "Arquivo não encontrado"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
@app.post("/chatlog/append")
async def save_chatlog(request: Request):
    data = await request.json()
    if not data.get("role") or not data.get("content"):
        raise HTTPException(status_code=400, detail="Campos 'role' e 'content' são obrigatórios.")
    try:
        with open(CHATLOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")
        return {"status": "salvo", "registro": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gravar chatlog: {e}")

@app.get("/chatlog/view")
def view_chatlog():
    try:
        with open(CHATLOG_PATH, "r", encoding="utf-8") as f:
            linhas = f.readlines()
        return {"linhas": [json.loads(l) for l in linhas]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao ler chatlog: {e}")

@app.get("/memory/export")
def export_memory():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            rows = conn.execute("SELECT * FROM memory ORDER BY id DESC").fetchall()
        return {"logs": [{"id": r[0], "prompt": r[1], "response": r[2], "timestamp": r[3]} for r in rows]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao exportar memória: {e}")

@app.post("/zapier/webhook-trigger")
async def zapier_webhook_trigger(request: Request):
    ZAPIER_SECRET = os.getenv("ZAPIER_SECRET", "zapier123")
    if request.headers.get("X-Zapier-Token") != ZAPIER_SECRET:
        raise HTTPException(status_code=403, detail="Token inválido")
    payload = await request.json()
    return JSONResponse(content={"mensagem": "Evento recebido", "dados": payload})
def init_db():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prompt TEXT,
                response TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()
    except Exception as e:
        logging.error(f"Erro ao iniciar banco: {e}")

@app.on_event("startup")
def startup_event():
    init_db()

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 7000))
    uvicorn.run("main_web:app", host="0.0.0.0", port=port, reload=True)
