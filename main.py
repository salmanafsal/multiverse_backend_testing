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

app = FastAPI()





#Write the categories and items olov2 end point call
def olov2datacallmerchantmetadata(ids):

    url = f'https://clover.com/olov2service/v2/merchants/{ids}'
    response = requests.get(url)
    data = response.json()
    return data

def olov2categorydata(ids):

    url = f'https://clover.com/olov2service/v1/item/{ids}/getCategories'
    response = requests.get(url)
    data = response.json()
    key_to_find = ids
    #key_value_list.append({id:data})

    names = []
    catids = []
    for pair in data:
        names.append(pair['name'])
        catids.append(pair['id'])
    return names,catids

def olov2itemsdata(ids):

    
    url = f'https://www.clover.com/olov2service/v1/item/{ids}/searchItem'
    payload = json.dumps({
    "limit": 100,
    "pageIndex": 1,
    "sortOrderColumns": [
    "name"
    ],
    "searchQuery": "",
    "itemType": "REGULAR",
    "sortBy": "ASC"
    })
    headers = {
    'Content-Type': 'application/json',
    'X-Clover-Appenv': 'dev::dev1'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    try:
        data = json.loads(response.text)
        #print(data)
    except requests.JSONDecodeError:
        print("Invalid JSON. Defaulting to an empty dictionary.")
        #print(data)
        data = []  # Default to an empty dictionary
    except Exception as e:  # Handles other exceptions like network issues
        #print(f"An error occurred: {e}")
        data = []  # Default to an empty list    
        
    #print(data)
    if ("elements" in data) and (isinstance(data["elements"], list)) and (len(data['elements'])>0):
        item_names = [item["name"] for item in data["elements"]]
        if(len(item_names)>10):
            random_selection = random.sample(item_names, 10)
            return random_selection
        else:
             return item_names
    else:
        return 'No item name found for this merchant'
        

    

def snowflakeconnection(mid):
    
    account_identifier = 'clover' 

    user_name = 'salman.afzal@CLOVER.COM' # Gets the version by querying from snowflake 

    ctx = snowflake.connector.connect( user=user_name, account=account_identifier, authenticator='externalbrowser' ) 

    cs = ctx.cursor()
    cs.execute('use warehouse DEMO_WH')

# sample query

    mmetadata_query = cs.execute(f"""select mm.*, sg.*
    
from northamerica.summary.merchant_metadata mm 
join northamerica.base.online_order_merchant_provider oomp on mm.id = oomp.merchant_id
join northamerica.base.online_order_provider oop on oomp.provider_id = oop.id
join sigma.sigma.view_NAM_BUSINESS_MCC_CE1083533B604506B25D6876C697E6BD_MAT sg on mm.mcc_code = sg."Mcc Code" 
where oop.name in ('Clover Online Shopping','Clover Online Booking')
    and mm.is_demo = False
    and mm.account_status_active = True
    and mm.uuid = '{mid}';""")

    Data = mmetadata_query.fetch_pandas_all()
    #print(type(Data))
    #print("Column names:", Data.columns.tolist())
    selected_columns = ['CLOVER_CATEGORY', 
                    'Merch Industry', 'Mcc Code Desc', 
                    'Product Sub Vertical']
    #print(mmetadata_query)
    #Mmetadata = pd.DataFrame(tuple(cs.fetchall()), columns=[col[0] for col in cs.description])
    
    SelectedMDeta = Data[selected_columns]
    return SelectedMDeta
    


@app.post("/{merchant_uuid}/generate_text")
async def update_item(merchant_uuid: str):
    mydata = olov2datacallmerchantmetadata(merchant_uuid)
    catnames, catids = olov2categorydata(merchant_uuid)
    itemnames = olov2itemsdata(merchant_uuid)

    MerchantName = mydata.get('name')
    Phone = mydata.get('phone')
    Address = [mydata.get('address')]
    mydata = snowflakeconnection(merchant_uuid)
    clover_category_value = mydata["CLOVER_CATEGORY"][0]
    merchant_industry = mydata["Merch Industry"][0]
    mcc_code_desc = mydata["Mcc Code Desc"][0]
    product_sub_vertical = mydata["Product Sub Vertical"][0]


    
    results = {"name": MerchantName,"Address": Address,"catData":catnames,"catids":catids,"product_sub_vertical":product_sub_vertical,"item names":itemnames}
    
    return results