import requests, os

class BlazegraphClient:
    def __init__(self, endpoint):
        self.endpoint = endpoint

    def create_namespace(self, namespace_name):
        url = f'{self.endpoint}/namespace'
        xml_data = f"""<?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">
        <properties>
        <entry key="com.bigdata.rdf.sail.namespace">{namespace_name}</entry>
        </properties>"""
        try:
            response = requests.post(url, data=xml_data, headers={'Content-Type': 'application/xml'})
            response.raise_for_status()  
            return response.text  
        except requests.RequestException as e:
            print(f"Error creating namespace: {e}")
            return None
    
    def query_data(self, namespace_name, query):
        url = f'{self.endpoint}/namespace/{namespace_name}/sparql'
        params = {'query': query}
        headers = {'Accept': 'application/json'}
        
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()  # Raise HTTPError for bad responses
            return response.json()
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            raise
