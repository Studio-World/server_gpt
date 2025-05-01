from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import requests, os, logging, json, time

from playwright.async_api import async_playwright
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/automation/playwright")
async def playwright_automation(request: Request):
    data = await request.json()
    url = data.get("url")
    if not url:
        raise HTTPException(status_code=400, detail="Campo 'url' é obrigatório.")
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(url)
            content = await page.content()
            await browser.close()
        return {"status": "ok", "content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro Playwright: {e}")


@app.post("/automation/selenium")
async def selenium_automation(request: Request):
    data = await request.json()
    url = data.get("url")
    if not url:
        raise HTTPException(status_code=400, detail="Campo 'url' é obrigatório.")
    try:
        import chromedriver_autoinstaller
        chromedriver_autoinstaller.install()
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        content = driver.page_source
        driver.quit()
        return {"status": "ok", "content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro Selenium: {e}")


@app.post("/automation/browser-use")
async def browser_use_automation(request: Request):
    from browser_automation.browser import run_browser_script
    data = await request.json()
    url = data.get("url")
    if not url:
        raise HTTPException(status_code=400, detail="Campo 'url' é obrigatório.")
    try:
        content = await run_browser_script(url)
        return {"status": "ok", "html": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no browser-use: {str(e)}")
GITHUB_API_BASE = "https://api.github.com"
AZURE_API_BASE = "https://dev.azure.com"
GOOGLE_API_BASE = "https://www.googleapis.com/drive/v3"

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
AZURE_DEVOPS_TOKEN = os.getenv("AZURE_DEVOPS_TOKEN")
GOOGLE_API_TOKEN = os.getenv("GOOGLE_DRIVE_TOKEN")

# === GITHUB
@app.get("/github/repos")
def list_github_repos():
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    r = requests.get(f"{GITHUB_API_BASE}/user/repos", headers=headers)
    return r.json()

@app.post("/github/repos/{owner}/{repo}/issues")
def create_issue(owner: str, repo: str, title: str = "Título padrão", body: str = "Criado via FastAPI"):
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}", "Accept": "application/vnd.github+json"}
    payload = {"title": title, "body": body}
    r = requests.post(f"{GITHUB_API_BASE}/repos/{owner}/{repo}/issues", headers=headers, json=payload)
    return r.json()

# === AZURE DEVOPS
@app.get("/azure/repos/{organization}/{project}")
def list_azure_repos(organization: str, project: str):
    headers = {"Authorization": f"Basic {AZURE_DEVOPS_TOKEN}"}
    r = requests.get(f"{AZURE_API_BASE}/{organization}/{project}/_apis/git/repositories?api-version=7.0", headers=headers)
    return r.json()

@app.get("/azure/builds/{organization}/{project}")
def list_azure_builds(organization: str, project: str):
    headers = {"Authorization": f"Basic {AZURE_DEVOPS_TOKEN}"}
    r = requests.get(f"{AZURE_API_BASE}/{organization}/{project}/_apis/build/builds?api-version=7.0", headers=headers)
    return r.json()

# === GOOGLE DRIVE
@app.get("/drive/list")
def list_drive_files(page_size: int = 10):
    headers = {"Authorization": f"Bearer {GOOGLE_API_TOKEN}"}
    params = {"pageSize": page_size, "fields": "files(id,name,mimeType)"}
    r = requests.get(f"{GOOGLE_API_BASE}/files", headers=headers, params=params)
    return r.json()

@app.get("/drive/file/{file_id}")
def get_file_metadata(file_id: str):
    headers = {"Authorization": f"Bearer {GOOGLE_API_TOKEN}"}
    r = requests.get(f"{GOOGLE_API_BASE}/files/{file_id}", headers=headers, params={"fields": "id,name,mimeType"})
    return r.json()

@app.get("/drive/file/{file_id}/download")
def download_file(file_id: str):
    headers = {"Authorization": f"Bearer {GOOGLE_API_TOKEN}"}
    r = requests.get(f"{GOOGLE_API_BASE}/files/{file_id}?alt=media", headers=headers, stream=True)
    return StreamingResponse(r.raw, media_type="application/octet-stream")

@app.delete("/drive/file/{file_id}/delete")
def delete_file(file_id: str):
    headers = {"Authorization": f"Bearer {GOOGLE_API_TOKEN}"}
    r = requests.delete(f"{GOOGLE_API_BASE}/files/{file_id}", headers=headers)
    return {"status": "Arquivo deletado", "code": r.status_code}
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "mistralai/Mistral-7B-Instruct-v0.1")

try:
    tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL_NAME, use_auth_token=HF_TOKEN)
    model = AutoModelForCausalLM.from_pretrained(LLM_MODEL_NAME, use_auth_token=HF_TOKEN)
    model.eval()
except Exception as e:
    logging.error(f"Erro ao carregar modelo local: {e}")

@app.post("/llm/generate")
async def generate_text(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")
    if not prompt:
        raise HTTPException(status_code=400, detail="Campo 'prompt' é obrigatório.")
    try:
        inputs = tokenizer(prompt, return_tensors="pt")
        with torch.no_grad():
            outputs = model.generate(**inputs, max_new_tokens=150)
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return {"response": generated_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar texto: {e}")


@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8001))
    uvicorn.run("main_core:app", host="0.0.0.0", port=port)
