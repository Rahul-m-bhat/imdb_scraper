import requests
from bs4 import BeautifulSoup
from .models import MovieDB
from imdb import IMDb
import re
import asyncio
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

ia = IMDb()


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.61 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.imdb.com/",
}


def fetcg_movie_text(movie_url):
    """This Function is responsible to hit and return response from the IMDB url"""
    try:
        response = requests.get(movie_url, headers=HEADERS)
        response.raise_for_status()
        
        if response.status_code in (200, 201, 202):
            logging.info(f"Successfully fetched with status code {response.status_code}: {movie_url}")
            return response
        else:
            logging.warning(f"Unexpected status code {response.status_code} for {movie_url}")
            return None
    
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching {movie_url}: {e}")
        return None


def get_movie_details(imdb_url):

    match = re.search(r'/title/(tt\d+)/', imdb_url)
    if match:
        imdb_id = match.group(1)

    try:
        movie = ia.get_movie(imdb_id[2:])

        if not movie:
            logging.warning(f"Movie not found for IMDb ID: {imdb_id}")

        movie_data = {
            'title': movie.get('title', None),
            'release_year': movie.get('year', None),
            'imdb_rating': movie.get('rating', None),
            'directors': ', '.join([d['name'] for d in movie.get('directors', [])]),
            'cast': ', '.join([a['name'] for a in movie.get('cast', [])[:10]]),
            'plot_summary': movie.get('plot'),
            'imdb_url': imdb_url
        }

    except Exception as e:
        logging.error(f"Error fetching using imdb_id @get_movie_details for url {imdb_url}: {e}")
        movie_data = None

    logging.info(f"Successfully retrieved details for movie: {movie_data.get('title')}")
    return movie_data


async def fetch_all_movie_details(movie_urls):
    tasks = [get_movie_details_nonblocking(url) for url in movie_urls]
    return await asyncio.gather(*tasks)
    

async def get_movie_details_nonblocking(imdb_url):
    return await asyncio.to_thread(get_movie_details, imdb_url)


def scrape_imdb_search_results(keyword, num_pages=1):
    """
    Scrapes movie information from IMDb search results for a given keyword,
    handling pagination.
    """
    base_search_url = "https://www.imdb.com/find/?q="
    movie_urls = []
    all_movie_details = []

    for page_num in range(num_pages):
        start_param = page_num * 50 + 1
        search_url = f"{base_search_url}{keyword}&ref_=nv_sr_sm&s=tt&start={start_param}"
        
        logging.info(f"Scraping search page: {search_url}")

        try:
            response = requests.get(search_url, headers=HEADERS)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error while Scraping search page: {search_url} with exception: {e}")
            break

        soup = BeautifulSoup(response.text, 'html.parser')

        movie_list_items = soup.find_all('li', class_='ipc-metadata-list-summary-item')

        for item in movie_list_items:
            link_tag = item.find('a', class_='ipc-metadata-list-summary-item__t')
            if link_tag and 'title' in link_tag.get('href', ''):
                relative_url = link_tag['href']
                full_url = f"https://www.imdb.com{relative_url.split('?')[0]}"
                movie_urls.append(full_url)

        next_page_link = soup.find('a', class_='ipc-btn ipc-btn--full-width ipc-btn--baseAlt ipc-btn--onInverse ipc-btn--single-padding ipc-btn--default-height ipc-btn--hover-border-light ipc-btn--button ipc-btn--text ipc-skip-link-button', text='Next Page')
        
        if not next_page_link and page_num < num_pages - 1:
            logging.info("No explicit 'Next Page' link found, continuing based on num_pages parameter.")
        elif not next_page_link and page_num == num_pages - 1:
            logging.info("Last page or no more pages found.")
            break
        
    all_movie_details = asyncio.run(fetch_all_movie_details(movie_urls))
    return all_movie_details


def save_movie_data(movie_details_list):
    """
    Saves scraped movie data to the Django database.
    """
    for movie_data in movie_details_list:
        try:
            movie, created = MovieDB.objects.update_or_create(
                imdb_url=movie_data['imdb_url'],
                defaults={
                    'title': movie_data.get('title'),
                    'release_year': movie_data.get('release_year', None),
                    'imdb_rating': movie_data.get('imdb_rating', None),
                    'directors': movie_data.get('directors', None),
                    'cast': movie_data.get('cast', None),
                    'plot_summary': movie_data.get('plot_summary', None)
                }
            )
            if created:
                logging.info(f"Added new movie: {movie.title}")
            else:
                logging.info(f"Updated existing movie: {movie.title}")
        except Exception as e:
            logging.error(f"Error saving movie data for {movie_data.get('title', 'N/A')}: {e}")

    