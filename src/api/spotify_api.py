import base64
import requests
from dotenv import load_dotenv
import os
import json

def get_token():
    auth_string = CLIENT_ID + ":" + CLIENT_SECRET
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = 'https://accounts.spotify.com/api/token'
    headers={"Authorization": f"Basic {auth_base64}",
             "Content-Type":"application/x-www-form-urlencoded"}
    data={"grant_type" : "client_credentials"}

    response = requests.request('POST', url=url, headers=headers,data=data)

    return response.json()["access_token"]

def get_auth_header(token):
    return {'Authorization': "Bearer " + token}

def get_artist(token, artista):

    url=f'https://api.spotify.com/v1/search'
    headers= get_auth_header(token)
    query  = f"q={artista}&type=artist&limit=1"

    query_url= url + "?" + query
    response = requests.request('GET', url=query_url, headers=headers)
    data = response.json()

    return data

if __name__ == "__main__":

    load_dotenv()

    CLIENT_ID=os.getenv('CLIENT_ID')
    CLIENT_SECRET=os.getenv('CLIENT_SECRET')

    acc_token=get_token()
    auth_header = get_auth_header(acc_token)

    nome_artista= input('Informe o nome do artista: ')
    artista = get_artist(acc_token, nome_artista)

    print(artista)
    

    


