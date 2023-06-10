import os
import json
import boto3
import pandas as pd
import re


def lambda_handler(event, context):

    BUCKET_NAME = os.environ["BUCKET_NAME"]
    PREFIX = os.environ["PREFIX"]
    PREFIX2 = os.environ["PREFIX2"]

    job_id = json.loads(event["Records"][0]["Sns"]["Message"])["JobId"]
    filename= json.loads(event['Records'][0]['Sns']['Message'])['DocumentLocation']['S3ObjectName'].split("/")[-1].strip().replace('.pdf', '')
    filename = f"{filename}.csv"
    print(filename)
    file_name = filename.split('.')[0]
    print(file_name)
    

    page_lines = process_response(job_id)

    # csv_key_name = f"{job_id}.csv"
    df = pd.DataFrame(page_lines.items())
    df.columns = ["PageNo", "Text"]
    df.to_csv(f"/tmp/{filename}", index=False)
    upload_to_s3(f"/tmp/{filename}", BUCKET_NAME, f"{PREFIX}/{filename}")

    
    
    all_text = ""
    for value_list in page_lines.values():
    # Iterate through the list of values for the current key
        for value in value_list:
        # Append the current value to the all_text string, with a space added
            all_text += f"{value} "
    
    print('The Whole text')
    norm_text = normalize_text(all_text)
    print('Normalized text')
    print(norm_text)
    
    chunk_size = 1500
    words = norm_text.split()
    if len(words)>1500:
        chunks = [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
    else:
        chunks = [norm_text]
    ch_df = pd.DataFrame(chunks, columns=['content'])
    ch_df['filename'] = file_name
    print('Splited Text into dataframe:  ')
    print(ch_df)
    
    ch_df.to_csv(f"/tmp/{filename}", index=False)
    upload_to_s3(f"/tmp/{filename}", BUCKET_NAME, f"{PREFIX2}/{filename}")
    
    
    

    return {"statusCode": 200, "body": json.dumps("File uploaded successfully!")}


def upload_to_s3(filename, bucket, key):
    s3 = boto3.client("s3")
    s3.upload_file(Filename=filename, Bucket=bucket, Key=key)


def process_response(job_id):
    textract = boto3.client("textract")

    response = {}
    pages = []

    response = textract.get_document_text_detection(JobId=job_id)

    pages.append(response)

    nextToken = None
    if "NextToken" in response:
        nextToken = response["NextToken"]

    while nextToken:
        response = textract.get_document_text_detection(
            JobId=job_id, NextToken=nextToken
        )
        pages.append(response)
        nextToken = None
        if "NextToken" in response:
            nextToken = response["NextToken"]

    page_lines = {}
    for page in pages:
        for item in page["Blocks"]:
            if item["BlockType"] == "LINE":
                if item["Page"] in page_lines.keys():
                    page_lines[item["Page"]].append(item["Text"])
                else:
                    page_lines[item["Page"]] = []
    return page_lines
    
def normalize_text(s, sep_token = " \n "):
    s = re.sub(r'\s+',  ' ', s).strip()
    s = re.sub(r". ,","",s)
    # remove all instances of multiple spaces
    s = s.replace("..",".")
    s = s.replace(". .",".")
    s = s.replace("\n", "")
    s = s.replace("#","")
    s = s.strip()
    if s =="":
        s = "<blank>"
    return s

