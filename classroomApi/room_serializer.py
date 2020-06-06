from rest_framework import serializers

from classroomApi import models


class UserSerializer(serializers.ModelSerializer):
	user_id = serializers.CharField(required=False)
	username = serializers.CharField(required=False)
	email = serializers.EmailField(required=False)
	telephone = serializers.CharField(required=False)
	class Meta:
		model = models.User
		fields = ['user_id','username', 'email', 'telephone']


class RoomSerializer(serializers.ModelSerializer):
	room_id = serializers.IntegerField(required=False)
	room_num = serializers.CharField(required=True)
	room_status = serializers.IntegerField(required=True)
	user = UserSerializer(read_only=True, required=False)
	
	class Meta:
		model = models.Classroom
		fields = ['room_id', 'room_num', 'room_status', 'user']
