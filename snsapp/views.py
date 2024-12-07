from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView # 追加
from django.contrib.auth.mixins import LoginRequiredMixin # 追加
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseRedirect

import random

from .models import User, Content
from .forms import ProfileForm

def get_random_content_pk():
    content_count = Content.objects.count()  # Contentの件数を取得
    if content_count == 0:
        return None  # Contentが1件もない場合はNoneを返す
    random_index = random.randint(0, content_count - 1)  # ランダムなインデックスを取得
    random_content = Content.objects.all()[random_index]  # インデックスに対応するContentを取得
    return random_content.pk

class HomeView(LoginRequiredMixin, DetailView):
    model = Content
    template_name = 'account/home.html'
   
    def get_object(self, queryset=None):
        # URLからpkを取得してオブジェクトを取得
        pk = self.kwargs.get('pk')  # URLのパラメータからpkを取得
        return Content.objects.get(pk=pk)

    def post(self, request, *args, **kwargs):
        # ボタンが押された場合にランダムなContentのpkを取得
        random_pk = get_random_content_pk()
        if random_pk:
            # ランダムに選ばれたpkの詳細ページへリダイレクト
            return redirect('accounts:home', pk=random_pk)  # 'content_detail' はURLの名前に合わせて変更
        else:
            # Contentが存在しない場合のエラーハンドリング
            return HttpResponseRedirect(reverse('account/edit_profile.html'))  # 例えば、homeページに戻る
   
   
class ProfileEditView(LoginRequiredMixin, UpdateView): # 追加
  template_name = 'account/edit_profile.html'
  model = User
  form_class = ProfileForm
  success_url = '/siniagram/home/'
  def get_object(self):
      return self.request.user