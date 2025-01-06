from fastapi import FastAPI
from pydantic import BaseModel
import requests
import json
import os
import json
import time
import datetime
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

def olov2itemsdata(ids,catids):

    for catid in catids:
        url = f'https://clover.com/olov2service/v1/item/{ids}/searchItemByCategory/{catids}'
        response = requests.get(url)
        data = response.json()
        print("The category id is"+ str(catid)+ "The data is "+ str(data))

    

def snowflakeconnection(mid):
    
    account_identifier = 'clover' 

    user_name = 'salman.afzal@CLOVER.COM' # Gets the version by querying from snowflake 

    ctx = snowflake.connector.connect( user=user_name, account=account_identifier, authenticator='externalbrowser' ) 

    cs = ctx.cursor()
    cs.execute('use warehouse DEMO_WH')

# sample query

    mmetadata_query = cs.execute(f"""select * from northamerica.summary.merchant_metadata as ab join sigma.sigma.view_nam_business_mcc_ce1083533b604506b25d6876c697e6bd_mat as cd 
    on ab.mcc_code = cd."Mcc Code"
    where is_demo = FALSE
    and account_status_active = 'TRUE'
    and COLO_MERCHANT_PROFILE = 'Enabled' 
    and ab.uuid = '{mid}';""")

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
    #olov2itemsdata(merchant_uuid,catids)

    MerchantName = mydata.get('name')
    Phone = mydata.get('phone')
    Address = [mydata.get('address')]
    mydata = snowflakeconnection(merchant_uuid)
    clover_category_value = mydata["CLOVER_CATEGORY"][0]
    merchant_industry = mydata["Merch Industry"][0]
    mcc_code_desc = mydata["Mcc Code Desc"][0]
    product_sub_vertical = mydata["Product Sub Vertical"][0]


    
    results = {"name": MerchantName,"Address": Address,"catData":catnames,"catids":catids,"product_sub_vertical":product_sub_vertical}
    
    return results