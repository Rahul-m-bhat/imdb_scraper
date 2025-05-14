# from rest_framework import viewsets
# from .models import MovieDB
# from .serializers import MovieSerializer

# class MovieViewSet(viewsets.ModelViewSet):
#     queryset = MovieDB.objects.all().order_by('title') # Order by title for consistency
#     serializer_class = MovieSerializer


from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import MovieDB
from .serializers import MovieSerializer
import logging
from scraper.scraper_helper import scrape_imdb_search_results, save_movie_data  # Import the scraper functions

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MovieViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows movies to be viewed and edited.
    """
    queryset = MovieDB.objects.all().order_by('title')  # Order by title for consistency
    serializer_class = MovieSerializer

    def list(self, request, *args, **kwargs):
        """
        Override the list method to handle pagination.
        """
        page = self.paginate_queryset(self.queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def get_movies(self, request):
        """
        Custom action to retrieve movies with pagination.
        """
        try:
            page_size = int(request.query_params.get('page_size', 10))  # Default page size is 10
            page = int(request.query_params.get('page', 1))  # Default page number is 1
            
            # Calculate start and end index for slicing the queryset
            start_index = (page - 1) * page_size
            end_index = page * page_size
            
            movies = MovieDB.objects.all().order_by('title')[start_index:end_index]
            serializer = self.get_serializer(movies, many=True)
            
            # Calculate total number of movies for pagination metadata
            total_movies = MovieDB.objects.count()
            
            response_data = {
                'total_movies': total_movies,
                'page': page,
                'page_size': page_size,
                'results': serializer.data,
            }
            
            logging.info(f"Successfully retrieved movies with pagination: Page {page}, Page Size {page_size}")
            return Response(response_data, status=status.HTTP_200_OK)
        
        except ValueError:
            logging.error("Invalid page or page_size value provided.")
            return Response({'error': 'Invalid page or page_size value. Must be an integer.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logging.error(f"Error retrieving movies with pagination: {e}")
            return Response({'error': f'Failed to retrieve movies: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_SERVER_ERROR)


    @action(detail=False, methods=['post'])
    def scrape_movies(self, request):
        """
        API endpoint to trigger the scraping of movie data from IMDb.
        """
        keyword = request.data.get('keyword')
        num_pages = request.data.get('pages', 1)  # Default to 1 page if not provided

        if not keyword:
            logging.error("Keyword not provided for scraping.")
            return Response({'error': 'Keyword is required for scraping.'}, status=status.HTTP_400_BAD_REQUEST)

        logging.info(f"Starting IMDb scraping for keyword: '{keyword}' across {num_pages} page(s)...")

        try:
            scraped_data = scrape_imdb_search_results(keyword, num_pages)
            if scraped_data:
                logging.info(f"Scraped {len(scraped_data)} movies. Saving to database...")
                save_movie_data(scraped_data)
                logging.info(f"Successfully scraped and saved {len(scraped_data)} movies for '{keyword}'.")
                return Response({'message': f"Successfully scraped and saved {len(scraped_data)} movies for '{keyword}'."}, status=status.HTTP_200_OK)
            else:
                logging.warning(f"No movies found for '{keyword}' or an error occurred during scraping.")
                return Response({'message': f"No movies found for '{keyword}' or an error occurred during scraping."}, status=status.HTTP_200_OK)  # Return 200 OK with a message
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            return Response({'error': f"An unexpected error occurred: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
