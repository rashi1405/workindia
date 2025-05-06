from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

class Map(models.Model):
    name = models.CharField(max_length=100, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    layout = models.JSONField()  # Stores 2D list of 'R' and '#' as JSON
    public = models.BooleanField(default=False)

    def __str__(self):
        return self.name
