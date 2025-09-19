from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime
import uvicorn
import os
import json

app = FastAPI(title="Sheets → API", version="1.0.0")

# === Auth Bearer mínima ===
API_TOKEN = os.getenv("API_TOKEN", "mi_token_secreto_123")
security = HTTPBearer()

async def validate_token(cred: HTTPAuthorizationCredentials = Depends(security)):
    if cred.credentials != API_TOKEN:
        raise HTTPException(status_code=401, detail="Token inválido")
    return True

# === Modelo de entrada: { "data": [ { ... }, ... ] } ===
class SheetData(BaseModel):
    data: List[Dict[str, Any]]

# === Almacenamiento en memoria ===
STORE: List[Dict[str, Any]] = []

def preview_first_15_fields(record: Dict[str, Any]) -> Dict[str, Any]:
    out = {}
    for i, (k, v) in enumerate(record.items()):
        if i >= 15:
            break
        try:
            json.dumps(v)  # valida serialización
            out[k] = v
        except Exception:
            out[k] = str(v)
    return out

@app.post("/api/sheet-data")
async def receive_sheet_data(payload: SheetData, _: bool = Depends(validate_token)):
    if not payload.data:
        return {"status": "ok", "received": 0, "total_in_memory": len(STORE), "ts": datetime.now().isoformat()}

    STORE.extend(payload.data)

    # Log útil en consola
    print(f"[{datetime.now().isoformat()}] Recibidos {len(payload.data)} registros. Total en memoria: {len(STORE)}")
    preview = preview_first_15_fields(payload.data[0])
    print("Vista previa (primer registro, 15 campos máx.):")
    print(json.dumps(preview, ensure_ascii=False, indent=2))

    return {"status": "ok", "received": len(payload.data), "total_in_memory": len(STORE), "ts": datetime.now().isoformat()}

@app.delete("/api/sheet-data")
async def clear_cache(_: bool = Depends(validate_token)):
    STORE.clear()
    print(f"[{datetime.now().isoformat()}] Cache limpiado (STORE vacío).")
    return {"status": "ok", "message": "Cache limpiado", "ts": datetime.now().isoformat()}

@app.get("/health")
async def health():
    return {"status": "healthy", "ts": datetime.now().isoformat()}

if __name__ == "__main__":
    # Nginx proxy en 443 -> aquí 8000
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
