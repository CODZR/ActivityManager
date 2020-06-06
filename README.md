# ActivityManager
## 项目简介
&emsp;&emsp;社团活动教室借用后台管理系统，数据库使用sqlite（说是数据较少时效率更高），
根据开发时间先后有schedule、activity、user和classroomApi四个app，
前三个使用django配合xadmin（基于layui），classroomApi(v1.5以后) 
则是基于drf(django restframework)写的api接口。时间问题略显粗糙且仍有许多bug。详情请看[演示网址](106.53.21.189:8000/index/)。

## GitHub 
[源码网址](https://github.com/dzr201732120115/ActivityManager) <br>
[演示地址](106.53.21.189:8000/index/) <br>
> git log --pretty=oneline
**tags:** 
* v1.4(activityApp) 
* v1.5(classroomApi)

## 快速本地部署（pycharm）
1. >pip install django 
2. >pip install djangorestframework(v1.5以后)
3. >python manage.py makemigrations
4. >python manage.py migrate
5. 使用database插入用户、教室等数据或者去网页里增删查改

## 预期改进
* 优化登录注册界面，验证码等，增加权限、认证、限流组件等，加强网站安全性
* 引入echarts图表，使用pandas中的dataframe处理数据并形成对应图表
* 界面、逻辑优化，学习更好的提高代码可读性、可扩展性、网站的并发性、安全性等
* 待补充