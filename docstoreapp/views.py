from pydoc_data.topics import topics
import shutil
from unicodedata import name
from urllib import request
from django.shortcuts import render
from .serializers import DocumentsSerializer,TopicsSerializer,FolderSerializer
from .models import Documents,Topics,Folder
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
import sys,os
from .utils import supermakedirs
from docstoreapi.settings import MEDIA_URL
import time
class AddTopics(generics.CreateAPIView):
    queryset = Topics.objects.all(),
    serializer_class = TopicsSerializer


class AddFolder(generics.CreateAPIView):
    queryset = Folder.objects.all(),
    serializer_class = FolderSerializer

    # def post(self, request, *args, **kwargs):
        
    #     return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        path_ = serializer.validated_data.get('path')
        path_ = os.path.join(MEDIA_URL, path_)
        print(path_)
        if not os.path.exists(path_):
            os.mkdir(path_)
            serializer.save()
        else:
            return Response('Folder Already Exists!')



class AddDocument(generics.CreateAPIView):
    queryset = Documents.objects.all(),
    serializer_class = DocumentsSerializer

    # def post(self, request, *args, **kwargs):
    #     print(request.FILES)


    def perform_create(self, serializer):
        folder = str(serializer.validated_data.get('folder').path)
        # folder_path = str(serializer.validated_data.get('folder').path)
        # serializer.validated_data['doc'] = folder_path + '/' + serializer.validated_data['doc']
        # filename = str(serializer.validated_data.get('doc'))
        # print('FileName',str(filename))
        serializer.save()
        # shutil.move(MEDIA_URL+filename,MEDIA_URL+folder+'/'+filename)



# class PurchaseList(generics.ListAPIView):
#     serializer_class = PurchaseSerializer




class GetDocument(generics.ListAPIView):
    queryset = Documents.objects.all()
    serializer_class = DocumentsSerializer

    def get_queryset(self):
        folder_name = self.request.query_params.get('folder_name')
        topic_name = self.request.query_params.get('topic')
        print(folder_name,topic_name)
        query_folder = Folder.objects.filter(path = folder_name).first()
        topic_query = Topics.objects.filter(short_des = topic_name).first()
        if folder_name == None and topic_name == None:
            return Documents.objects.all()
        if folder_name != None and topic_name == None:
            return Documents.objects.filter(folder_id=str(query_folder.folder_id), topics = topic_query)
        if folder_name != None :
            return Documents.objects.filter(folder_id=str(query_folder.folder_id))
        if topic_name != None :
            return Documents.objects.filter(topics=topic_query)


