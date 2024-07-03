from rest_framework import serializers
from items.models import Item


class ItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Item
        fields=['id','item_name','stock_quantity','item_price']
        
    def create(self, validated_data):
        # 이미 존재하는지 확인
        existing_item = Item.objects.filter(item_name=validated_data['item_name']).first()
        if existing_item:
            raise serializers.ValidationError("Item with this name already exists.")
        
        # 존재하지 않는 경우 상품 생성
        item = Item.objects.create(**validated_data)
        
        return item
