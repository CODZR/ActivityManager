from django.db import models

# Create your models here.
from userApp.models import User


class Classroom(models.Model):
	room_id = models.AutoField(primary_key=True)
	room_num = models.CharField(max_length=32, unique=True)
	room_status_entry = (
		(1, '空闲'),
		(2, '使用中'),
		(3, '暂不外借')
	)
	room_status = models.IntegerField(choices=room_status_entry, default=1)
	user = models.OneToOneField(User, on_delete=models.DO_NOTHING, null=True, blank=True, default='')
