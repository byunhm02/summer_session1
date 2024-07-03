from django.db import models
from members.models import Member
from items.models import Item

# Create your models here.

class Order(models.Model):
    order_date=models.DateTimeField(auto_now_add=True) #주문 날짜
    status=models.CharField(max_length=50) #주문 상태
    member=models.ForeignKey(Member,on_delete=models.CASCADE) #회원아이디
    item=models.ManyToManyField(Item,through='Order_item') #상품 아이디
    
    class Meta:
        db_table='orders'
       
#중간테이블 
class Order_item(models.Model):
    count=models.IntegerField() #해당 상품 몇개 주문했는지
    order=models.ForeignKey(Order,on_delete=models.CASCADE) #주문 아이디 
    item=models.ForeignKey(Item,on_delete=models.CASCADE) #상품 아이디
    
    class Meta:
        db_table='order_item'