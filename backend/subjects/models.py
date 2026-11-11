from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    semester = models.IntegerField()

    branch = models.CharField(max_length=50)
    regulation = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} ({self.code})"