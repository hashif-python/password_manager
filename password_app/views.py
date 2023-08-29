from django.shortcuts import render
from rest_framework.views import APIView
import time,datetime
from rest_framework.response import Response
from .serializers import *
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from . models import *
from django.utils import timezone
from .utils import *
from django.db.models import Q


class Login(APIView):
	def get(self, request):
		try:
			startT = time.time()
			username = request.data.get('username')
			password = request.data.get('password')
			user = authenticate(username=username, password=password)
			if user:
				refresh = RefreshToken.for_user(user)
				access_token = str(refresh.access_token)
				refresh_token = str(refresh)
				data={'access_token': access_token,'refresh_token': refresh_token}
				exc_time=f'execution time: {time.time() - startT}ms'
				return Response({'status':'success','data':data,'exc_time':exc_time})
			else:
				data={'message': 'Invalid credentials'}
            
				exc_time=f'execution time: {time.time() - startT}ms'
				return Response({'status':'failed','data':data,'exc_time':exc_time})
		except Exception as e:
			exc_time=f'execution time: {time.time() - startT}ms'
			return Response({'status':'error','data': {'message':str(e)}, 'exc_time':exc_time})


class Signup(APIView):
    def post(self, request):
        try:
            startT = time.time()
            data=request.data
            serializer=UserSerializer(data=data)
            data['password']=make_password(data['password'])
            if serializer.is_valid():
                serializer.save()
        
                exc_time=f'execution time: {time.time() - startT}ms'
            
                return Response({'status':'success','data': serializer.data,'exc_time':exc_time})
            else:
                exc_time=f'execution time: {time.time() - startT}ms'
                return JsonResponse({'status': 'error', 'data':serializer.errors,'exc_time':exc_time})
        except Exception as e:
            exc_time=f'execution time: {time.time() - startT}ms'
            return Response({'status':'error','data': {'message':str(e)}, 'exc_time':exc_time})




class UserPasswordView(APIView):
	permission_classes = (IsAuthenticated,)
	def get(self, request):
		try:
			startT = time.time()
			user_passwords=UserPassword.objects.filter(user=request.user,is_deleted=False)
			serializer=UserPasswordSerializer(user_passwords,many=True)

			exc_time=f'execution time: {time.time() - startT}ms'
			return Response({'status':'success','data':serializer.data,'exc_time':exc_time})
		except Exception as e:
			exc_time=f'execution time: {time.time() - startT}ms'
			return Response({'status':'error','data': {'message':str(e)}, 'exc_time':exc_time})


	def post(self, request):
		try:
			startT = time.time()
			data=request.data
			data['created_at']=timezone.localtime(timezone.now())
			data['created_by']=request.user.id
			data['user']=request.user.id
			pass_validation=validate_password(data['user_password'])
			if pass_validation['status'] == True:
				serializer=UserPasswordSerializer(data=data)
				if serializer.is_valid():
					serializer.save()

					exc_time=f'execution time: {time.time() - startT}ms'
					return Response({'status':'success','data':serializer.data,'exc_time':exc_time})
				else:
					exc_time=f'execution time: {time.time() - startT}ms'
					return Response({'status':'fail','data':serializer.errors,'exc_time':exc_time})
			else:
				exc_time=f'execution time: {time.time() - startT}ms'
				return Response({'status':'fail','data':pass_validation,'exc_time':exc_time})
		except Exception as e:
			exc_time=f'execution time: {time.time() - startT}ms'
			return Response({'status':'error','data': {'message':str(e)}, 'exc_time':exc_time})


