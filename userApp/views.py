import json

from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from schedule.utils import datetime_handler
from userApp.models import User, UserToken
from userApp.utils import get_token


def user(request):
	return render(request, 'userApp/manage.html')


def add_user(request):
	if request.POST:
		username = request.POST.get('username')
		if User.objects.filter(username=username).exists():
			print('exist')
			return render(request, 'userApp/add.html', {'message': '用户重复'})
		password = request.POST.get('password')
		email = request.POST.get('email')
		telephone = request.POST.get('telephone')
		user_type = request.POST.get('user_type')
		try:
			user_obj = User(username=username, password=password, email=email, telephone=telephone, user_type=user_type)
			user_obj.save()
			return render(request, 'userApp/add.html', {'message': '添加成功'})
		except:
			print('fail to add')
			return render(request, 'userApp/add.html', {'message': '添加失败'})
	else:
		return render(request, 'userApp/add.html')


# 用户信息的删除
def delete_user(request, user_id):
	User.objects.filter(user_id=user_id).delete()
	return render(request, 'userApp/manage.html')


# 根据id查用户表和分页
def search_user(request):
	user_id = request.GET.get('user_id')
	if user_id is None:
		user_obj_ordered = User.objects.all().values().order_by('user_id')
		count = user_obj_ordered.count()  # 数据库中的目标总条数
		limit = request.GET.get('limit')  # 单页最大条数
		paginator = Paginator(user_obj_ordered, limit)  # 分页对象
		page = request.GET.get('page')  # 当前页数
		# print(page)
		try:
			contacts = paginator.page(page)
		except PageNotAnInteger:
			contacts = paginator.page(1)
		except EmptyPage:
			contacts = paginator.page(paginator.num_pages)
		# print(contacts)
		res = []
		for contact in contacts:
			res.append(contact)
		# 数据转为列表
		# data = list(user_obj_ordered)
		
		# layui需要的格式
		data = {"code": 0, "msg": "", "count": count, "data": res, }
		return HttpResponse(json.dumps(data, cls=datetime_handler.DateEncoder), content_type="application/json", )
	else:
		user_obj = User.objects.filter(user_id=user_id).values()
		data = list(user_obj)
		# print(data)
		data = {"code": 0, "msg": "", "data": data}
		return HttpResponse(json.dumps(data, cls=datetime_handler.DateEncoder), content_type="application/json")


# 根据id来进行更新用户表
def update_user(request, user_id):
	user_obj = User.objects.get(user_id=user_id)
	print(user_obj)
	context = dict()
	context['User'] = user_obj
	
	if request.POST:
		username = request.POST.get('username')
		password = request.POST.get('password')
		email = request.POST.get('email')
		telephone = request.POST.get('telephone')
		user_type = request.POST.get('user_type')
		schedule = request.POST.get('schedule')
		
		User.objects.filter(user_id=user_id).update(username=username, password=password, email=email, telephone=telephone, user_type=user_type)
		print('success')
		return render(request, 'userApp/update.html', context)
	else:
		return render(request, 'userApp/update.html', context)
