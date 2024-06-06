## SETUP:

### Create python environment(optional):  
python3 -m venv .env  
activate:  
source .env/bin/activate  

### Install library to connect to google drive  
'''pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib'''  
then install other libraries  
'''pip install -r requirements.txt'''  

### Setup for google drive API  
go to google cloud API and service  
select or create a project  
setup OAuth 2.0 Client ID for google drive API  
download the json api key, create a credentials.json and copy the content over  




## Useage:
python3 main.py [number_of_search_results (default = 500)]  
