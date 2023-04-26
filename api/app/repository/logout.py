from jose import JWTError,jwt,ExpiredSignatureError
from app.routers import auth

def close_session(token,username,SECRET_KEY,ALGORITHM):
    try:
            payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
            print(payload)
            user_id = payload.get("sub")
            print(auth.active_tokens[f"tokens{username}"])
            auth.active_tokens.pop(f"tokens{username}",None)
            return {"message": "Sesión cerrada exitosamente"}

    except ExpiredSignatureError:
        # Si el token ha expirado, retornar una respuesta de error
        return {"message": "Token expirado"}
    

    except (JWTError, KeyError):
        # Si el token es inválido o el ID del usuario no está en el payload, retornar una respuesta de error
        return {"message": "Token inválido"}
    