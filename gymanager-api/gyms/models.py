from django.db import models


class Gym(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    reference = models.CharField(max_length=255)

    def __str__(self):
        return self.name
