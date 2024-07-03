
# Create your views here.
from django.shortcuts import render
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Order,Order_item
from .serializers import OrderSerializer
from members.models import Member
from .serializers import OrderRequestSerializer, OrderSerializer

@api_view(['POST', 'GET'])
def order(request):
    if request.method == 'POST':
        serializer = OrderRequestSerializer(data=request.data)
        if serializer.is_valid():
            order_instance = serializer.save()

            order_data = OrderSerializer(order_instance).data

            return Response( order_data, status=201)

        return Response(serializer.errors, status=400)
    
    elif request.method == 'GET':
        member_id = request.query_params.get('memberid')
        if not member_id:
            return Response( status=400)

        try:
            member = Member.objects.get(id=member_id)
        except Member.DoesNotExist:
            return Response( status=404)
        
        orders = Order.objects.filter(member=member)
        order_data = [
            {
                'order_id': order.id,
                'order_date': order.order_date,
                'items': [
                    {
                        'item_id': item.item.id,
                        'item_name': item.item.item_name,
                        'item_price': item.item.item_price,
                        'count': item.count
                    } for item in order.order_item_set.all()
                ]
            } for order in orders
        ]

        response_data = {
            'member_id': member.id,
            'orders': order_data
        }

        return Response(response_data, status=200)

@api_view(['DELETE', 'GET'])
def order_delete_detail(request, id):
    if not id:
        return Response(status=400)
    if request.method == 'DELETE':
        try:
            order = Order.objects.get(id=id)
        except Order.DoesNotExist:
            return Response(status=404)
        
        order.delete()
        return Response(status=200)
    
    elif request.method == 'GET':
        try:
            order = Order.objects.get(id=id)
        except Order.DoesNotExist:
            return Response(status=404)
        
        order_data = OrderSerializer(order).data

        return Response(order_data, status=200)
