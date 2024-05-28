## SETUP:

create python environment(optional):  
python3 -m venv .env  
activate:  
source .env/bin/activate  

install library to connect to google drive  
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib  
then install other libraries  
pip install -r requirements.txt  

## Useage:
python3 main.py [number_of_search_results (default = 500)]  
