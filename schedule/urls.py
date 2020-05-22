from django.urls import re_path, path
from schedule import views

urlpatterns = [
	#  path('schedule/', include('schedule.urls')),
	path('', views.schedule),
	path('add/', views.add_schedule),
	path('delete/<int:sch_id>', views.delete_schedule),
	path('search/', views.search_schedule),
	path('update/<int:sch_id>', views.update_schedule),
	path('check/', views.check_schedule),
]
