import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from run_agent import main as run_agent_main

app = FastAPI()

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/run-agent")
async def run_agent_endpoint():
    try:
        run_agent_main()
        return JSONResponse(content={"status": "Agent run complete"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
