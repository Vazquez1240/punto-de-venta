from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime
import uvicorn
import os
import json

app = FastAPI(title="Sheets → API (mínimo)", version="1.0.0")

# === Auth mínima (Bearer) ===
API_TOKEN = os.getenv("API_TOKEN", "mi_token_secreto_123")
security = HTTPBearer()

async def validate_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != API_TOKEN:
        raise HTTPException(status_code=401, detail="Token inválido")
    return True

# === Modelo de entrada, compatible con tu script: { "data": [ {..fila..}, ... ] } ===
class SheetData(BaseModel):
    data: List[Dict[str, Any]]

# === Almacenamiento en memoria y helper de logging ===
STORE: List[Dict[str, Any]] = []

def preview_first_15_fields(record: Dict[str, Any]) -> Dict[str, Any]:
    # Toma los primeros 15 pares (clave:valor) según el orden de inserción del dict
    out = {}
    for i, (k, v) in enumerate(record.items()):
        if i >= 15:
            break
        # Serializa valores no JSON-ables para que el print no truene
        try:
            json.dumps(v)
            out[k] = v
        except Exception:
            out[k] = str(v)
    return out

# === Endpoint principal: recibe filas editadas y las imprime/almacena ===
@app.post("/api/sheet-data")
async def receive_sheet_data(payload: SheetData, _: bool = Depends(validate_token)):
    if not payload.data:
        return {"status": "ok", "received": 0, "timestamp": datetime.now().isoformat()}

    STORE.extend(payload.data)

    # Log útil en consola
    print(f"[{datetime.now().isoformat()}] Recibidos {len(payload.data)} registros. Total en memoria: {len(STORE)}")
    # Vista previa (primer registro + 15 campos)
    preview = preview_first_15_fields(payload.data[0])
    print("Vista previa (primer registro, 15 campos máx.):")
    print(json.dumps(preview, ensure_ascii=False, indent=2))

    return {
        "status": "ok",
        "received": len(payload.data),
        "total_in_memory": len(STORE),
        "timestamp": datetime.now().isoformat()
    }

# === Healthcheck (para pruebas rápidas desde Apps Script) ===
@app.get("/health")
async def health():
    return {"status": "healthy", "ts": datetime.now().isoformat()}

if __name__ == "__main__":
    # Lanza en 0.0.0.0:8000 (Nginx hace el proxy por 443)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
