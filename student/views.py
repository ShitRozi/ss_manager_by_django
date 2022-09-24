from django.contrib.auth import authenticate, login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

from score.models import Score
from student.forms import StudentLoginForm
from student.models import Student


# Create your views here.


class StudentLoginView(View):
    """
    学生登录页表单
    """

    def get(self, request):
        """
        显示登录页面
        """
        return render(request, 'login.html', {'form': StudentLoginForm()})  # 渲染模板

    def post(self, request):
        """
        提交登录页面表单
        """
        form = StudentLoginForm(request.POST)  # 接收Form表单
        # 验证表单
        if form.is_valid():
            student_num = request.POST['student_num']  # 获取学号
            password = request.POST['password']  # 获取密码
            user = authenticate(request, username=student_num, password=password)  # 授权校验
            if user is not None:  # 校验成功，获得返回用户信息
                login(request, user)  # 登录用户，设置登录session
                request.session['uid'] = user.id  # 设置用户名的session
                request.session['username'] = user.student.name  # 设置用户名的session
                request.session['student_num'] = user.student.student_num  # 设置用户名的session
                return HttpResponseRedirect('/')
            else:
                messages.add_message(request, messages.ERROR, '用户名和密码不匹配')  # 提示错误信息
        return render(request, 'login.html', {'form': form})  # 渲染模板


def logout(request):
    """
    退出登录
    :param request:
    :return:
    """
    django_logout(request)  # 清楚response的cookie和django_session中的记录
    return HttpResponseRedirect("/login")


@login_required
def index(request):
    """
    首页
    :param request:
    :return:
    """
    student_num = request.session.get("student_num", )  # 获取当前学生学号
    student = Student.objects.get(student_num=student_num)  # 根据学号查询学生信息
    scores = student.score_set.all()  # 获取该学生的所有分数
    return render(request, 'index.html', {'scores': scores})


@login_required
def score(request, score_id):
    """
    成绩详情
    :param request:
    :param score_id:
    :return:
    """
    try:
        score= Score.object.get(id=score_id)
    except:
        return render(request,'404.html', {"errmsg":'数据异常'})
    return render(request,'score.html',{'score':score})