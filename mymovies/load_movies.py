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
    m = r.json()

    conn = psycopg2.connect("dbname=django_bootstrap user=ubuntu password=sobrado18")
    cur = conn.cursor()

    sql = 'SELECT * FROM movies_movie WHERE title = %s'
    cur.execute(sql, (m['title'],))
    movie_exists = cur.fetchall()

    print(movie_exists)

    r = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}/credits?language=en-US', headers=headers) 
    credits = r.json()

    actors = [( actor['name'], actor['known_for_department'], actor['profile_path']) for actor in credits['cast'][:10]] 
    crew =   [(   job['name'], job['job'], job['profile_path']) for job in credits['crew'][:15]]

    credits_list = actors + crew

    jobs = [job for name, job,profile in credits_list]
    jobs = set(jobs)

    sql = 'SELECT * FROM movies_job WHERE name IN %s'
    cur.execute(sql, (tuple(jobs),))
    jobs_in_db = cur.fetchall()

    jobs_to_create = [(name,) for name in  jobs if name not in [name for id, name,profile, in jobs_in_db]]
    sql = 'INSERT INTO movies_job (name) values  (%s)'
    cur.executemany(sql, jobs_to_create) 

    persons = [(person,job,profile) for person, job, profile, in credits_list]
    persons_ids = [person for person,job, profile in persons]
    persons_ids = set(persons_ids)
    
    sql = 'SELECT * FROM movies_person WHERE name IN %s'
    cur.execute(sql, (tuple(persons_ids),))
    persons_in_db = cur.fetchall()

    persons_to_create = ([(name,poster_path) for name,job,poster_path in persons if (name,job,poster_path) not in [(name,job,poster_path) for id, name, poster_path in persons_in_db]])
    print(persons_to_create)
    sql = 'INSERT INTO movies_person (name, poster_path) values  (%s, %s)'
    cur.executemany(sql, persons_to_create) 


    genres = [d['name']  for  d in m['genres']] 

    sql = 'SELECT * FROM movies_genre WHERE name IN %s'
    cur.execute(sql, (tuple(genres),))
    genres_in_db = cur.fetchall()

    genres_to_create = [(name,) for name in  genres if name not in [name for id, name in genres_in_db]]

    sql = 'INSERT INTO movies_genre (name) values  (%s)'
    cur.executemany(sql, genres_to_create) 



    date_obj = date.fromisoformat(m['release_date']) 
    date_time = datetime.combine(date_obj, datetime.min.time())

    sql = '''INSERT INTO movies_movie 
             (title,
              overview,
              release_date,
              running_time,
              budget,
              tmdb_id,
              revenue,
              poster_path) values  (%s, %s, %s, %s, %s, %s, %s, %s);'''

    movie_tuple = (m['title'], m['overview'], date_time.astimezone(timezone.utc), m['runtime'], 
                   m['budget'] , movie_id, m['revenue'], m['poster_path'] )


    sql = '''INSERT INTO movies_movie 
             (title,
              overview,
              release_date,
              running_time,
              budget,
              tmdb_id,
              revenue,
              poster_path) values  (%s, %s, %s, %s, %s, %s, %s, %s);'''

    movie_tuple = (m['title'], m['overview'], date_time.astimezone(timezone.utc), m['runtime'], 
                   m['budget'] , movie_id, m['revenue'], m['poster_path'] )
    cur.execute(sql, movie_tuple)

     
    sql = '''INSERT INTO movies_movie_genres (movie_id, genre_id)
             SELECT (SELECT id FROM movies_movie WHERE title = %s) as movie_id, id as genre_id 
             FROM movies_genre 
             WHERE name IN %s'''
    cur.execute(sql, (m['title'], tuple(genres),))

    
    for p in persons:
        print((p[0],p[1],m['title']))
        sql = '''INSERT INTO movies_moviecredit (movie_id,person_id, job_id)
                 SELECT id as movie_id,
                 (SELECT id FROM movies_person WHERE name = %s LIMIT 1)  as person_id ,
                 (SELECT id FROM movies_job WHERE name = %s LIMIT 1)  as job_id 
                 FROM movies_movie
                 WHERE title = %s'''
        print((p[0],p[1],m['title']))
        cur.execute(sql, (p[0],p[1],m['title']),)
        print((p[0],p[1],m['title']))

    conn.commit()

if __name__ == "__main__":
    add_movie(int(sys.argv[1]))