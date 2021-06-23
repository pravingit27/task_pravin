from django.shortcuts import render
from rest_framework import generics,viewsets
from .serializers import studentserializer,markserializer,gradeserializer,UserSerializer
from .models import student,Mark,Grade,User
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework.parsers import *
from rest_framework import status
from rest_framework.decorators import action
from django.db.models import Count
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from rest_framework import permissions
import jwt, datetime

# Create your views here.
class RegisterView(APIView):
	def post(self,request):
		serializer = UserSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(serializer.data)

class LoginView(APIView):
	def post(self,request):
		email = request.data['email']
		password = request.data['password']

		user = User.objects.filter(email=email).first()

		if user is None:
			raise exceptions.AuthenticationFailed('User not Found!')

		if user.check_password(password):
			raise exceptions.AuthenticationFailed('Incorrect Password')

		payload = {
			'id':user.id,
			'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
			'iat': datetime.datetime.utcnow()
		}

		token = jwt.encode(payload, 'secret',algorithm='HS256').decode('utf-8')

		response =Response()
		response.set_cookie(key='jwt', value=token, httponly=True)

		response.data = {
			'jwt':token
		}
		return response

class UserView(APIView):
	def get(self,request):
		token = request.COOKIES.get('jwt')

		if not token:
			raise exceptions.AuthenticationFailed('Unauthenticated')

		try:
			payload = jwt.decode(token,'secret',algorithm=['HS256'])
		except jwt.ExpiredSignatureError:
			raise AuthenticationFailed('Unauthenticated')

		user = User.objects.filter(id=payload['id']).first()
		serializer = UserSerializer(user)

		return Response(serializer.data)

class LogoutView(APIView):
	def post(self,request):
		response = Response()
		response.delete_cookie('jwt')
		response.data = {
			'message':'logout success'
		}
		return response

class StudentViewSet(viewsets.ModelViewSet):
	#permission_classes = (permissions.IsAuthenticated,)
	queryset = student.objects.all()
	serializer_class = studentserializer
	lookup_field = 'slug'

class Listmark(generics.ListCreateAPIView):
	#permission_classes = (permissions.IsAuthenticated,)
	queryset = Mark.objects.all()
	serializer_class = markserializer

class Detailmark(generics.RetrieveUpdateDestroyAPIView):
	#permission_classes = (permissions.IsAuthenticated,)
	queryset = Mark.objects.all()
	serializer_class = markserializer

class GradeViewSet(viewsets.ModelViewSet):
	#permission_classes = (permissions.IsAuthenticated,)
		#queryset = Grade.objects.prefetch_related('grade','marks').all()
	queryset = Grade.objects.all()
	serializer_class = gradeserializer

class TotalCountAPIView(RetrieveAPIView):
	 def get(self, request, *args, **kwargs):
		 count_student = student.objects.count()
		 count_grade = Grade.objects.count()
		 return Response(data= {'count_student':count_student, 'count_grade': count_grade})
	

			

	   



		
	