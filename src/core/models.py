from django.db import models

# Create your models here.


class BaseModel(models.Model):
    class Meta:
        abstract = True

    create_date = models.DateTimeField(null=True, auto_now_add=True)
    write_date = models.DateTimeField(null=True, auto_now=True)
