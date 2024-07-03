from rest_framework import serializers
from members.models import Member,Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['city', 'street', 'zipcode']

class MemberSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Member
        fields = ['id', 'name', 'address']

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        
        # 이미 존재하는지 확인
        existing_member = Member.objects.filter(name=validated_data['name']).first()
        if existing_member:
            raise serializers.ValidationError("Member with this name already exists.")
        
        # 존재하지 않는 경우 회원 생성
        member = Member.objects.create(**validated_data)
        Address.objects.create(member=member, **address_data)
        return member
    
    def update(self,instance,validated_data):
        Address_data=validated_data.pop('address')
        address_serializer=self.fields['address']
        address_instance=instance.address
        
        address_serializer.update(address_instance,Address_data)
        instance.save()
        return instance
