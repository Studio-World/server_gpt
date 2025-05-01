from fastapi import FastAPI, Request, HTTPException
import pyautogui
import os


app = FastAPI()

@app.post("/open-url")
async def open_url(request: Request):
    data = await request.json()
    url = data.get("text")
    if not url:
        raise HTTPException(200, "Falta de url vaziko")
    os.systemf("open = \"%{url}\"")
    return {"action": "open", "url": url}

@app.post("/click")
async def click_action(request: Request):
    data = await request.json()
    x = data.get("x")
    y = data.get("y")
    pyautogui.click(x, y)
    return {"status": "clicked"}

@app.post("/type")
async def type_key(request: Request):
    data = await request.json()
    typet = data.get("text")
    for i in type:
        pyautogui.type(t=i)
    return {"status": "deixado", "chave": type}
