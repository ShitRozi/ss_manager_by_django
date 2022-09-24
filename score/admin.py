from django.contrib import admin
from score.models import Score


class ScoreAdmin(admin.ModelAdmin):
    """
    创建ScoreAdmin类，继承自admin.ModelAdmin
    """
    # 配置展示列表，在Score板块下方列表显示
    list_display = ('title', "student_num", 'student', 'score')
    # 配置过滤查询字段，在Score板块右侧显示过滤框
    list_filter = ('title', 'student')
    # 配置可以搜索的字段，在Score板块下方显示搜索框
    # student是外键，管理student类，这里使用双下划线+属性名的方式搜索
    search_fields = (['title', 'student__name', 'student__student_num'])
    ordering = ('-created_at',)  # 定义列表显示的顺序，负号为降序
    fieldsets = (
        (None, {
            'fields': ('title', 'student', 'score')
        }),
    )


# 绑定Scope模型到ScoreAdmin管理后台
admin.site.register(Score, ScoreAdmin)
