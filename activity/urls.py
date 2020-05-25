from django.urls import re_path, path
from activity import views

urlpatterns = [
	path('login/', views.login),
	path('logout/<str:username>', views.logout),
	path('index/', views.index),
	path('activity/', views.activity),
	path('activity/add/', views.add_activity),
	path('activity/delete/<int:act_id>', views.delete_activity),
	path('activity/search/', views.search_activity),
	path('activity/update/<int:act_id>', views.update_activity),
	path('activity/check1/<int:act_id>', views.check_status1),
	path('activity/check2/<int:act_id>', views.check_status2),
	path('fail/', views.fail),
	path('log/', views.log),

]
