# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Literal, Optional
import time

app = FastAPI(title="Mini Text Service", version="1.0.0")

class ClassifyRequest(BaseModel):
    # Campo de texto obrigatório com limite de caracteres [cite: 29]
    text: str = Field(..., min_length=1, max_length=2000)
    strategy: Optional[Literal["rules"]] = "rules"

class ClassifyResponse(BaseModel):
    category: Literal["pergunta", "relato", "reclamacao"]
    confidence: float
    strategy: str
    elapsed_ms: int

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/info")
def info():
    return {
        "service": "mini-text-service",
        "version": "1.0.0",
        "endpoints": ["/health", "/info", "/classify", "/echo"],
    }

@app.post("/echo")
def echo(payload: dict):
    # Útil para testar requests/response e debug de rede [cite: 46]
    return {"received": payload}

def classify_rules(text: str) -> tuple[str, float]:
    t = text.strip().lower()
    
    # Heurísticas simples (baseadas no PDF) [cite: 49]
    # Detecta perguntas
    if "?" in t or t.startswith(("como ", "por que ", "pq ", "qual", "quais ")):
        return "pergunta", 0.85
    
    # Detecta reclamações
    keywords_reclamacao = ["não funciona", "erro", "ruim", "problema", "insatisfeito", "reclama"]
    if any(k in t for k in keywords_reclamacao):
        return "reclamacao", 0.75
        
    # Default para relato
    return "relato", 0.60

@app.post("/classify", response_model=ClassifyResponse)
def classify(req: ClassifyRequest):
    start = time.time()
    
    text = (req.text or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="text must be non-empty")
        
    if req.strategy != "rules":
        raise HTTPException(status_code=400, detail="unsupported strategy")
        
    category, confidence = classify_rules(text)
    
    # Calcula tempo decorrido em ms
    elapsed_ms = int((time.time() - start) * 1000)
    
    return ClassifyResponse(
        category=category,
        confidence=confidence,
        strategy=req.strategy,
        elapsed_ms=elapsed_ms,
    )