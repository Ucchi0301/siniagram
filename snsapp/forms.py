from django import forms
from .models import User
from django.core.exceptions import ValidationError

class ProfileForm(forms.ModelForm):
   def __init__(self, *args, **kwargs):
       super(ProfileForm, self).__init__(*args, **kwargs)
       for field in self.fields.values():  # bootstrapで使用するform-controlクラス
           field.widget.attrs['class'] = 'form-control'
           
   class Meta:
       model = User
       fields = ('nickname', 'email', 'avatar')
       help_texts = {
           'nickname': "ユーザーネーム",
           'email': None,
       }

class CustomSignupForm(forms.Form):
    email = forms.EmailField(label='メールアドレス')
    password1 = forms.CharField(widget=forms.PasswordInput, label='パスワード')
    password2 = forms.CharField(widget=forms.PasswordInput, label='パスワード (再入力)')
    nickname = forms.CharField(max_length=30, label='ニックネーム', required=True)
    
    is_sinia = forms.BooleanField(label="シニアの人はチェック")
    
    
    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname')
        is_sinia = self.cleaned_data.get('is_senior')
        if not nickname:
            raise ValidationError("ニックネームを入力してください。")
        if User.objects.filter(nickname=nickname).exists():
            raise ValidationError("このニックネームはすでに使用されています。")
        return nickname

    def signup(self, request, user):
        nickname = self.cleaned_data['nickname']
        is_sinia = self.cleaned_data['is_sinia']
        user.nickname = nickname
        user.is_senior = is_sinia
        user.save()
        return user