class UserPasswordDetailView(APIView):
	permission_classes = (IsAuthenticated,)
	def get(self, request):
		try:
			startT = time.time()
			objid=request.GET.get('objid')
			password_obj=UserPassword.objects.get(id=objid,user=request.user,is_deleted=False)
			serializer=UserPasswordSerializer(password_obj,many=False)

			exc_time=f'execution time: {time.time() - startT}ms'
			return Response({'status':'success','data':serializer.data,'exc_time':exc_time})
		except Exception as e:
			exc_time=f'execution time: {time.time() - startT}ms'
			return Response({'status':'error','data': {'message':str(e)}, 'exc_time':exc_time})


	def patch(self, request):
		try:
			startT = time.time()
			data=request.data
			objid=request.GET.get('objid')
			password_obj=UserPassword.objects.get(id=objid,user=request.user,is_deleted=False)

			data['updated_at']=timezone.localtime(timezone.now())
			data['updated_by']=request.user.id
			if  'user_password' in data:
				pass_validation=validate_password(data['user_password'])
			else:
				pass_validation=validate_password(password_obj.user_password)

			if pass_validation['status'] == True:
				serializer= UserPasswordSerializer(password_obj,data=request.data,partial=True)
				if serializer.is_valid():
					serializer.save()

					exc_time=f'execution time: {time.time() - startT}ms'
					return Response({'status':'success','data':serializer.data,'exc_time':exc_time})
				else:
					exc_time=f'execution time: {time.time() - startT}ms'
					return Response({'status':'fail','data':serializer.errors,'exc_time':exc_time})
			else:
				exc_time=f'execution time: {time.time() - startT}ms'
				return Response({'status':'fail','data':pass_validation,'exc_time':exc_time})
		except Exception as e:
			exc_time=f'execution time: {time.time() - startT}ms'
			return Response({'status':'error','data': {'message':str(e)}, 'exc_time':exc_time})


	def delete(self, request):
		try:
			startT = time.time()
			data=request.data
			objid=request.GET.get('objid')
			password_obj=UserPassword.objects.get(id=objid,user=request.user,is_deleted=False)
			password_obj.is_deleted=True
			password_obj.save()
			
			exc_time=f'execution time: {time.time() - startT}ms'
			return Response({'status':'success','data':{'message':'Object Deleted'},'exc_time':exc_time})
		except Exception as e:
			exc_time=f'execution time: {time.time() - startT}ms'
			return Response({'status':'error','data': {'message':str(e)}, 'exc_time':exc_time})



class UsersListView(APIView):
	permission_classes = (IsAuthenticated,)
	def get(self, request):
		try:
			startT = time.time()
			users=User.objects.all().exclude(Q(is_superuser=True) | Q(username=request.user.username))
			print(len(users))
			serializer=UsersListSerializer(users,many=True)

			exc_time=f'execution time: {time.time() - startT}ms'
			return Response({'status':'success','data':serializer.data,'exc_time':exc_time})
		except Exception as e:
			exc_time=f'execution time: {time.time() - startT}ms'
			return Response({'status':'error','data': {'message':str(e)}, 'exc_time':exc_time})


