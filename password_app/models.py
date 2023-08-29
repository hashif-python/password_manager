from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
# Create your models here.

class Basemodel(models.Model):
    created_at = models.DateTimeField(blank=True,null=True)
    created_by = models.ForeignKey(User,related_name='%(class)s_createdby',on_delete=models.CASCADE,blank=True,null=True)
    updated_at = models.DateTimeField(blank=True,null=True)
    updated_by = models.ForeignKey(User,related_name='%(class)s_updatedby',on_delete=models.CASCADE,blank=True,null=True)
    deleted_at = models.DateTimeField(blank=True,null=True)
    deleted_by = models.ForeignKey(User,related_name='%(class)s_deletedby',on_delete=models.CASCADE,blank=True,null=True)

    class Meta:
        abstract = True

class UserPassword(Basemodel):
    user= models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    title=models.CharField(max_length=255,blank=True,null=True)
    user_password=models.CharField(max_length=255,blank=True,null=True)
    expiration=models.DateField(max_length=255,blank=True,null=True)
    is_deleted=models.BooleanField(default=False)

    def __str__(self):
        return str(self.title)

class SharePassword(Basemodel):
    user_pass_id= models.ForeignKey(UserPassword, on_delete=models.CASCADE,blank=True, null=True)
    share_to= models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    permission=models.CharField(max_length=255,blank=True,null=True)
    is_deleted=models.BooleanField(default=False)

    def __str__(self):
        return str(self.user_pass_id.title)


class PasswordEditRequests(Basemodel):
    user_pass_id= models.ForeignKey(UserPassword, on_delete=models.CASCADE,blank=True, null=True)
    reqs_by= models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    request_to=models.CharField(max_length=255,blank=True,null=True)
    status=models.CharField(max_length=255,blank=True,null=True)
    is_deleted=models.BooleanField(default=False)

    def __str__(self):
        return str(self.user_pass_id.title)



class Organisation(Basemodel):
    owner= models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    organasation_name= models.CharField(max_length=255,blank=True,null=True)
    password_title=models.CharField(max_length=255,blank=True,null=True)
    organasation_password=models.CharField(max_length=255,blank=True,null=True)
    members= models.ManyToManyField(User,related_name='memebers',blank=True, null=True)
    is_deleted=models.BooleanField(default=False)

    def __str__(self):
        return str(self.organasation_name)