from django.db import models


# Create your models here.
from userApp.models import User


class Schedule(models.Model):
	sch_id = models.AutoField(primary_key=True)
	time_frame = models.CharField(max_length=32)
	description = models.TextField(default='')
	priority_entry = (
		(1, 'black'),
		(2, 'red'),
		(3, 'blue'),
		(4, 'green')
	)
	# 通过 get_属性_display()方法取display_name
	priority = models.PositiveSmallIntegerField(choices=priority_entry, default=4)
	is_done = models.BooleanField(default=False)
	create_time = models.DateTimeField(auto_now_add=True)
	update_time = models.DateTimeField(auto_now=True)
# 为了页面和数据库中显示一致，需要在页面格式化时间，需要添加<td>{{ infor.updatetime|date:"Y-m-d H:i:s" }}</td> 类似的过滤器。
	user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default='')

