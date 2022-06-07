import requests
from pprint import pprint

'''
Example:
    https://api.themoviedb.org/3/trending/tv/week?api_key=3ad6ff4112660691295eb3c33dba950c
'''

'''
Query structure
    movie id
    title
    original title
    image link

'''

class InformationConfiguration:
    ID: str = 'id'
    TITLE: str = 'title'
    ORIGINAL_TITLE: str = 'original_title'
    POSTER_PATH: str = 'poster_path'
    
    ORIGINAL_LANGUAGE: str = 'original_language'
    BACKDROP_PATH: str = 'backdrop_path'
    RELEASE_DATE: str = 'release_date'

class API:
    BASE_URL = 'https://api.themoviedb.org/3'
    KEY = '3ad6ff4112660691295eb3c33dba950c'
    
    IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500'


class Response(API, InformationConfiguration):
        
    def get_top_rated_movies(self):
        data_to_return = []
        
        response = requests.get(f'https://api.themoviedb.org/3/movie/top_rated?api_key={self.KEY}')
        data = response.json()['results']
        for i in data:
            data_to_return.append((i[self.ID], i[self.TITLE], i[self.ORIGINAL_TITLE], self.IMAGE_BASE_URL + i[self.POSTER_PATH])) 

        return data_to_return
    
    def get_popular_movies(self):
        data_to_return = []
        
        response = requests.get(f'https://api.themoviedb.org/3/movie/popular?api_key={self.KEY}')
        data = response.json()['results']
        for i in data:
            data_to_return.append((i[self.ID], i[self.TITLE], i[self.ORIGINAL_TITLE], self.IMAGE_BASE_URL + i[self.POSTER_PATH])) 

        return data_to_return
    
    
    def get_upcoming_movies(self):
        data_to_return = []
        
        response = requests.get(f'https://api.themoviedb.org/3/movie/upcoming?api_key={self.KEY}')
        data = response.json()['results']
        for i in data:
            data_to_return.append((i[self.ID], i[self.TITLE], i[self.ORIGINAL_TITLE], self.IMAGE_BASE_URL + i[self.POSTER_PATH])) 

        return data_to_return
    
    
    def get_trailer_by_id(self, movie_id: int):
        keys = []
        
        response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={self.KEY}')
        data = response.json()['results']
        for i in data:
            keys.append(i['key'])
        return f"https://www.youtube.com/watch?v={keys[0]}"
    
    def get_movie_details_by_id(self, movie_id: int):
        """
        Return structure -> list of
            (poster_url, title, release_date, duration, imdb, overview)
        """
        ORIGINAL_TITLE: str = 'original_title'
        RELEASE_DATE: str = 'release_date'
        RUNTIME: str = 'runtime'
        VOTE_AVERAGE = 'vote_average'
        OVERVIEW: str = 'overview'
        
        
        data_to_return = []
        
        response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={self.KEY}')
        data = response.json()
        data_to_return.append((self.IMAGE_BASE_URL + data[self.POSTER_PATH], data[ORIGINAL_TITLE], data[RELEASE_DATE], data[RUNTIME], data[VOTE_AVERAGE],data[OVERVIEW]))
        return data_to_return
        
# 123

if __name__ == '__main__':
    r = Response()
    a = r.get_top_rated_movies()
    print(r.get_movie_details_by_id(a[0][0]))
# print(a[0][0])
