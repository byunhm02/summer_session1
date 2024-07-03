from django.shortcuts import render

# Create your views here.
from django.shortcuts import render


from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Item
from .serializers import ItemSerializer

# Create your views here.


@api_view(['GET','POST'])
def item(request):
    if request.method=='POST':
        serializer=ItemSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data,status=201)
            except serializers.ValidationError as e:
                return Response({
                    'message': '중복 등록'
                    #'error': str(e)
                }, status=409)
        return Response(serializer.errors,status=400)
    if request.method=='GET':
        member=Item.objects.all()
        serializer=ItemSerializer(member,many=True)
        return Response(serializer.data,status=200)

        
            
@api_view(['GET','PATCH','DELETE'])
def item_detail(request,id):
    if request.method=='GET':
        try:
            member=Item.objects.get(id=id)
        except Item.DoesNotExist:
            return Response({
                'message':'존재하지 않는 상품'
            },status=404)
        serializer=ItemSerializer(member)
        return Response(serializer.data,status=200)
        
    if request.method=='PATCH':
        try:
            member=Item.objects.get(id=id)
        except Item.DoesNotExist:
            return Response({
                'message':'존재하지 않는 상품'
            },status=404)
        serializer=ItemSerializer(member,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=200)
    if request.method=='DELETE':
        try:
            member=Item.objects.get(id=id)
        except Item.DoesNotExist:
            return Response({
                'message':'존재하지 않는 상품'
            },status=404)
        member.delete()
        return Response(status=200)