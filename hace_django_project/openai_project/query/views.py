from django.http import HttpResponse, JsonResponse, FileResponse, Http404, response
from openai_project.settings import BASE_DIR, MEDIA_ROOT
from rest_framework.decorators import api_view
from django.shortcuts import render
from django.core.files import File
from django.conf import settings
from . import cosine_smilarity
import pandas as pd
import os
import json

df_similarities = pd.read_pickle("C:/Users/44744/Desktop/embedded.pickle")

# Create your views here.
def sem_search(request):
    query = request.GET.get('q')
    pdf_files = os.listdir(settings.MEDIA_ROOT)
    pdf_files = [f for f in pdf_files if f.endswith('.pdf')]
    if query is not None:
        # TODO: Implement query handling logic
        res = cosine_smilarity.search_docs(df_similarities, query, top_n=20)
        res['url'] = res['filename'].apply(lambda x: x+'.pdf')
        res.reset_index(drop=True, inplace=True)
        
        files = []
        i = 0
        for filename in res.url:
            if  filename in pdf_files:
                content = (res['Text'][i])
                page = res['PageNo'][i]
                # print('*'*20)
                file_path = os.path.join(settings.MEDIA_ROOT, filename)
                view_url = request.build_absolute_uri(settings.MEDIA_URL + filename)
                download_url = request.build_absolute_uri('/download/' + filename)
                files.append({"filename": filename,"text": content, "view_url": view_url,\
                               "download_url": download_url, "page" : page})
                i+=1
    response1 = HttpResponse(json.dumps(files));
    return response1
            
def pdf_list(request):
    # get a list of PDF files in the media folder
    pdf_files = os.listdir(settings.MEDIA_ROOT)
    pdf_files = [f for f in pdf_files if f.endswith('.pdf')]
    
    # create a list of file metadata with URLs for viewing and downloading
    files = []
    for filename in pdf_files:
        file_path = os.path.join(settings.MEDIA_ROOT, filename)
        view_url = request.build_absolute_uri(settings.MEDIA_URL + filename)
        download_url = request.build_absolute_uri('/download/' + filename)
        files.append({'filename': filename, 'view_url': view_url, 'download_url': download_url})
    
    # render the template with the list of files
    context = {'files': files}
    return render(request, 'pdf_list.html', context)

def download(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    if os.path.exists(file_path):
        # use Django's built-in FileResponse to allow users to view or download the file
        response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=' + filename
        return response
    else:
        raise Http404
    
def ask_hace(request):
    if request.method == 'GET':
        query = request.GET.get('q', '')
        response_text = cosine_smilarity.davinci(query)
        return HttpResponse(response_text)
    else:
        return HttpResponse("Invalid request method")
    

    