from django.db import models

# Create your models here.
from schedule.models import Schedule
from userApp.models import User


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
