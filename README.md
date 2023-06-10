# Project Title

HACE SEARCH ENGINE

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

1. Lambda textract job creation 
2. Lambda text parsing
3. Embedder Code(EC2)
4. Hace Django Project
5. User Interface

## Installation

1. Lambda textract job creation
2. Lambda text parsing

  ![image](https://github.com/Geo4367/Project_HACE/assets/86464328/2646b335-1162-4791-8a5c-eced445d02b3)
  
  Once the PDF file is uploaded to the S3 bucket directory, a trigger is set to the S3, which initiates the lambda function. The lambda function, in turn, creates a Textract job with a unique job ID. Subsequently, a cache file in JSON format is generated and stored in the intermediate S3 bucket directory. Upon this occurrence, an SNS notification is sent to notify the second lambda function, which accesses the intermediate S3 bucket directory to locate the cached JSON file using the previously generated job ID. The text parsing lambda function then extracts the text from the JSON file created during the intermediate step, and saves it as a CSV file in the output S3 bucket.
  
  After which the folder containing the CSV will be mounted on the EC2 instance. Once this is done the '**Embedder Code**', a python file deployed in the EC2 will continuously monitor the csv folder for any new csv files

what happens inside the embedder file is meticulously defined below

embedder file is a Python script that monitors a folder for text files, processes the files, generates embeddings for the text using the OpenAI API, and saves the results in a pandas DataFrame. Here's a breakdown of the script:

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
  
## Usage

Explain how to use your project or application. Provide instructions, code samples, or examples to help users understand how to interact with the project. You can also include screenshots or GIFs to demonstrate functionality.

## Configuration

If your project requires configuration files or settings, explain how to set them up. Include information about environment variables, configuration options, or any other necessary configurations.

## Contributing

If you want others to contribute to your project, provide guidelines for how they can do so. Include information about submitting bug reports, feature requests, or pull requests. Specify any coding standards, conventions, or guidelines that contributors should follow.

## Credits

Acknowledge and give credit to any individuals, organizations, or resources that have contributed to your project. This can include libraries, frameworks, or tutorials that you used.

## License

Specify the license under which your project is distributed. Include any disclaimers or limitations of liability if applicable.

## Support

Provide information on how users can seek support for your project. Include contact details, links to documentation, or community forums where users can find help.

## Frequently Asked Questions (FAQ)

If there are common questions or concerns about your project, address them in this section. Provide clear and concise answers to help users resolve common issues.

## Changelog

If your project has multiple versions or releases, include a changelog that outlines the changes, bug fixes, and new features in each version.

## Roadmap

If you have plans for future development or enhancements, share them in this section. Provide an overview of upcoming features or improvements you plan to implement.

## Acknowledgments

Express gratitude to individuals or organizations that have supported or influenced your project. This can include mentors, colleagues, or open-source communities.

## Appendix

Include any additional information, references, or resources that might be useful to readers. This can include links to related documentation, tutorials, or examples.

Remember that the above structure is just a suggested format, and you can adapt it to fit the specific needs of your project. The goal is to provide clear and relevant information that helps users understand and engage with your project effectively.
