# Project_HACE
Extraction of the text 

Since the data(pdfs) was saved in the AWS S3 bucket, a pipeline was built to extract

the text from the pdfs using a service named textract provided by the AWS itself.

For making this happen AWS lambda functions were utilized as well. Lambda

functions were used to create the job as well as parse the text from the cached files,

formed in the intermediate step. Text extracted from these pdfs are saved as csv files

in another S3 bucket directory. 

Embedding the Text 

Text from each pages of the pdfs are parsed and saved separately in the csv files. 

This step focuses on embedding the text from each pages of the pdfs using the 

API service provided by the Open-AI. A python script is put in place inside of an 

EC2 instance. This is written in such a way that it is continuously monitoring the 

folder where the csv files are saved after extracting the text from the pdfs. When 

new files are added to the folder, the Open-AI embedder will retrieve them and 

generate text embeddings. This is an ongoing procedure, and these new 

embeddings will be merged with those from the previous procedure. These 

embeddings along with the filename, text and the page number will be saved 

inside a pandas dataframe. To preserve the datatype of the embeddings, this 

dataframe will be saved as pickle file in the filesystem. 

Django Application 

To make the whole process into a service, a Django project was built. Two 

services were written . One for the semantic search and the other for question 

answering bot. For the semantic search engine, once the query gets passed into 

the system, it will get embedded using the ADA model offered by the Open-AI 

API. The first service, which is the semantic search make use of cosine similarity 

to retrieve the pages of the document which has the most similarity with the 

embedded query text. For the second service, text generating model offered by 

the Open-AI is used to generate a chatbot on top of the extracted text. 

User Interface 

In the next, a simple user interface is made for pdf search as well as for the 

question answering bot. This is done using simple HTML, CSS and JavaScript. 

Hosting on AWS 

Since this is meant to be a webservice, everything accomplished above should be 

moved to the cloud. For this purpose, an EC2 instance has to be instantiated. The 

Django project along with the UI from end will be moved to the cloud. 
