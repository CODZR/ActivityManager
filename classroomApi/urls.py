from django.urls import path
from classroomApi import views

urlpatterns = [
	path('', views.room),
	path('add/', views.add_page),
	path('update/', views.update_page),
	path('detail/', views.RoomDetailAPI.as_view()),
	
]
