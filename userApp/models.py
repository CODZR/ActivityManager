from django.db import models

# Create your models here.


class User(models.Model):
	user_id = models.AutoField(primary_key=True)
	username = models.CharField(max_length=32)
	password = models.CharField(max_length=32)
	email = models.EmailField(max_length=32, default='', null=True, blank=True)
	telephone = models.CharField(max_length=32, default='', null=True, blank=True)
	user_type_entry = (
		(1, 'student'),
		(2, 'instructor'),
		(3, 'dean'),
		(4, 'admin')
	)
	user_type = models.IntegerField(choices=user_type_entry)
	
	def __str__(self):
		return self.username


class UserToken(models.Model):
	user = models.OneToOneField('User', on_delete=models.CASCADE)
	token = models.CharField(max_length=128)
