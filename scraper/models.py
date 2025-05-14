from django.db import models

class MovieDB(models.Model):
    title = models.CharField(max_length=255)
    release_year = models.CharField(max_length = 10,null=True, blank=True)
    imdb_rating = models.FloatField(null= True, blank=True)
    directors = models.CharField(max_length=500, null=True, blank=True)
    cast = models.TextField(null=True, blank=True)
    plot_summary = models.TextField(null=True, blank=True)
    imdb_url = models.URLField(max_length=500, unique=True, null=False)

    def __str__(self):
        return f"Movie Title : {self.title}, Movie IMDB Url : {self.imdb_url}"
    
    class Meta:
        verbose_name_plural = "Movies"