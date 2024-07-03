from rest_framework import serializers
from orders.models import Order,Order_item
from items.models import Item
from members.models import Member




# 주문 요청시 item 관련 속성
class OrderItemRequestSerializer(serializers.Serializer):
    item_id = serializers.IntegerField()
    count = serializers.IntegerField()

# 주문 등록 요청
class OrderRequestSerializer(serializers.Serializer):
    member_id = serializers.IntegerField()
    status = serializers.CharField(max_length=50)
    items = OrderItemRequestSerializer(many=True)

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        member_id = validated_data.pop('member_id')
        member = Member.objects.get(id=member_id)
        order = Order.objects.create(member=member, **validated_data)

        for item_data in items_data:
            item = Item.objects.get(id=item_data['item_id'])
            Order_item.objects.create(order=order, item=item, count=item_data['count'])

        return order

# 주문 등록 응답 중 item 관련 객체
class OrderItemSerializer(serializers.ModelSerializer):
    item_id = serializers.IntegerField(source='item.id')
    item_name = serializers.CharField(source='item.item_name')
    item_price = serializers.IntegerField(source='item.item_price')
    
    class Meta:
        model = Order_item
        fields = ['item_id', 'item_name', 'item_price', 'count']

# 주문 등록 응답
class OrderSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(source='id')  # Order 모델의 id를 order_id로 사용
    member_id = serializers.IntegerField(source='member.id')
    items = OrderItemSerializer(many=True, source='order_item_set')  # OrderItemSerializer를 사용하여 items 필드 직렬화
    order_date = serializers.DateTimeField()  # Order 모델의 created_at을 order_date로 사용
    
    class Meta:
        model = Order_item
        fields = ['order_id', 'member_id', 'order_date','items']