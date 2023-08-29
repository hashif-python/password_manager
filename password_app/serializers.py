from rest_framework import serializers
from .models import *
from django.utils import timezone
from django.contrib.auth.models import User
import time,datetime




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','password','email']


class UserPasswordSerializer(serializers.ModelSerializer):
    username=serializers.CharField(source='user.username',read_only=True)
    class Meta:
        model = UserPassword
        fields = ['id','user','username','title','user_password','expiration','created_at','updated_at',\
        'deleted_at','created_by','updated_by','deleted_by']





    def create(self, validated_data):
        
        userpass = UserPassword.objects.create(**validated_data)
        return userpass


class UsersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username']


class PasswordShareSerializer(serializers.ModelSerializer):
    shared_user=serializers.CharField(source='share_to.username',read_only=True)
    password_id=serializers.CharField(source='user_pass_id.id',read_only=True)
    password_title=serializers.CharField(source='user_pass_id.title',read_only=True)
    password=serializers.CharField(source='user_pass_id.user_password',read_only=True)
    class Meta:
        model = SharePassword
        fields = ['id','shared_user','password_id','password_title','password','permission','created_at','updated_at',\
        'deleted_at','created_by','updated_by','deleted_by']

class PasswordShareToSerializer(serializers.ModelSerializer):
    user=serializers.CharField(source='user_pass_id.user.username',read_only=True)
    password_id=serializers.CharField(source='user_pass_id.id',read_only=True)
    password_title=serializers.CharField(source='user_pass_id.title',read_only=True)
    password=serializers.CharField(source='user_pass_id.user_password',read_only=True)
    class Meta:
        model = SharePassword
        fields = ['id','user','password_id','password_title','password','permission','created_at','updated_at',\
        'deleted_at','created_by','updated_by','deleted_by']


class PasswordEditReqsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordEditRequests
        fields = ['id','user_pass_id','reqs_by','request_to','status']


class OrganisationGetSerializer(serializers.ModelSerializer):
    members=serializers.SerializerMethodField()
    class Meta:
        model = Organisation
        fields = ['id','owner','organasation_name','organasation_password','members']

    def get_members(self, obj):
        # get_members_data = obj.value_list('id', 'username')

        # get_members_list = list(get_members_data)
        members_data=obj.members.all()
        members = members_data.values('id', 'username')


        return members


class OrganisationGuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = ['id','owner','organasation_name','organasation_password']

    