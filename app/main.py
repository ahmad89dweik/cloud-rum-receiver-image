from fastapi import FastAPI

app = FastAPI(title="cloud-rum-receiver-poc")


@app.get("/")
def health() -> dict[str, str]:
    return {"status": "ok"}
