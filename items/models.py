from django.db import models

# Create your models here.
class Item(models.Model):
    item_name=models.CharField(max_length=50)
    stock_quantity=models.IntegerField()
    item_price=models.IntegerField()
    
    
    class Meta:
        db_table='item'
        
