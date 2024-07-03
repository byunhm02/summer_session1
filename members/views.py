from django.shortcuts import render

from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Member,Address
from .serializers import AddressSerializer,MemberSerializer

# Create your views here.


@api_view(['GET','POST'])
def member(request):
    if request.method=='POST':
        serializer=MemberSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data,status=201)
            except serializers.ValidationError as e:
                return Response({
                    'message': '회원 등록 실패'
                    #'error': str(e)
                }, status=409)
        return Response(serializer.errors,status=400)
    if request.method=='GET':
        member=Member.objects.all()
        serializer=MemberSerializer(member,many=True)
        return Response(serializer.data,status=200)

        
            
@api_view(['GET','PATCH','DELETE'])
def member_detail(request,id):
    if request.method=='GET':
        try:
            member=Member.objects.get(id=id)
        except Member.DoesNotExist:
            return Response({
                'message':'존재하지 않는 회원'
            },status=404)
        serializer=MemberSerializer(member)
        return Response(serializer.data,status=200)
        
    if request.method=='PATCH':
        try:
            member=Member.objects.get(id=id)
        except Member.DoesNotExist:
            return Response({
                'message':'존재하지 않는 회원'
            },status=404)
        serializer=MemberSerializer(member,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=200)
        return Response(status=400)
    if request.method=='DELETE':
        try:
            member=Member.objects.get(id=id)
        except Member.DoesNotExist:
            return Response({
                'message':'존재하지 않는 회원'
            },status=404)
        member.delete()
        return Response(status=200)