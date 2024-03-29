from django import forms
from django.contrib.auth.models import User
from .models import Profile


# 用户登录
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


# 注册用户
class UserRegisterForm(forms.ModelForm):
    # 复写 User 密码
    password = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'email')

    # 检验两次输入的密码是否一致
    def clean_password2(self):
        data = self.cleaned_data
        if data['password'] == data['password2']:
            return data.get('password')
        else:
            raise forms.ValidationError('密码输入不一致，请重新输入！')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'avatar', 'bio')