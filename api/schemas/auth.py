from pydantic import BaseModel

class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str
    
class DecodedToken(BaseModel):
    username: str
    user_id: int
    role: str