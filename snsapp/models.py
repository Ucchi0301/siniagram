from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth import get_user_model
from snsapp.manager import UserManager
from django.utils import timezone

# Userモデル


class User(AbstractBaseUser, PermissionsMixin):
    avatar = models.ImageField(upload_to='images', verbose_name='プロフィール画像', blank=True, null=True)
    nickname = models.CharField(max_length=150, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    is_senior = models.BooleanField(default=False)  # シニアかどうか
    button_click_count = models.PositiveIntegerField(default=0)  # ボタンクリック回数
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日
    last_login = models.DateTimeField(blank=True, null=True)  # 最終ログイン
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.nickname

# Contentモデル


class Content(models.Model):
    image = models.ImageField(upload_to="content_images/", blank=True, null=True)  # 画像
    title = models.CharField(max_length=255)  # タイトル
    description = models.TextField(blank=True, null=True)  # 説明
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日
    created_by = models.ForeignKey(User, related_name="content", on_delete=models.CASCADE)
    photo_date = models.DateField(blank=True, null=True)  # 撮影日

    def __str__(self):
        return self.title
