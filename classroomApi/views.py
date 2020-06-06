import json

from django.core.paginator import UnorderedObjectListWarning
from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
from classroomApi import models, room_serializer


class MyPageNumberPagination(PageNumberPagination):
	# 默认一页条数
	page_size = 5
	# 前端发送的页数关键字名
	page_query_param = 'page'
	# 用户自定义一页条数 关键字名
	page_size_query_param = 'limit'
	# 用户自定义一页最大控制条数
	max_page_size = 30


def room(request):
	return render(request, 'room/manage.html')


def add_page(request):
	return render(request, 'room/add.html')


def update_page(request):
	response_msg = dict()
	room_id = request.GET.get('room_id')
	room_obj = models.Classroom.objects.get(room_id=room_id)
	response_msg['room_data'] = room_obj
	response_msg['msg'] = '更新成功'
	return render(request, 'room/update.html', response_msg)


class RoomDetailAPI(APIView):
	def get(self, request):
		response_msg = dict()  # 定义返回消息体
		
		room_id = request.query_params.get('room_id')
		if room_id:
			try:
				room_obj = models.Classroom.objects.get(room_id=room_id)
				r_serializer = room_serializer.RoomSerializer(room_obj)
				
				response_msg = {"code": 0, "msg": "", "data": r_serializer.data}
				print(response_msg)
			except:
				# 宽泛异常，未学习先做简化处理
				response_msg = {"code": -1, "msg": "", "data": None}
			return Response(response_msg)
		else:
			try:
				# 这里room_objs不排序会报一个Warning，不用管主键room_id为自增字段本身是排好序的，且order_by('id')效率极低
				room_objs = models.Classroom.objects.all()
				
				count = room_objs.count()
				# 实例化分页类
				page = MyPageNumberPagination()
				# 调用paginate_queryset进行分页，获取当前分页数据
				page_data = page.paginate_queryset(queryset=room_objs, request=request, view=self)
				r_serializer = room_serializer.RoomSerializer(instance=page_data, many=True)
				
				# layui需要的格式
				response_msg = {"code": 0, "msg": "", "count": count, "data": r_serializer.data}
			# except UnorderedObjectListWarning:
			# 	pass
			except:
				# 宽泛异常，未学习先做简化处理
				response_msg = {"code": -1, "msg": "", "data": None}
			return Response(response_msg)
	
	def post(self, request):
		response_msg = dict()  # 定义返回消息体
		r_serializer = room_serializer.RoomSerializer(data=request.data)
		room_num = request.data.get('room_num')
		
		room_exist = models.Classroom.objects.filter(room_num=room_num).exists()
		
		if r_serializer.is_valid():
			try:
				if room_exist:
					response_msg['msg'] = '教室号重复'
				else:
					r_serializer.save()
					response_msg['msg'] = '上传成功'
			except Exception as e:
				response_msg['Exception_message'] = e.args
				response_msg['validated_error_message'] = r_serializer.errors
		return Response(response_msg)
	
	def put(self, request):
		response_msg = dict()  # 定义返回消息体
		room_id = request.query_params.get('room_id')
		room_obj = models.Classroom.objects.get(room_id=room_id)
		r_serializer = room_serializer.RoomSerializer(instance=room_obj, data=request.data)
		if r_serializer.is_valid(raise_exception=True):
			try:
				room_status = request.data.get('room_status')
				user_id = request.data.get('user_id')
				
				if user_id is not None:  # 有人正在借用这个教室
					print(user_id)
					user_obj = models.User.objects.get(user_id=user_id)
					print(user_obj)
					r_serializer.save(user=user_obj)
					print(r_serializer)
				else:
					print(3)
					r_serializer.save()
				response_msg['msg'] = '更新成功'
			except Exception as e:
				print('wrong')
				response_msg['Exception_message'] = e.args
				response_msg['validated_error_message'] = r_serializer.errors
		return Response(response_msg)
	
	def delete(self, request):
		response_msg = dict()  # 定义返回消息体
		room_id = request.query_params.get('room_id')
		print(room_id)
		try:
			room_obj = models.Classroom.objects.get(room_id=room_id)
			room_obj.delete()
			response_msg['msg'] = 'Deleted successfully'
		except:
			response_msg['msg'] = 'room_id does not exist or unknown error'
		return Response(response_msg)
