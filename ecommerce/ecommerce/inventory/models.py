from django.db import models
from res.models import BaseModel
from mimetypes import guess_type

# Create your models here.
class Product(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    store = models.ForeignKey('store.Store', on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name

class ProductFile(models.Model): 
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='product_files/') 

    def save(self, *args, **kwargs):
        mime_type, _ = guess_type(self.file.name)
        if mime_type:
            if mime_type.startswith('image'):
                self.file_type = 'image'
            elif mime_type.startswith('video'):
                self.file_type = 'video'
            else:
                self.file_type = 'other'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.file.name}"