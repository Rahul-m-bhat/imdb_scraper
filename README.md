# IMDb Movie Scraper API

This project is a Django REST Framework (DRF) API that allows you to scrape movies from IMDb based on a keyword with No of Pages, 
save them to a database, and retrieve them with pagination.

---

## Setup Instructions

1. **Clone the repository:**
   ```bash
   https://github.com/Rahul-m-bhat/imdb_scraper.git
   cd yourproject


## Create and activate virtual environment
    python -m venv venv
    source venv/bin/activate

## Requrements Installation
    pip install -r requirements.txt

## Running Migrations
    python manage.py migrate

## Starting Django Server
    python manage.py runserver

## API Endpoints
   
   
## POST /api/movies/scrape_movies/

      curl --location 'http://127.0.0.1:8000/api/movies/scrape_movies/' \
      --header 'Content-Type: application/json' \
      --header 'Cookie: csrftoken=g4sluwitTTTNaojPMAkjPpMSUtrfgsMX' \
      --data '{
          "keyword": "comedy",
          "pages" : 5
      }'

## GET /api/movies/get_movies/?page=1&page_size=1

      curl --location 'http://127.0.0.1:8000/api/movies/get_movies/?page=1&page_size=10' \
      --header 'Cookie: csrftoken=g4sluwitTTTNaojPMAkjPpMSUtrfgsMX'

## Running Test cases
    python manage.py test

## Additional 

    "Django commands to scrape the movies data from imdb"

    python manage.py {keyword} --pages {no of pages to scrape}
