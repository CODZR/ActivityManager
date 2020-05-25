import json

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render

from activity import models
from activity.models import Activity
from userApp.models import User, UserToken
from userApp.utils import get_token
# from userApp.utils.myAuthentication import check_token


def login(request):
	print(request.POST)
	if request.POST:  # 提交表单，登录验证并产生token
		print('post')
		username = request.POST.get('username', None)
		password = request.POST.get('password', None)
		user_obj = User.objects.get(username=username)
		if password == user_obj.password:  # 验证通过
			user_obj.is_active = True
			user_obj.save()  # 记得save不然无效
			print('is_active = True')
			operate_token = get_token.generate_token()  # 产生一个关键操作用的token
			UserToken.objects.update_or_create(user=user_obj, defaults={  # defaults 的值不同则创建，相同则更新
				'token': operate_token
			})
			return render(request, 'index.html', {'username': username, 'token': operate_token})
		else:  # 未提交表单，访问登陆界面
			print('failed')
			return render(request, 'userApp/login.html', {'mssg': '用户名或密码错误'})
	else:
		print('not post')
		return render(request, 'userApp/login.html')


def logout(request, username):
	user_obj = User.objects.get(username=username)
	user_obj.is_active = False  # 激活状态改为false
	user_obj.save()
	print('is_active = False')
	return render(request, 'userApp/login.html')


def index(request):
	username = request.POST.get('username')
	try:
		user_obj = User.objects.get(username=username)
		if user_obj.is_active:  # 登陆过已经激活（是从登录界面进来的，而不是post仿造用户名）
			print('done')
		return render(request, 'index.html')
	except User.DoesNotExist:
		print('user does not exist')
		return render(request, 'userApp/login.html')
	except:
		print('exceptions')
		return render(request, 'userApp/login.html')


# 更新日志
def log(request):
	return render(request, 'log.html')


def activity(request):
	return render(request, 'activity/manage.html')


def add_activity(request):
	if request.POST:
		print(1)
		act_content = request.POST.get('act_content')
		user_id = request.POST.get('user_id')
		print(act_content)
		try:
			print(2)
			act_obj = Activity(act_content=act_content, user_id=user_id)
			print(act_obj)
			act_obj.save()
			return render(request, 'activity/add.html', {'message': '活动表添加成功'})
		except:
			print('fail to add')
			return render(request, 'activity/add.html', {'message': '活动表添加失败'})
	else:
		return render(request, 'activity/add.html')


# 用户信息的删除
def delete_activity(request, act_id):
	Activity.objects.filter(act_id=act_id).delete()
	return render(request, 'activity/manage.html')


# 根据id查时间表和分页
def search_activity(request):
	act_id = request.GET.get('act_id')
	if act_id is None:
		activity_obj_ordered = Activity.objects.all().values().order_by('act_id')
		count = activity_obj_ordered.count()  # 数据库中的目标总条数
		limit = request.GET.get('limit')  # 单页最大条数
		paginator = Paginator(activity_obj_ordered, limit)  # 分页对象
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
		
		# layui需要的格式
		data = {"code": 0, "msg": "", "count": count, "data": res, }
		return HttpResponse(json.dumps(data), content_type="application/json", )
	else:
		act_obj = Activity.objects.filter(act_id=act_id).values()
		data = list(act_obj)
		# print(data)
		data = {"code": 0, "msg": "", "data": data}
		return HttpResponse(json.dumps(data), content_type="application/json")


# 根据id来进行更新时间表
def update_activity(request, act_id):
	act_obj = Activity.objects.get(act_id=act_id)
	print(act_obj)
	context = dict()
	context['Activity'] = act_obj
	
	if request.POST:
		act_content = request.POST.get('act_content')

		user_id = request.POST.get('user_id')
		act_obj = Activity()
		Activity.objects.filter(act_id=act_id).update(act_content=act_content, user_id=user_id)
		print('success')
		return render(request, 'activity/update.html', context)
	else:
		return render(request, 'activity/update.html', context)


def check_status1(request, act_id):
	act_obj = Activity.objects.get(act_id=act_id)
	context = dict()
	context['Activity'] = act_obj
	if request.POST:
		status1 = request.POST.get('status1')
		rej_reason = request.POST.get('rej_reason')
		Activity.objects.filter(act_id=act_id).update(status1=status1, rej_reason=rej_reason)
	return render(request, 'activity/check1.html', context)
	
	
def check_status2(request, act_id):
	act_obj = Activity.objects.get(act_id=act_id)
	context = dict()
	context['Activity'] = act_obj
	if request.POST:
		status2 = request.POST.get('status2')
		print(status2)
		rej_reason = request.POST.get('rej_reason')
		Activity.objects.filter(act_id=act_id).update(status2=status2, rej_reason=rej_reason)
	return render(request, 'activity/check2.html', context)
	

def fail(request):
	return render(request, 'fail.html')
