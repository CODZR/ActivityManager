from django.shortcuts import render

from userApp.models import User


# def check_token(username):
# 	user_obj = User.objects.get(username=username)
# 	if user_obj.usertoken.token:  # 登陆过已经生成了token
# 		print('done')
# 		return True
# 	else:
# 		return False
