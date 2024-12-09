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
    nickname = forms.CharField(max_length=8, label='ニックネーム', required=True)
    email = forms.EmailField(label='メールアドレス')
    password1 = forms.CharField(widget=forms.PasswordInput, label='パスワード')
    password2 = forms.CharField(widget=forms.PasswordInput, label='パスワード (再入力)')
    is_sinia = forms.BooleanField(label="お年寄りの方はチェック", required=False)
    avatar = forms.ImageField(label='プロフィール画像', required=False)
    
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
        avatar = self.cleaned_data.get('avatar')  # 画像を取得
        
        user.nickname = nickname
        user.is_senior = is_sinia
        if avatar:
            user.avatar = avatar  # avatarが存在すればユーザーに設定
        user.save()
        return user
    
    
from .models import Content

class PostForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control ml-3',
            'placeholder': 'タイトルを入力(18字以内)',
            'style': 'height: 150px; padding-top: 5px; resize: none; border: none; font-size: 20px; outline: none;',
            'focus': 'this.style.outline="none"',  # インラインスタイルでもOK
        }),
        required=True,  # 必須項目に設定
        max_length=18,  # 18文字以内に制限
        error_messages={'required': 'タイトルは必須です', 'max_length': 'タイトルは18文字以内で入力してください'}
    )
    image = forms.ImageField(
        required=True,  # 必須項目に設定
        error_messages={'required': '画像は必須です'}
    )

    class Meta:
        model = Content
        fields = ['title', 'image']
