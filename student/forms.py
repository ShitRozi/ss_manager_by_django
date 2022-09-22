from django import forms
from django.contrib.auth.models import User


class StudentLoginForm(forms.Form):
    student_num = forms.CharField(
        label='学号',
        required=True,
        max_length=11,
        widget=forms.TextInput(attrs={
            'class': "form-control mb-0",
            'placeholder': '请输入学号'
        }),
        error_messages={
            'required': "学号不能为空",
            "max_length": '长度不能超过50个字符',
        }
    )
    password = forms.CharField(
        label='密码',
        required=True,
        min_length=6,
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': "form-control mb-0",
            'placeholder': '请输入密码'
        }),
        error_messages={
            'required': "学号不能为空",
            "max_length": '长度不能超过50个字符',
            "min_length": '长度不能少于6个字符',
        }
    )

    # 二次验证函数的名字是固定写法，以clean_开头，后面跟上字段的变量
    def clean_student_num(self):
        # 通过了validators的验证后，在进行二次验证
        student_num = self.cleaned_data['student_num']
        try:
            User.objects.get(username=student_num)  # 使用student_num获取django用户
        except User.DoesNotExist:
            raise forms.ValidationError("学号不存在", 'invalid')
        else:
            return student_num
