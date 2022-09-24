from django.contrib import admin
from student.models import Student
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.hashers import make_password


# Register your models here.


class StudentAdmin(admin.ModelAdmin):
    """
    创建StudentAdmin类，继承自admin.ModelAdmin
    """
    # 配置展示列表，在user板块下方列表展示
    list_display = ('student_num', 'name', 'class_name', 'teacher_name', 'gender', 'birthday')
    # 配置过滤查询字段，在User板块右侧显示过滤框
    list_filter = ('name', 'student_num')
    # 配置可以搜索的字段，在User板块下方显示搜索框
    search_fields = (['name', 'student_num'])
    readonly_fields = ("teacher",)  # 设置只读字段，不允许更改
    ordering = ('-created_at',)  # 定义列表现实的顺序，符号表示降序
    # 显示字段
    fieldsets = (
        (None, {
            'fields': ('student_num', 'name', 'gender', 'phone', 'birthday')
        }),
    )

    def save_model(self, request, obj, form, change):
        """
        添加student表时，同时添加到user表
        由于需要和teacher表级联，所以自动获取当前登陆的老师id作为teacher_id
        :param request:
        :param obj:
        :param form:
        :param change:
        :return:
        """
        if not change:
            user = User.objects.create(

                username=request.POST.get("student_num"),  # 学号作为用户登陆名
                password=make_password(settings.STUDENT_INIT_PASSWORD),
            )
            obj.user_id = user.id  # 获取新增用户的id
            obj.teacher_id = request.user.id  # 获取当前老师的id
            super().save_model(request, obj, form, change)  # 调用父类保存方法
            return

    def delete_queryset(self, request, queryset):
        """
        删除多条数据
        同时删除user表中数据
        由于使用的是批量删除，所以需要遍历delete_queryset 中的 queryset
        :param request:
        :param queryset:
        :return:
        """
        for obj in queryset:
            obj.user.delete()
            super().delete_model(request, obj)
            return

    def delete_model(self, request, obj):
        """
        删除单条记录
        同时删除user表中数据
        :param request:
        :param obj:
        :return:
        """
        super().delete_model(request, obj)
        if obj.user:
            obj.user.delete()
        return


# 绑定Student模型到StudentAdmin管理后台
admin.site.register(Student, StudentAdmin)
