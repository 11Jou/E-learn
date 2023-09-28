from django.db import models

class Message(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    message = models.TextField(max_length=500)

    def __str__(self) -> str:
        return self.name