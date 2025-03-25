from fastapi import FastAPI
from pydantic import BaseModel
import requests
import json
import os
import json
import time
import datetime
import random
import numpy as np
# Data Processing Libraries
import pandas as pd
import snowflake.connector
from google.cloud import storage


app = FastAPI()

class Snippet(BaseModel):
    language: str
    code: str



@app.get("/snippets")
async def getAllSnippets():
    
   file_path = "/Users/salman.afzal/Downloads/MultiverseBackendTesting/model/seedData.json"

   with open(file_path, "r") as file:
        seed_data = json.load(file)  # Load JSON data as a dictionary

   print(seed_data)
    
   return seed_data;

@app.get("/snippets/{snippet_id}")
async def getAllSnippets(snippet_id: int):
    
   file_path = "/Users/salman.afzal/Downloads/MultiverseBackendTesting/model/seedData.json"

   with open(file_path, "r") as file:
        seed_data = json.load(file)  # Load JSON data as a dictionary
   print(type(snippet_id))
   for snippet in seed_data:
        print(type(snippet.get("id")))
        if snippet.get("id") == snippet_id:
            return snippet  # Return found snippet
       
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

   new_entry = {"id": new_id, "language": snippet.language, "code": snippet.code}

   seed_data.append(new_entry)

   with open(file_path, "w") as file:
      json.dump(seed_data, file, indent=4)

    
   return seed_data