class PasswordShareView(APIView):
	permission_classes = (IsAuthenticated,)
	def get(self, request):
		try:
			startT = time.time()
			objid=request.GET.get('objid')
			shared_users=SharePassword.objects.filter(user_pass_id__user=request.user,\
				user_pass_id__id=objid,is_deleted=False)
			serializer=PasswordShareSerializer(shared_users,many=True)

			exc_time=f'execution time: {time.time() - startT}ms'
			return Response({'status':'success','data':serializer.data,'exc_time':exc_time})
		except Exception as e:
			exc_time=f'execution time: {time.time() - startT}ms'
			return Response({'status':'error','data': {'message':str(e)}, 'exc_time':exc_time})


	def post(self, request):
		try:
			startT = time.time()
			objid=request.GET.get('objid')
			user_list=request.data['user_list']
			permission=request.data['permissions']
			ob=UserPassword.objects.filter(id=objid,user=request.user,is_deleted=False).last()
			if ob:
				for i in user_list:
					print(i)
					user=User.objects.get(id=i)
					obj=SharePassword.objects.create(user_pass_id=ob,share_to=user,\
						created_at=timezone.localtime(timezone.now()),created_by=request.user,\
						permission=permission)
				
				exc_time=f'execution time: {time.time() - startT}ms'
				return Response({'status':'success','data':[user_list,permission],'exc_time':exc_time})
			else:

				exc_time=f'execution time: {time.time() - startT}ms'
				return Response({'status':'fail','data':{"message":"Permission denied"},'exc_time':exc_time})
		except Exception as e:
			exc_time=f'execution time: {time.time() - startT}ms'
			return Response({'status':'error','data': {'message':str(e)}, 'exc_time':exc_time})


	def patch(self, request):
		try:
			startT = time.time()
			obj_id=request.GET.get('obj_id')
			user_list=request.data['user_list']
			permission=request.data['permissions']

			obj=SharePassword.objects.filter(user_pass_id_id=obj_id,user_pass_id__user=request.user)

			objlast=obj.last()

			ob=UserPassword.objects.filter(id=objlast.user_pass_id.id,user=request.user,is_deleted=False).last()
			print('hi',ob)
			if ob:
				obj.delete()
				for i in user_list:
					user=User.objects.get(id=i)
					obj=SharePassword.objects.create(user_pass_id=ob,share_to=user,updated_at=timezone.localtime(timezone.now()),\
						updated_by=request.user,permission=permission)
				
				exc_time=f'execution time: {time.time() - startT}ms'
				return Response({'status':'success','data':[user_list,permission],'exc_time':exc_time})
			else:

				exc_time=f'execution time: {time.time() - startT}ms'
				return Response({'status':'fail','data':{"message":"Permission denied"},'exc_time':exc_time})
		except Exception as e:
			exc_time=f'execution time: {time.time() - startT}ms'
			return Response({'status':'error','data': {'message':str(e)}, 'exc_time':exc_time})


	def delete(self, request):
		try:
			startT = time.time()
			obj_id=request.GET.get('obj_id')
			

			obj=SharePassword.objects.filter(user_pass_id_id=obj_id,user_pass_id__user=request.user)
			
			obj.update(is_deleted=True)
			
			exc_time=f'execution time: {time.time() - startT}ms'
			return Response({'status':'fail','data':{"message":"Password Share Removed"},'exc_time':exc_time})
		except Exception as e:
			exc_time=f'execution time: {time.time() - startT}ms'
			return Response({'status':'error','data': {'message':str(e)}, 'exc_time':exc_time})



class SharedPasswordView(APIView):
	permission_classes = (IsAuthenticated,)
	def get(self, request):
		try:
			startT = time.time()
			shared_users=SharePassword.objects.filter(share_to=request.user,is_deleted=False)
			serializer=PasswordShareToSerializer(shared_users,many=True)

			exc_time=f'execution time: {time.time() - startT}ms'
			return Response({'status':'success','data':serializer.data,'exc_time':exc_time})
		except Exception as e:
			exc_time=f'execution time: {time.time() - startT}ms'
			return Response({'status':'error','data': {'message':str(e)}, 'exc_time':exc_time})


	def patch(self, request):
		try:
			startT = time.time()
			share_id=request.GET.get('share_id')
			title=request.data['title']
			user_password=request.data['user_password']
			shared_users=SharePassword.objects.get(id=share_id,share_to=request.user,is_deleted=False)
			if 'edit' in shared_users.permission:
				shared_users.user_pass_id.title=title
				shared_users.user_pass_id.user_password=user_password
				shared_users.user_pass_id.updated_at=timezone.localtime(timezone.now())
				shared_users.user_pass_id.updated_by=request.user
				shared_users.user_pass_id.save()
				exc_time=f'execution time: {time.time() - startT}ms'
				return Response({'status':'success','data':{'message':'Password Object Updated'},'exc_time':exc_time})
			else:
				exc_time=f'execution time: {time.time() - startT}ms'
				return Response({'status':'fail','data':{'message':'Permission Denied'},'exc_time':exc_time})
		except Exception as e:
			exc_time=f'execution time: {time.time() - startT}ms'
			return Response({'status':'error','data': {'message':str(e)}, 'exc_time':exc_time})

	

