#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import json
import boto3
import os
import csv
import io
from io import BytesIO
import pickle
import time
import pandas as pd
import openai
from IPython.display import clear_output

api_key = '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'
openai.api_key = api_key
request_counter = 0
total_requests_sent = 0
rate_limit= 3000
start_timer=time.time()

def generate_embeddings(text, model="text-embedding-ada-002"):
    global request_counter
    global rate_limit
    global total_requests_sent
    global start_timer
    clear_output(wait=True)
    check_timer = time.time()
    duration = check_timer-start_timer
    print(duration)
    
    if int(duration) >= 60:
        start_timer=time.time()
        request_counter=0
    if request_counter == rate_limit and int(duration) <= 59:
        sleep_for = 60-int(duration)
        print("Sleeping for " + str(sleep_for) +" seconds")
        print("Total requests sent: ", total_requests_sent)
        time.sleep(sleep_for)
        start_timer = time.time()
        request_counter =0
    if request_counter < rate_limit:
        request_counter+=1
        total_requests_sent+=1
        print("Request counter: ", request_counter)
        print("Total requests sent: ", total_requests_sent)
        
    return openai.Embedding.create(input = [text], model=model)['data'][0]['embedding']

COLUMN_NAMES = ['content', 'filename', 'ada_v2_embedding']
df = pd.DataFrame(columns=COLUMN_NAMES)
folder_to_monitor = '/home/ubuntu/bucket/embed_ec2_text/text_for_embed/'
processed_folder = '/home/ubuntu/bucket/embed_ec2_text/processed_files/' # replace with your processed folder path
pickle_location = '/home/ubuntu/hace_project/embedded_file/embedded.pickle'

with open(pickle_location, 'wb') as f:
        pickle.dump(df, f)
        f.close()


while True:
    # Get the list of files in the folder
    files = os.listdir(folder_to_monitor)
    # Process any new files
    df = pd.DataFrame(columns=COLUMN_NAMES)
    for filename in files:
        with open(os.path.join(folder_to_monitor, filename)) as f:
            text_df = pd.read_csv(f)
            f.close()
            df_embeddings = text_df.copy()
            df_embeddings['ada_v2_embedding'] = text_df.content.transform(lambda x: generate_embeddings(x, model='text-embedding-ada-002'))
            df = pd.concat([df_embeddings, df], axis=0, ignore_index=True)
            os.rename(os.path.join(folder_to_monitor, filename), os.path.join(processed_folder, filename))
    
    with open(pickle_location, 'rb') as f:
        ret_df = pd.read_pickle(f)
        f.close()
    ret_df = pd.concat([df, ret_df], axis=0, ignore_index=True)
    df.drop(index=df.index, inplace=True)
    
    with open(pickle_location, 'wb') as f:
        pickle.dump(ret_df, f)
        f.close()
    for i in ret_df.ada_v2_embedding:
        print(type(i))
    # Wait for some time before checking again
    time.sleep(60) # Check every minute

