import re
from pydantic import BaseModel, Field, EmailStr, validator
import validators

class PostSchema(BaseModel):
    id: int = Field(default=None)
    title: str = Field(...)
    content: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "title": "Securing FastAPI applications with JWT.",
                "content": "In this tutorial, you'll learn how to secure your application by enabling authentication using JWT. We'll be using PyJWT to sign, encode and decode JWT tokens...."
            }
        }

# write validation schema for account user by using pydantic


class AccountSchema(BaseModel):
    company_name: str = Field(...,  min_length=3, max_length=15)
    company_country: str = Field(...)
    company_city: str = Field(...)
    company_adress: str = Field(..., min_length=10, max_length=30)
    company_taxid: int = Field(...)
    company_phone: str = Field(...) 
    @validator("company_phone")
    def phone_validation(cls, v):
        regex = r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$"
        if v and not re.search(regex, v, re.I):
            raise ValueError("Phone Number Invalid.")
        return v

    class Config:
        orm_mode = True
        use_enum_values = True
    company_website: str = Field(...)
    @validator("company_website")
    def company_website_validation(cls, v):
        if validators.url(v) == True:
            return v    
        raise ValueError("Url Invalid.")
    
    company_email: EmailStr = Field(...)
    name: str = Field(..., min_length=3, max_length=15)
    surname: str = Field(...)
    email: EmailStr = Field(...)
    phone: str = Field(...)
    @validator("phone")
    def phone_validation_phone(cls, v):
        regex = r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$"
        if v and not re.search(regex, v, re.I):
            raise ValueError("Phone Number Invalid.")
        return v

    class Config:
        orm_mode = True
        use_enum_values = True
    role_company: str = Field(...)
    password: str = Field(...,  min_length=8, max_length=20)
    @validator('password', always=True)
    def validate_password_Sign(cls, value):
        password = value
        errors = ''
        if not any(character.islower() for character in password):
            errors += 'Password should contain at least one lowercase character.'
        if not any(character.isupper() for character in password):
            errors += 'Password should contain at least one uppercase character.'
        if not any(character.isnumeric() for character in password):
            errors += 'Password should contain at least one number character.'
        if errors:
            raise ValueError(errors)
        
        return value
    password2: str = Field(...)
    @validator('password2')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('passwords do not match')
        return v

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Joe Doe",
                "email": "joe@xyz.com",
                "password": "any"
            }
        }

class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...,  min_length=8, max_length=20)


    class Config:
        schema_extra = {
            "example": {
                "email": "joe@xyz.com",
                "password": "any"
            }
        }