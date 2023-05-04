from django.contrib import admin
from django.urls import path, include
from .views import pdf_list, sem_search, download, ask_hace
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('search/',sem_search, name='search'),
    path('ask_hace/',ask_hace, name='ask_hace'),
    path('pdfs/', pdf_list, name='pdf_list'),
    path('download/<str:filename>/', download, name='download'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

        