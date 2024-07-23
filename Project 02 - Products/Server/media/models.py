from django.db import models


# Create your models here.
class Media(models.Model):
    """
        DB Model for Media table to store basic information
    """
    show_name = models.CharField(max_length=255)
    show_desc = models.CharField(max_length=512)
    date_of_completion = models.DateField(auto_now_add=True)
    is_series = models.BooleanField(default=False)
    is_anime = models.BooleanField(default=True)

    def __str__(self):
        return self.show_name
