from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.


class User(AbstractUser):
    school = models.CharField(max_length=255, blank=True)
    user_class = models.CharField(max_length=10, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    image = models.ImageField(upload_to='profile_images/', default='profile_images/default.jpg', blank=True)
    birth_date = models.DateField(null=True, blank=True)
    rating = models.DecimalField(default=0.0, decimal_places=2, max_digits=5,
                                 validators=[MinValueValidator(0), MaxValueValidator(100)])
