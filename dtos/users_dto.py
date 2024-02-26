from pydantic import BaseModel, Field, EmailStr, field_validator
from pydantic_extra_types.phone_numbers import PhoneNumber
import string


class UserDTO(BaseModel):
    email: EmailStr 
    username: str = Field(min_length=3, max_length=100)
    first_name: str = Field(min_length=3, max_length=100)
    last_name:  str = Field(min_length=3, max_length=100)
    password: str
    phone_number: PhoneNumber

    @field_validator("password")
    def validate_password(cls, value):
        
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