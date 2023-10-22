import os
import environ
import requests
import psycopg2
from  datetime import datetime, date, timezone 
import sys

def add_movie(movie_id):
    env = environ.Env()
    environ.Env.read_env('.env')
    print('API_KEY: ', env('API_KEY'))
    print('API_TOKEN: ', env('API_TOKEN'))

    '''
    url --request GET \
         --url 'https://api.themoviedb.org/3/movie/76341?language=en-US' \
         --header 'Authorization: Aasdfqwer' \
         --header 'accept: application/json'
    '''
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {env('API_TOKEN')}"}
    
    r = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?language=en-US', headers=headers) 
    print(r.json())

if __name__ == "__main__":
    add_movie(int(sys.argv[1]))