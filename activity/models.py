from django.db import models

# Create your models here.
from schedule.models import Schedule


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
	schedule = models.ForeignKey(Schedule, on_delete=models.DO_NOTHING, default='')
	
	def __str__(self):
		return self.username


class UserToken(models.Model):
	user = models.OneToOneField('User', on_delete=models.CASCADE)
	token = models.CharField(max_length=128)


class Activity(models.Model):
	act_id = models.AutoField(primary_key=True)
	content = models.TextField(default='')
	status_entry = (
		(1, 'under_review'),
		(2, 'pass'),
		(3, 'reject')
	)
	status1 = models.IntegerField(choices=status_entry, default=1)  # 辅导员批准
	status2 = models.IntegerField(choices=status_entry, default=1)  # 教务处批准
	rej_reason = models.TextField(default='', null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, default='')
