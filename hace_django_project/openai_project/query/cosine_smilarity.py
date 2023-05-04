# search embedded docs based on cosine similarity
import os
import time
import pandas as pd
import pickle
import openai
import re
import requests
import sys
from num2words import num2words
import numpy as np
from openai.embeddings_utils import cosine_similarity
from IPython.display import clear_output
# openai.api_key = getpass()
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

def get_embedding(text, model="text-embedding-ada-002"):
   return openai.Embedding.create(input = [text], model=model)['data'][0]['embedding']

def search_docs(df, user_query, top_n=100, to_print=True):
    embedding = get_embedding(
        user_query,
        model="text-embedding-ada-002"
    )

    df["similarities"] = df.ada_v2_embedding.apply(lambda x: cosine_similarity(x, embedding))

    res = (
        df.sort_values("similarities", ascending=False)
        .head(top_n)
    )
    # if to_print:
    #     print(res.filename)
    return res

def davinci(query):
        df_similarities = pd.read_pickle("C:/Users/44744/Desktop/embedded.pickle")
        res = search_docs(df_similarities, query, top_n=2)
        ai_question =  query             #input("How can I help you?\n\n")
        context= res.Text.values
        completion_model='text-davinci-003'

        initial_prompt = 'The following conversation is with Hacebot. your task to to do research on Child labour'
        # "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly."
        combined_prompt = initial_prompt + str(context) + "Q: " + ai_question
        response = openai.Completion.create(model=completion_model, prompt=combined_prompt, max_tokens=300)
        ai_response = response['choices'][0]['text'].replace('\n', '').replace(' .', '.').strip()
        return ai_response
