from django.urls import re_path, path
from activity import views

urlpatterns = [
	path('index/', views.index),
	path('activity/search/', views.search_activity),
	path('fail/', views.fail),
	path('log/', views.log),

]