class EditPasswordReqsView(APIView):
	permission_classes = (IsAuthenticated,)
	def get(self, request):
		try:
			startT = time.time()
			reqs=PasswordEditRequests.objects.filter(reqs_by=request.user,is_deleted=False)
			serializer=PasswordEditReqsSerializer(reqs,many=True)

			exc_time=f'execution time: {time.time() - startT}ms'
			return Response({'status':'success','data':serializer.data,'exc_time':exc_time})
		except Exception as e:
			exc_time=f'execution time: {time.time() - startT}ms'
			return Response({'status':'error','data': {'message':str(e)}, 'exc_time':exc_time})



	def post(self, request):
		try:
			startT = time.time()
			objid=request.GET.get('objid')
			shared_pass=SharePassword.objects.get(id=objid,is_deleted=False)

			if shared_pass.share_to==request.user:
				if 'edit' not in shared_pass.permission:
					obreq=PasswordEditRequests.objects.filter(user_pass_id=shared_pass.user_pass_id,reqs_by=request.user,\
						request_to='edit',is_deleted=False).last()
					if obreq:
						exc_time=f'execution time: {time.time() - startT}ms'
						return Response({'status':'fail','data':{'message':'Password Edit Permission Already Requested,Please Wait for Approval '},'exc_time':exc_time})
					else:
						ob=PasswordEditRequests.objects.create(user_pass_id=shared_pass.user_pass_id,\
							created_at=timezone.localtime(timezone.now()),created_by=request.user,\
							reqs_by=request.user,request_to='edit')
						exc_time=f'execution time: {time.time() - startT}ms'
						return Response({'status':'success','data':{'message':'Password Edit Permission Requested'},'exc_time':exc_time})
				else:
					exc_time=f'execution time: {time.time() - startT}ms'
					return Response({'status':'fail','data':{'message':'Already Permission Granted'},'exc_time':exc_time})
			else:
				exc_time=f'execution time: {time.time() - startT}ms'
				return Response({'status':'fail','data':{'message':'Permission Denied'},'exc_time':exc_time})
		except Exception as e:
			exc_time=f'execution time: {time.time() - startT}ms'
			return Response({'status':'error','data': {'message':str(e)}, 'exc_time':exc_time})



class PasswordEditReqsView(APIView):
	permission_classes = (IsAuthenticated,)
	def get(self, request):
		try:
			startT = time.time()
			reqs=PasswordEditRequests.objects.filter(user_pass_id__user=request.user,is_deleted=False)
			serializer=PasswordEditReqsSerializer(reqs,many=True)

			exc_time=f'execution time: {time.time() - startT}ms'
			return Response({'status':'success','data':serializer.data,'exc_time':exc_time})
		except Exception as e:
			exc_time=f'execution time: {time.time() - startT}ms'
			return Response({'status':'error','data': {'message':str(e)}, 'exc_time':exc_time})


	def patch(self, request):
		try:
			startT = time.time()
			req_id=request.GET.get('req_id')
			status=request.data['status']
			reqs=PasswordEditRequests.objects.get(id=req_id,user_pass_id__user=request.user,is_deleted=False)
			print('Hi',reqs)
			if status=='Accepted':
				reqs.status='Accepted'
				reqs.updated_at=timezone.localtime(timezone.now())
				reqs.updated_by=request.user
				reqs.save()
				shared_pass=SharePassword.objects.get(user_pass_id__id=reqs.user_pass_id.id,share_to=reqs.reqs_by)
				
				shared_pass.permission='view,edit'
				shared_pass.save()
				exc_time=f'execution time: {time.time() - startT}ms'
				return Response({'status':'success','data':{'message':'Edit Request Granted'},'exc_time':exc_time})
			elif status=='Revoked':
				reqs.status='Revoked'
				reqs.updated_at=timezone.localtime(timezone.now())
				reqs.updated_by=request.user,
				reqs.save()
				exc_time=f'execution time: {time.time() - startT}ms'
				return Response({'status':'success','data':{'message':'Edit Request Revoked'},'exc_time':exc_time})
			else:
				exc_time=f'execution time: {time.time() - startT}ms'
				return Response({'status':'fail','data':{'message':'Something Went Wrong'},'exc_time':exc_time})
		except Exception as e:
			exc_time=f'execution time: {time.time() - startT}ms'
			return Response({'status':'error','data': {'message':str(e)}, 'exc_time':exc_time})


	

