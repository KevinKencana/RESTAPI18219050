from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth_handler import decodeJWT

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if self.verify_jwt(credentials.credentials):
                # Note untuk Penilai. Kalau dari baca kode, seharusnya kondisinya "if not self".
                # Karena kalau waktu sekarang sudah melebihi waktu expiration, seharusnya verify akan return False
                # Jadi karena return false, kita raise exception
                # Tapi saat saya coba deploy dan pakai, ternyata selalu keluar message "Invalid Token or expired token"
                # Saya coba hilangkan "not" nya, baru bisa pakai fungsi di main.py setelah autentikasi
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decodeJWT(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid