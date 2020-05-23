from django.urls import re_path, path
from userApp import views

urlpatterns = [
	#  path('user/', include('user.urls')),
	path('', views.user),
	path('add/', views.add_user),
	path('delete/<int:sch_id>', views.delete_user),
	path('search/', views.search_user),
	path('update/<int:sch_id>', views.update_user),
]
