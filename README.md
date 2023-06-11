# HACE SEARCH ENGINE

![image](https://github.com/Geo4367/Project_HACE/assets/86464328/404b960d-c469-4673-aa16-49623a3c2a28)


## Description

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



## Table of Contents

**1. Lambda textract job creation 
**2. Lambda text parsing**
**3. Embedder Code(EC2)**
**4. Hace Django Project**
**5. User Interface****

## Installation
**1. Lambda textract job creation 
**2. Lambda text parsing**

  ![image](https://github.com/Geo4367/Project_HACE/assets/86464328/2646b335-1162-4791-8a5c-eced445d02b3)
  
  Once the PDF file is uploaded to the S3 bucket directory, a trigger is set to the S3, which initiates the lambda function. The lambda function, in turn, creates a Textract job with a unique job ID. Subsequently, a cache file in JSON format is generated and stored in the intermediate S3 bucket directory. Upon this occurrence, an SNS notification is sent to notify the second lambda function, which accesses the intermediate S3 bucket directory to locate the cached JSON file using the previously generated job ID. The text parsing lambda function then extracts the text from the JSON file created during the intermediate step, and saves it as a CSV file in the output S3 bucket.
  
**follow the tutorial in the below link for any clarifications:**
 https://www.youtube.com/watch?v=L6vdd9OYF_8
  
 **3. Embedder Code(EC2)** 
 
  After which the folder containing the CSV will be mounted on the EC2 instance. Once this is done the '**Embedder Code**', a python file deployed in the EC2 will continuously monitor the csv folder for any new csv files

what happens inside the embedder file is meticulously defined below

embedder file is a Python script that monitors a folder for text files, processes the files, generates embeddings for the text using the OpenAI API, and saves the results in a pandas DataFrame. Here's a breakdown of the script

1. Import necessary libraries: The script starts by importing the required libraries, including `json`, `boto3`, `os`, `csv`, `io`, `pickle`, `time`, `pandas`, `openai`, and `clear_output`.

2. Set up API key and variables: The script sets up the OpenAI API key (`api_key`) and initializes variables for request tracking and rate limiting.

3. Define the `generate_embeddings` function: This function takes a text input and model name as parameters and uses the OpenAI API to generate embeddings for the text. It keeps track of the request count and handles rate limiting to ensure the API usage stays within the allowed limits.

4. Define DataFrame and file paths: The script sets up the DataFrame (`df`) with column names and defines the paths for the folder to monitor for new files (`folder_to_monitor`), the folder to move processed files to (`processed_folder`), and the location to save the pickle file containing the DataFrame (`pickle_location`).

5. Initialize the DataFrame and pickle file: The script creates an empty DataFrame and saves it as a pickle file.

6. Monitor the folder for new files: The script enters an infinite loop and repeatedly checks the folder for new files. It processes any new files by reading their contents, generating embeddings for the text using the `generate_embeddings` function, and appending the results to the DataFrame (`df`). After processing, it moves the processed files to the specified folder.

7. Load the existing DataFrame from the pickle file: At the end of each loop iteration, the script loads the existing DataFrame from the pickle file (`pickle_location`) and assigns it to `ret_df`.

8. Merge the processed DataFrame with the existing DataFrame: The script concatenates the processed DataFrame (`df`) with the existing DataFrame (`ret_df`) and assigns the result to `ret_df`.

9. Clear the processed DataFrame: The script clears the processed DataFrame (`df`) to prepare for the next iteration.

10. Save the updated DataFrame to the pickle file: The script saves the updated DataFrame (`ret_df`) to the pickle file (`pickle_location`) to persist the data between iterations.

11. Output the types of the embeddings: The script iterates over the `ada_v2_embedding` column of the DataFrame (`ret_df`) and prints the type of each embedding.

12. Wait before checking again: The script pauses execution for 60 seconds before starting the next iteration to avoid continuous checking of the folder.

The script continues to monitor the folder, process new files, and update the DataFrame with the embeddings until it is interrupted externally or a specific condition is met.


**4. Hace Django Project**
Contains a django project that provides two webservices. 
1. HACE search engine 
2. HACE question-answering bot
The** view.py** in the query app of the django project includes Django views for a web application that performs semantic search and handles PDF file operations. Here's a breakdown of the views

    sem_search: This view handles the semantic search functionality. It retrieves the search query from the request parameters (q) and performs a cosine similarity search using the cosine_smilarity module. The top matching results are then processed to generate URLs for viewing and downloading the corresponding PDF files. The results are formatted as JSON and returned as an HTTP response.

    pdf_list: This view retrieves a list of PDF files in the media folder and generates metadata for each file, including URLs for viewing and downloading. The list of file metadata is passed to a template (pdf_list.html), which renders the HTML with the file information.

    download: This view handles file downloads. It takes the filename as a parameter and constructs the file path. If the file exists, it creates a FileResponse with the file content and sets the appropriate headers for the browser to download the file. If the file does not exist, it raises an Http404 exception.

    ask_hace: This view handles HACE (Hybrid Agent for Customer Engagement) requests. If the request method is GET, it retrieves the query parameter (q) and passes it to the davinci function in the cosine_smilarity module. The response from davinci is returned as an HTTP response. If the request method is not GET, it returns an "Invalid request method" response.

The code also includes the following additional code:
The df_similarities DataFrame is loaded from the pickle file "C:/Users/44744/Desktop/embedded.pickle".
The necessary imports are included, such as HttpResponse, JsonResponse, FileResponse, Http404, response, and modules from Django and other files (cosine_smilarity).
The settings module is imported from openai_project.settings to access the MEDIA_ROOT path.
The views and functions are defined within a Django application.

Note: Make sure you have the required templates and necessary configurations in your Django project for these views to work correctly.

The **cosine_similarity.py** is a python file that performs a search for embedded documents based on cosine similarity. It uses OpenAI's text-embedding-ada-002 model to generate embeddings for the user query and the documents in the dataframe.

Here's how the code works
The get_embedding function takes a text input and a model name as parameters and returns the embedding for the input text using the specified model.
The search_docs function takes a dataframe (df), a user query (user_query), the number of top results to retrieve (top_n), and a boolean flag indicating whether to print the results (to_print). It calculates the embedding for the user query and computes the cosine similarity between the query embedding and the embeddings of the documents in the dataframe. It then sorts the dataframe based on the similarity scores and returns the top top_n results.

The davinci function takes a query as input. It reads a precomputed dataframe of document similarities from a pickle file. It then calls the search_docs function to retrieve the most similar documents based on the query. It sets up a conversation prompt by combining an initial prompt, the retrieved context from the similar documents, and the user question. It uses OpenAI's text-davinci-003 model to generate a response to the combined prompt.

Please note that the code assumes you have the necessary dependencies installed and have a valid API key for OpenAI. Also, make sure you have the pickle file (embedded.pickle) in the specified location.

**5. User Interface** inside the **TestWeb**

**hace.js**: JavaScript code snippet that defines several functions for handling user interactions on a web page. Here's a brief explanation of each function

**askHace()**: This function is called when the user performs a query using an input field with the id "haceInput". It retrieves the query text, sends an AJAX GET request to a specified URL with the query text as a parameter, and handles the success response by calling the openHacePopUp() function with the received message.

**Search():** This function is called when the user performs a search using an input field with the id "myInput". It retrieves the search query text, sends an AJAX GET request to a specified URL with the query text as a parameter, and handles the success response by dynamically generating a table with search results based on the received JSON data. It also sets up event listeners for each row in the table to open a content popup.

**openPopUp**(tr, text): This function is called when a user clicks on a row in the search results table. It takes the clicked row element (tr) and the associated content text as parameters. It opens a content popup by toggling the "show" class on the popup element and sets the popup content to the provided text.

**openHacePopUp**(text): This function is called when a response is received from the Hace API call. It takes the response text as a parameter. It opens a Hace popup by toggling the "show" class on the popup element and sets the popup content to the received text.

switch_tab(evt, tab): This function is called when a tab link is clicked. It takes the event object (evt) and the target tab element (tab) as parameters. It hides all tab content elements by setting their display style to "none", removes the "active" class from all tab links, shows the selected tab content element by setting its display style to "block", and adds the "active" class to the clicked tab link.
This is used in conjunction with HTML and CSS code to create an interactive web page where users can perform searches and view search results and additional information in popups.

Better to install a tomcat server inside the EC2, inside which the TestWeb user interface will be hosted. 


  
## Usage
The image below shows the end product, once the project is configured correctly

![image](https://github.com/Geo4367/Project_HACE/assets/86464328/4e98e5e6-9aca-4828-8b0a-3507ca829b8e)



## Configuration
Lambda: necessary layers must be added to the lambda function to achieve the desired result. 
![image](https://github.com/Geo4367/Project_HACE/assets/86464328/b9b1871e-649c-41d5-9dfe-4f4c6a98fb32)

EC2: For the deployment of the embedder file and the django project, necessary dependancies must be installed beforehand. As per the requirement of the different 
python files, necessary libraries must be installed. 

## Credits

tutorial 1: AWS textract 
  https://www.youtube.com/watch?v=L6vdd9OYF_8&t=292s


## Roadmap

Making use of **Pinecone database ** instead of pandas dataframe

The Pinecone vector database offers several advantages that make it a powerful tool for working with high-dimensional vectors:

1. **Efficient Similarity Search:** Pinecone is designed for fast and accurate similarity search, enabling you to find the most similar vectors to a given query efficiently. It utilizes advanced indexing and retrieval algorithms optimized for high-dimensional data.

2. **Scalability:** Pinecone is built to scale with your data. It can handle millions or even billions of vectors, ensuring that you can easily accommodate large-scale applications and growing datasets.

3. **Real-Time Updates:** Pinecone supports real-time updates, allowing you to add or remove vectors from the database without downtime. This is particularly useful in dynamic applications where vectors need to be continuously updated or replaced.

4. **High Dimensionality Support:** Pinecone excels in handling high-dimensional vectors, such as those commonly encountered in natural language processing, computer vision, and other machine learning domains. It efficiently indexes and searches vectors with hundreds or even thousands of dimensions.

5. **API Integration:** Pinecone provides an easy-to-use API that allows seamless integration into your applications. You can quickly integrate Pinecone into your existing workflows and leverage its capabilities without extensive infrastructure setup.

6. **Cloud-Based Service:** Pinecone is a cloud-based service, which means you don't have to worry about managing the underlying infrastructure. It handles the scalability, availability, and performance aspects, allowing you to focus on your application logic.

7. **Community and Support:** Pinecone offers a supportive community and comprehensive documentation, making it easier to get started and troubleshoot any issues you may encounter. The Pinecone team actively maintains and improves the platform, ensuring a reliable and up-to-date experience.

Overall, the Pinecone vector database provides an efficient and scalable solution for similarity search, enabling you to build applications that require fast and accurate retrieval of high-dimensional vectors.

**Hybrid search engine:**

A hybrid search engine combines the strengths of multiple search techniques, such as semantic search, keyword search, and other advanced algorithms, to provide a more comprehensive and accurate search experience. Here are some advantages of a hybrid search engine over a simple semantic search engine:

1. Enhanced Relevance: A hybrid search engine can leverage semantic search capabilities to understand the context and meaning of search queries, resulting in more accurate and relevant search results. By incorporating keyword-based search as well, it can consider both the literal terms used in the query and the underlying intent, leading to improved relevance.

2. Improved Precision and Recall: Semantic search engines primarily rely on the meaning and relationships between words, but they may sometimes overlook relevant results if the query doesn't match exactly or if the semantic analysis doesn't capture the desired context. A hybrid search engine can address this limitation by combining semantic search with keyword search, ensuring a higher precision and recall rate by considering both textual relevance and contextual understanding.

3. Handling Ambiguity: Language can be ambiguous, and semantic search engines may struggle to disambiguate certain queries with multiple possible interpretations. Hybrid search engines can overcome this challenge by incorporating additional search techniques. For example, they can consider the search history, user preferences, or user location to refine the search results and provide more accurate answers.

4. Diverse Content Discovery: Semantic search engines tend to focus on retrieving highly relevant results, which can sometimes result in a narrow range of content. Hybrid search engines can offer a broader content discovery experience by incorporating keyword search, which may include related but not directly relevant information. This enables users to explore diverse perspectives and discover new content that they might not have found otherwise.

5. Flexibility: Hybrid search engines can be more flexible in adapting to different user preferences and needs. They can provide a combination of search approaches, allowing users to choose the most suitable method based on their requirements. This versatility ensures a personalized search experience tailored to individual preferences, improving overall user satisfaction.

In summary, a hybrid search engine offers advantages such as enhanced relevance, improved precision and recall, better handling of ambiguity, diverse content discovery, and increased flexibility. By combining different search techniques, it provides a more comprehensive and accurate search experience, catering to a wider range of user needs.


## Acknowledgments

Prof Kaveh Kiani
Elizabeth Burroughs

