from pydantic import BaseModel, field_validator
import string

class ChangePasswordDTO(BaseModel):
    password: str
    new_password: str

@field_validator("password")
def check_password_length(cls, value):    
        if(len(value) < 8):
            raise ValueError("Password should be at least 8 characters long")
        if not any(char.isupper() for char in str(value)):
          raise ValueError("Password must have at least one uppercase letter")
            
        if not any(c.islower() for c in value):
            raise ValueError("Password must have at least one lowercase letter")
    
        if not any(c.isdigit() for c in value):
            raise ValueError("Password must have at least one digit")

        if not any(c in string.punctuation for c in value):
            raise ValueError("Password must have at least one special chracter")
        
        return value