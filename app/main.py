from fastapi import FastAPI, HTTPException

from app.calculator import add, divide

app = FastAPI(title="Sample Calculator API", version="1.0.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "version": "1.0.28"}



@app.get("/add")
def add_endpoint(a: float, b: float) -> dict[str, float]:
    return {"result": add(a, b)}


@app.get("/divide")
def divide_endpoint(a: float, b: float) -> dict[str, float]:
    try:
        return {"result": divide(a, b)}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
