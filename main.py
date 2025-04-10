from fastapi import FastAPI
from pydantic import BaseModel
import requests
import json
import os
import time
import datetime
import random
import numpy as np
# Data Processing Libraries
import pandas as pd
import snowflake.connector
from google.cloud import storage
from cryptography.fernet import Fernet
import base64
from pathlib import Path
import bcrypt
from fastapi import  HTTPException, Depends

from jose import JWTError, jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Security

JWT_SECRET_KEY = "test-secret-key"  # Use a more secure random key in production
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_TIME_MINUTES = 1440  # 24 hours

security = HTTPBearer()

app = FastAPI()

CREDENTIALS_FILE = "/Users/salman.afzal/Downloads/MultiverseBackendTesting/model/credentials.json"


def create_jwt_token(data: dict):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=JWT_EXPIRATION_TIME_MINUTES)
    to_encode.update({"exp": int(expire.timestamp())})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def decode_jwt_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

# Extracts user info from token
def get_current_user(token: HTTPAuthorizationCredentials = Security(security)):
    print(token.credentials)
    payload = decode_jwt_token(token.credentials)
    return payload.get("email")

class User(BaseModel):
    email: str
    password: str

class Snippet(BaseModel):
    language: str
    code: str

KEY_PATH = "/Users/salman.afzal/Downloads/MultiverseBackendTesting/model/secret.key"

def load_credentials():
    credentials_file = Path(CREDENTIALS_FILE)
    if credentials_file.exists():
        try:
            with open(CREDENTIALS_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []
    return []

def save_credentials(data):
    with open(CREDENTIALS_FILE, "w") as file:
        json.dump(data, file, indent=4)

@app.post("/user")
async def create_user(user:User):
    
    credentials = load_credentials()

    # Check if user already exists
    if any(u["email"] == user.email for u in credentials):
        raise HTTPException(status_code=400, detail="User already exists")

    # Hash password
    hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode()

    new_user = {"email": user.email, "password": hashed_password}
    credentials.append(new_user)
    save_credentials(credentials)

    return {"message": "User created successfully"}

def authenticate_user(user: User):
    credentials = load_credentials()
    
    for stored_user in credentials:
        if stored_user["email"] == user.email and bcrypt.checkpw(user.password.encode(), stored_user["password"].encode()):
            return stored_user  # Authentication successful
    return None  # Authentication failed

@app.post("/login")
async def login(user: User):
    authenticated_user = authenticate_user(user)
    if not authenticated_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_jwt_token({"email": user.email})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/user")
async def get_user(user: User):
    authenticated_user = authenticate_user(user)
    
    if not authenticated_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Return user info without the password
    return {"email": authenticated_user["email"]}

def get_encryption_key():
    key_file = Path(KEY_PATH)
    if key_file.exists():
        with open(KEY_PATH, "rb") as key_file:
            return key_file.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_PATH, "wb") as key_file:
            key_file.write(key)
        return key

ENCRYPTION_KEY = get_encryption_key()
cipher = Fernet(ENCRYPTION_KEY)


@app.get("/snippets")
async def getAllSnippets(current_user: str = Security(get_current_user)):
    
   
   file_path = "/Users/salman.afzal/Downloads/MultiverseBackendTesting/model/seedData.json"

   try:
        with open(file_path, "r") as file:
            seed_data = json.load(file)  # Load JSON data as a dictionary
   except (FileNotFoundError, json.JSONDecodeError):
        return {"error": "No data available"}

   decrypted_snippets = []

   for snippet in seed_data:
        decrypted_entry = snippet.copy()  # Copy to avoid modifying original data

        try:
            # Attempt to decrypt the 'code' field
            decrypted_entry["code"] = cipher.decrypt(snippet["code"].encode()).decode()
        except Exception:
            # If decryption fails, assume it's already plaintext and leave it as is
            pass  

        decrypted_snippets.append(decrypted_entry)

   return decrypted_snippets

@app.get("/snippets/{snippet_id}")
async def getAllSnippets(snippet_id: int):
    
   file_path = "/Users/salman.afzal/Downloads/MultiverseBackendTesting/model/seedData.json"

   with open(file_path, "r") as file:
        seed_data = json.load(file)  # Load JSON data as a dictionary
   for snippet in seed_data:    
        if snippet.get("id") == snippet_id:
            decrypted_code = cipher.decrypt(snippet["code"].encode()).decode()
            return {"id": snippet["id"], "language": snippet["language"], "code": decrypted_code}  # Return found snippet
       
   return "data does not exist"     


@app.post("/snippetsPost")
async def postAllSnippets(snippet: Snippet):
    
   file_path = "/Users/salman.afzal/Downloads/MultiverseBackendTesting/model/seedData.json"

   with open(file_path, "r") as file:
        seed_data = json.load(file)  # Load JSON data as a dictionary

   if seed_data:
        max_id = max(item.get("id", 0) for item in seed_data)  # Get max existing ID
   else:
        max_id = 0  # Start from 1 if no data exists

   new_id = max_id + 1  # Increment the ID     

   encrypted_code = cipher.encrypt(snippet.code.encode()).decode() 

   new_entry = {"id": new_id, "language": snippet.language, "code": encrypted_code}

   seed_data.append(new_entry)

   with open(file_path, "w") as file:
      json.dump(seed_data, file, indent=4)

    
   return seed_data