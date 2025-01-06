from django.db import models

# Create your models here.
class Recipe(models.Model):
    name = models.CharField(max_length=255)
    image = models.URLField()
    healthLabels = models.TextField()
    cuisineType = models.TextField()
    calories = models.FloatField()
    totalNutrients = models.JSONField()
    ingredients = models.TextField()
    def __str__(self):
        return self.name
