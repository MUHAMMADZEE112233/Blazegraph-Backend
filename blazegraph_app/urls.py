from django.urls import path
from .views import  create_database, upload_data, display_data, home

urlpatterns = [
    path('', home, name='home'),

    path('create-database/', create_database, name='create_database'),

    path('upload-data/', upload_data, name='upload_data'),

    path('display-data/', display_data, name='display_data'),
]