from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Dict, Any, Optional, Annotated
import uvicorn
from datetime import datetime
import json
import os

app = FastAPI(
    title="Google Sheets API",
    description="API para recibir y almacenar datos de Google Sheets",
    version="1.0.0"
)

# Configuración de CORS
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:5500",
    "*"  # Para permitir desde Google Apps Script
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración de autenticación
API_TOKEN = os.getenv("API_TOKEN", "mi_token_secreto_123")  # Token por defecto para desarrollo
security = HTTPBearer()

# Cache en memoria para almacenar los datos
data_cache: Dict[str, Any] = {
    "last_updated": None,
    "data": [],
    "total_records": 0
}

# Función para validar el token
async def validate_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Valida el token Bearer enviado en el header Authorization.
    """
    if credentials.credentials != API_TOKEN:
        raise HTTPException(
            status_code=401,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials

# Modelos Pydantic
class SheetData(BaseModel):
    data: List[Dict[str, Any]]

class CacheResponse(BaseModel):
    last_updated: Optional[str]
    total_records: int
    data: List[Dict[str, Any]]

# Endpoint para recibir datos del Google Sheet
@app.post("/api/sheet-data", response_model=dict)
async def receive_sheet_data(payload: SheetData, token: str = Depends(validate_token)):
    """
    Endpoint para recibir datos del Google Sheet.
    Guarda los datos en caché en memoria.
    """
    try:
        # Actualizar el cache
        data_cache["data"].extend(payload.data)
        data_cache["last_updated"] = datetime.now().isoformat()
        data_cache["total_records"] = len(data_cache["data"])
        
        return {
            "status": "success",
            "message": f"Recibidos {len(payload.data)} registros",
            "total_records": data_cache["total_records"],
            "timestamp": data_cache["last_updated"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando datos: {str(e)}")

# Endpoint para obtener todos los datos del cache
@app.get("/api/sheet-data", response_model=CacheResponse)
async def get_cached_data(token: str = Depends(validate_token)):
    """
    Obtiene todos los datos almacenados en caché.
    """
    return CacheResponse(
        last_updated=data_cache["last_updated"],
        total_records=data_cache["total_records"],
        data=data_cache["data"]
    )

# Endpoint para limpiar el cache
@app.delete("/api/sheet-data")
async def clear_cache(token: str = Depends(validate_token)):
    """
    Limpia todos los datos del caché.
    """
    data_cache["data"].clear()
    data_cache["last_updated"] = datetime.now().isoformat()
    data_cache["total_records"] = 0
    
    return {
        "status": "success",
        "message": "Cache limpiado exitosamente",
        "timestamp": data_cache["last_updated"]
    }

# Endpoint para obtener estadísticas del cache
@app.get("/api/stats")
async def get_stats():
    """
    Obtiene estadísticas del caché de datos.
    """
    return {
        "total_records": data_cache["total_records"],
        "last_updated": data_cache["last_updated"],
        "cache_size_mb": len(json.dumps(data_cache["data"])) / (1024 * 1024) if data_cache["data"] else 0
    }

# Endpoint de salud
@app.get("/health")
async def health_check():
    """
    Endpoint de salud para verificar que la API está funcionando.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Google Sheets API"
    }

# Endpoint para obtener información del token (solo para desarrollo)
@app.get("/api/token-info")
async def get_token_info():
    """
    Obtiene información sobre el token de autenticación.
    Solo para desarrollo - NO usar en producción.
    """
    return {
        "token": API_TOKEN,
        "message": "Usa este token en el header: Authorization: Bearer " + API_TOKEN,
        "google_apps_script_config": {
            "API_TOKEN": API_TOKEN,
            "AUTH_TYPE": "Bearer"
        }
    }

# Endpoint raíz
@app.get("/")
async def root():
    """
    Endpoint raíz con información básica de la API.
    """
    return {
        "message": "Google Sheets API con Autenticación",
        "version": "1.0.0",
        "authentication": "Bearer Token requerido para endpoints protegidos",
        "token_info": "GET /api/token-info para obtener el token de desarrollo",
        "endpoints": {
            "POST /api/sheet-data": "Recibir datos del Google Sheet (requiere auth)",
            "GET /api/sheet-data": "Obtener datos del caché (requiere auth)",
            "DELETE /api/sheet-data": "Limpiar caché (requiere auth)",
            "GET /api/stats": "Estadísticas del caché",
            "GET /api/token-info": "Información del token (solo desarrollo)",
            "GET /health": "Estado de la API"
        }
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)