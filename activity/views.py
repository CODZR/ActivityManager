import json

from django.http import HttpResponse
from django.shortcuts import render

from activity import models
from activity.models import Activity


def index(request):
	return render(request, 'index.html')


# 更新日志
def log(request):
	return render(request, 'log.html')


def add_activity(request):
	if request.POST:
		username = request.POST.get('username', None)
		print(username)
		user_obj = models.User.objects.get(username=username)
		user_type = user_obj.user_type
		content = ''
		if user_type == 1:
			content = request.POST.get('content')
		a_obj = Activity(user=user_obj, content=content)
		a_obj.save()


def search_activity(request):
	act_all = Activity.objects.all()
	act_data = {'act_all': act_all}
	return render(request, 'activity/manage.html', act_data)


def update_activity(request):
	if request.POST:
		username = request.POST.get('username', None)
		user_obj = models.User.objects.get(username=username)
		user_type = user_obj.user_type
		
		act_id = request.POST.get('act_id', None)
		act_obj = models.Activity.objects.get(act_id=act_id)
		if user_type == 2:
			status1 = request.POST.get('status1', 1)
		if user_type == 3:
			status2 = request.POST.get('status2', 1)


def fail(request):
	return render(request, 'fail.html')
