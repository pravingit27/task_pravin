from rest_framework import serializers
from . models import student,Mark,Grade
from rest_framework.serializers import Serializer

class studentserializer(serializers.ModelSerializer):
	
	class Meta:
		fields = (
			'name',
			'rollno',
			'dob',
		)
		model = student

class MarkGradeSerializer(serializers.ModelSerializer):

	class Meta:
		model = Mark
		fields = ('studentname',)

	def to_representation(self,instance):
		student = super(MarkGradeSerializer,self).to_representation(instance)
		student['studentname'] = instance.studentname.name
		return student


class gradeserializer(serializers.ModelSerializer):
	marks = MarkGradeSerializer(many=True,read_only=True)
	studentgrade_count = serializers.SerializerMethodField()   
	total_student = serializers.SerializerMethodField()  

	def get_studentgrade_count(self, obj):       
		return obj.marks.count()

	def get_total_student(self,obj):
		return student.objects.count()

	class Meta:
		model = Grade
		fields = ('grade','marks','studentgrade_count','total_student')

class markserializer(serializers.ModelSerializer):
	#marks = studentmarkserializer(many=True)
	#studentname = serializers.StringRelatedField()
	class Meta:     
		fields = (
			'id',
			'studentname',
			'studentmarks',
			'grade'
		)
		model = Mark

	def to_representation(self,instance):
		student = super(markserializer,self).to_representation(instance)
		student['studentname'] = instance.studentname.name
		return student

			




