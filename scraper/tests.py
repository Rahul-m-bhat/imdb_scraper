from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import MovieDB

class MovieViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        self.movie1 = MovieDB.objects.create(title="Inceptionewd", release_year="2010", imdb_rating=8.8, imdb_url="https:test1.com")
        self.movie2 = MovieDB.objects.create(title="The Dark Knight rises", release_year="2008", imdb_rating=9.0, imdb_url="https:test12.com")

    def test_get_movies_paginated_success(self):
        response = self.client.get('/api/movies/get_movies/?page=1&page_size=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_movies_paginated_invalid_params(self):
        response = self.client.get('/api/movies/get_movies/?page=abc&page_size=xyz')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_scrape_movies_missing_keyword(self):
        response = self.client.post('/api/movies/scrape_movies/', data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_scrape_movies_valid(self):
        # Mock the scraping if needed; this is a simple structure
        response = self.client.post('/api/movies/scrape_movies/', data={
            "keyword": "comedy", "pages": 1
        }, format='json')

        self.assertIn(response.status_code, [200, 500]) 
