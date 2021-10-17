class UserSchema(BaseModel):
    username: str = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "username": "Kevin Kencana",
                "password": "tstseru"
            }
        }

class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "username": "Kevin Kencana",
                "password": "tstseru"
            }
        }