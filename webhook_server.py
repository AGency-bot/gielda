from fastapi import FastAPI, Form

app = FastAPI()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/webhook/whatsapp")
async def whatsapp_webhook(From: str = Form(...), Body: str = Form(...)):
    # na razie logujemy i odsyłamy potwierdzenie
    print(f"📥 Incoming WhatsApp message from {From}: {Body}")
    return {"status": "received"}
