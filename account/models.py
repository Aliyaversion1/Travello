from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=65)
    last_name = models.CharField(max_length=65)
    image = models.ImageField(upload_to='users_photo')

    def __str__(self):
        return self.get_full_name()



