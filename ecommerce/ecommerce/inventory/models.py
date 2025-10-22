from django.db import models
from res.models import BaseModel
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

    def __str__(self):
        return f"{self.product.name} - {self.file.name}"