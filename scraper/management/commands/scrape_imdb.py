from django.core.management.base import BaseCommand
from scraper.scraper_helper import scrape_imdb_search_results, save_movie_data

class Command(BaseCommand):
    help = 'Scrapes movie information from IMDb for a given keyword and stores it in the database.'

    def add_arguments(self, parser):
        parser.add_argument('keyword', type=str, help='The keyword or genre to search for on IMDb.')
        parser.add_argument('--pages', type=int, default=1, help='Number of search result pages to scrape (default: 1).')

    def handle(self, *args, **options):
        keyword = options['keyword']
        num_pages = options['pages']

        self.stdout.write(f"Starting IMDb scraping for keyword: '{keyword}' across {num_pages} page(s)...")

        try:
            scraped_data = scrape_imdb_search_results(keyword, num_pages)
            if scraped_data:
                self.stdout.write(f"Scraped {len(scraped_data)} movies. Saving to database...")
                save_movie_data(scraped_data)
                self.stdout.write(self.style.SUCCESS(f"Successfully scraped and saved {len(scraped_data)} movies for '{keyword}'."))
            else:
                self.stdout.write(self.style.WARNING(f"No movies found for '{keyword}' or an error occurred during scraping."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An unexpected error occurred: {e}"))