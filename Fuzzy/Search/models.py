from django.db import models

# Create your models here.

# Dataset model will contain all the 3,33,333 records.


class Dataset(models.Model):
    word = models.CharField(max_length=100000)
    count = models.CharField(max_length=100000000000000)

    def __str__(self):
        return self.word
