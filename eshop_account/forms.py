from captcha import fields
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.core import validators
from django.forms import ModelForm
from eshop_account.models import UserAddress, UserProfile
import phonenumber_field
from captcha.fields import ReCaptchaField


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'نام کاربری خود را وارد کنید', 'class': "input-ui pr-2 "}),
        label='نام کاربری'
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'رمز خود را وارد کنید', 'class': "input-ui pr-2"}),
        label='رمز عبور')


class RegisterForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'نام کاربری خود را وارد کنید', 'class': "input-ui pr-2 "}),
        label='نام کاربری',
        validators=[
            validators.MaxLengthValidator(20, 'نام کاربری نباید بیشتر از 20 کارکتر باشد'),
            validators.MinLengthValidator(4, 'نام کاربری نباید کمتر از 4 کارکتر باشد')
        ]
    )
    phone = forms.CharField(
        widget=forms.NumberInput(attrs={'placeholder': 'تلفن خود را وارد کنید', 'class': "input-ui pr-2"}),
        label='تلفن'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'ایمیل خود را وارد کنید', 'class': "input-ui pr-2 "}),
        label='ایمیل'

    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'رمز خود را وارد کنید', 'class': "input-ui pr-2 "}),
        label='رمز عبور')

    re_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'رمز خود را مجددا وارد کنید', 'class': "input-ui pr-2 "}),
        label='تکرار رمز عبور')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        is_exist_user_by_username = User.objects.filter(username=username).exists()
        if is_exist_user_by_username:
            raise forms.ValidationError('این نام کاربری از قبل وجود دارد')
        return username

    # def clean_phone(self):
    #     phone = self.cleaned_data.get('phone')
    #     is_exist_user_by_phone = User.objects.filter(phone=phone).exists()
    #     if is_exist_user_by_phone:
    #         raise forms.ValidationError('این شماره تلفن از قبل وجود دارد')
    #     return phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        is_exist_user_by_email = User.objects.filter(email=email).exists()
        if is_exist_user_by_email:
            raise forms.ValidationError('این ایمیل قبلا استفاده شده است')
        return email

    # def clean_phone(self):
    #     phone = self.cleaned_data.get('phone')
    #     is_exist_user_by_phone = UserProfile.phone = RegisterForm.phone
    #     if is_exist_user_by_phone:
    #         raise forms.ValidationError('این تلفن قبلا استفاده شده است ')
    #     else:
    #         UserProfile.phone = phone

    def clean_re_password(self):
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')
        if password != re_password:
            raise forms.ValidationError('رمزهای عبور باهم برابر نیستند')
        return password


class UserAddressForm(ModelForm):
    class Meta:
        model = UserAddress
        fields = ['full_name', 'phone', 'ostan', 'city', 'address', 'post_code']


# edit profile
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'national_code', 'image']


# edit profile
class UserUpdateForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        fields = ['first_name', 'last_name', 'email']

    password = None