class OrganisationView(APIView):
	permission_classes = (IsAuthenticated,)
	def get(self, request):
		try:
			startT = time.time()
			obj=Organisation.objects.filter(owner=request.user,is_deleted=False)
			serializer=OrganisationGetSerializer(obj,many=True)

			exc_time=f'execution time: {time.time() - startT}ms'
			return Response({'status':'success','data':serializer.data,'exc_time':exc_time})
		except Exception as e:
			exc_time=f'execution time: {time.time() - startT}ms'
			return Response({'status':'error','data': {'message':str(e)}, 'exc_time':exc_time})


	def post(self, request):
		try:
			startT = time.time()
			data=request.data
			pass_validation=validate_password(data['organasation_password'])
			if pass_validation['status'] == True:
				ob=Organisation.objects.create(owner=request.user,password_title=data['password_title'],\
				organasation_name=data['organasation_name'],organasation_password=data['organasation_password'],\
				created_at=timezone.localtime(timezone.now()),created_by=request.user,)

				user_list=data['members']
				users = User.objects.filter(id__in=user_list)
				ob.members.add(*users)

				exc_time=f'execution time: {time.time() - startT}ms'
				return Response({'status':'success','data':{'message':'Organisation Added'},'exc_time':exc_time})
			else:
				exc_time=f'execution time: {time.time() - startT}ms'
				return Response({'status':'fail','data':pass_validation,'exc_time':exc_time})
		except Exception as e:
			exc_time=f'execution time: {time.time() - startT}ms'
			return Response({'status':'error','data': {'message':str(e)}, 'exc_time':exc_time})


	def patch(self, request):
		try:
			startT = time.time()
			objid=request.GET.get('objid')
			data=request.data
			obj=Organisation.objects.get(id=objid,owner=request.user)
			obj.organasation_name = request.data.get('organasation_name',obj.organasation_name)
			obj.password_title = request.data.get('password_title',obj.password_title)
			obj.organasation_password = request.data.get('organasation_password',obj.organasation_password)
			

			if request.data.get('members'):
				obj.members.clear()
				user_list=data['members']
				users = User.objects.filter(id__in=user_list)
				obj.members.add(*users)

			obj.save()
			exc_time=f'execution time: {time.time() - startT}ms'
			return Response({'status':'success','data':{'message':'Organisation Updated'},'exc_time':exc_time})
			
		except Exception as e:
			exc_time=f'execution time: {time.time() - startT}ms'
			return Response({'status':'error','data': {'message':str(e)}, 'exc_time':exc_time})



class GuestOrganisationView(APIView):
	permission_classes = (IsAuthenticated,)
	def get(self, request):
		try:
			startT = time.time()
			obj = Organisation.objects.filter(members__id=request.user.id, is_deleted=False)
			serializer=OrganisationGuestSerializer(obj,many=True)

			exc_time=f'execution time: {time.time() - startT}ms'
			return Response({'status':'success','data':serializer.data,'exc_time':exc_time})
		except Exception as e:
			exc_time=f'execution time: {time.time() - startT}ms'
			return Response({'status':'error','data': {'message':str(e)}, 'exc_time':exc_time})