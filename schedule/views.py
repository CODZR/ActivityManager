import json

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from schedule.utils import datetime_handler
from schedule.models import Schedule


def schedule(request):
	return render(request, 'schedule/manage.html')


def add_schedule(request):
	if request.POST:
		time_frame = request.POST.get('time_frame')
		description = request.POST.get('description')
		priority = request.POST.get('priority')
		is_done = request.POST.get('is_done')
		user_id = request.POST.get('user_id')
		print(user_id)
		print(is_done)
		try:
			sch_obj = Schedule(time_frame=time_frame, description=description, priority=priority, is_done=is_done, user_id=user_id)
			sch_obj.save()
			return render(request, 'schedule/add.html', {'message': '时间表添加成功'})
		except:
			print('fail to add')
			return render(request, 'schedule/add.html', {'message': '时间表添加失败'})
	else:
		return render(request, 'schedule/add.html')


# 用户信息的删除
def delete_schedule(request, sch_id):
	Schedule.objects.filter(sch_id=sch_id).delete()
	return render(request, 'schedule/manage.html')


# 根据id查时间表和分页
def search_schedule(request):
	sch_id = request.GET.get('sch_id')
	if sch_id is None:
		sch_obj_ordered = Schedule.objects.all().values().order_by('sch_id')
		count = sch_obj_ordered.count()  # 数据库中的目标总条数
		limit = request.GET.get('limit')  # 单页最大条数
		paginator = Paginator(sch_obj_ordered, limit)  # 分页对象
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
		# data = list(sch_obj_ordered)
		
		# layui需要的格式
		data = {"code": 0, "msg": "", "count": count, "data": res, }
		return HttpResponse(json.dumps(data, cls=datetime_handler.DateEncoder), content_type="application/json", )
	else:
		sch_obj = Schedule.objects.filter(sch_id=sch_id).values()
		data = list(sch_obj)
		# print(data)
		data = {"code": 0, "msg": "", "data": data}
		return HttpResponse(json.dumps(data, cls=datetime_handler.DateEncoder), content_type="application/json")


# 根据id来进行更新时间表
def update_schedule(request, sch_id):
	sch_obj = Schedule.objects.get(sch_id=sch_id)
	print(sch_obj)
	context = dict()
	context['Schedule'] = sch_obj
	
	if request.POST:
		time_frame = request.POST.get('time_frame', None)
		description = request.POST.get('description', None)
		priority = request.POST.get('priority', None)
		is_done = request.POST.get('is_done', None)
		user_id = request.POST.get('user_id', None)
		
		Schedule.objects.filter(sch_id=sch_id).update(time_frame=time_frame, description=description, priority=priority,
		                                              is_done=is_done, user_id=user_id)
		print('success')
		return render(request, 'schedule/update.html', context)
	else:
		return render(request, 'schedule/update.html', context)


def check_schedule(request):
	count_done = Schedule.objects.filter(is_done=True).values().count()
	count_undone = Schedule.objects.filter(is_done=False).values().count()
	check_data = {'count_done': count_done, 'count_undone': count_undone}
	return HttpResponse(json.dumps(check_data), content_type="application/json")
