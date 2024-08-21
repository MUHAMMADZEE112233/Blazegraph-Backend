import os
import requests, json
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .blazegraph_client import BlazegraphClient

blazegraph_endpoint = settings.BLAZEGRAPH_ENDPOINT
client = BlazegraphClient(blazegraph_endpoint)

@csrf_exempt
def create_database(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            namespace_name = data.get('namespace_name')
        except json.JSONDecodeError:
            return JsonResponse({'status': 'Failed', 'error': 'Invalid JSON data'}, status=400)
        if not namespace_name:
            return JsonResponse({'status': 'Failed', 'error': 'Namespace name is required'}, status=400)
        response = client.create_namespace(namespace_name)
        if response:
            return JsonResponse({'status': 'Success', 'data': {'response': response}})
        else:
            return JsonResponse({'status': 'Failed', 'error': 'Error creating namespace'}, status=500)
    else:
        return JsonResponse({'status': 'Failed', 'error': 'Only POST method allowed'}, status=405)

@csrf_exempt
def upload_data(request):
    if request.method == 'POST':
        namespace = request.POST.get('namespace')
        ttl_file = request.FILES.get('ttl_file')
        
        if not namespace or not ttl_file:
            return JsonResponse({'status': 'Failed', 'error': 'Namespace and file are required'}, status=400)

        try:
            file_content = ttl_file.read()
            url = f'{blazegraph_endpoint}/namespace/{namespace}/sparql'
            headers = {'Content-Type': 'text/turtle'}
            response = requests.post(url, data=file_content, headers=headers)
            response.raise_for_status()
            return JsonResponse({'status': 'Success', 'message': 'File uploaded successfully'})
        except requests.RequestException as e:
            return JsonResponse({'status': 'Failed', 'error': str(e)}, status=500)
    
    return JsonResponse({'status': 'Failed', 'error': 'Only POST method allowed'}, status=405)

def display_data(request):
    if request.method == 'GET':
        namespace = request.GET.get('namespace')
        query = request.GET.get('query', 'SELECT ?s ?p ?o WHERE { ?s ?p ?o } LIMIT 10')
        
        if not namespace:
            return JsonResponse({'status': 'Failed', 'error': 'Namespace is required'}, status=400)
        try:
            response = client.query_data(namespace, query)
            return JsonResponse({'status': 'Success', 'data': response})
        except Exception as e:
            print(f"Error in display_data view: {e}")
            return JsonResponse({'status': 'Failed', 'error': str(e)}, status=500)
    
    return JsonResponse({'status': 'Failed', 'error': 'Only GET method allowed'}, status=405)

def home(request):
    return HttpResponse("Welcome to the Blazegraph Django App. Use /create-database/, /upload-data/, or /display-data/ endpoints.")