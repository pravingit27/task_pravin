from django.shortcuts import render
from rest_framework import generics,viewsets
from .serializers import studentserializer,markserializer,gradeserializer
from .models import student,Mark,Grade
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework.parsers import *
from rest_framework import status
from rest_framework.decorators import action
from django.db.models import Count
from rest_framework.generics import RetrieveAPIView

# Create your views here.

class StudentViewSet(viewsets.ModelViewSet):
	queryset = student.objects.all()
	serializer_class = studentserializer
	lookup_field = 'slug'

class Listmark(generics.ListCreateAPIView):
 #   permission_classes = (permissions.IsAuthenticated,)
	queryset = Mark.objects.all()
	serializer_class = markserializer

class Detailmark(generics.RetrieveUpdateDestroyAPIView):
  #  permission_classes = (permissions.IsAuthenticated,)
	queryset = Mark.objects.all()
	serializer_class = markserializer

class GradeViewSet(viewsets.ModelViewSet):
		#queryset = Grade.objects.prefetch_related('grade','marks').all()
		queryset = Grade.objects.all()
		serializer_class = gradeserializer

class TotalCountAPIView(RetrieveAPIView):
	 def get(self, request, *args, **kwargs):
		 count_student = student.objects.count()
		 count_grade = Grade.objects.count()
		 return Response(data= {'count_student':count_student, 'count_grade': count_grade})
	

			

	   



		
	