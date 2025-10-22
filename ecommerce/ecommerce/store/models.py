from django.db import models
from res.models import BaseModel,CustomUser

# Create your models here.

class Store(BaseModel):
    name = models.CharField(max_length=255)
    tel = models.CharField(max_length=20)
    owner = models.ForeignKey('res.CustomUser', on_delete=models.CASCADE)
    address = models.TextField()
    avatar = models.ImageField(upload_to='store_avatars/', null=True, blank=True)
    

    def __str__(self):
        return self.name