from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.core.cache import cache
from django.contrib.messages.views import SuccessMessageMixin
import random
from .models import User, Content
from .forms import ProfileForm, PostForm
from django.contrib import messages


def get_random_content_pk(current_pk=None):
    # 現在のコンテンツを除外するクエリセットを作成
    content_queryset = Content.objects.all()
    if current_pk is not None:
        content_queryset = content_queryset.exclude(pk=current_pk)
    
    # 利用可能なコンテンツの数を取得
    content_count = content_queryset.count()
    
    if content_count == 0:
        return None  # 他のコンテンツがない場合
    
    # ランダムなインデックスを取得
    random_index = random.randint(0, content_count - 1)
    random_content = content_queryset[random_index]
    return random_content.pk

class HomeView(LoginRequiredMixin, DetailView):
    model = Content
    template_name = 'account/home.html'
   
    def get_object(self, queryset=None):
        # URLからpkを取得してオブジェクトを取得
        pk = self.kwargs.get('pk')
        
        try:
            return Content.objects.get(pk=pk)
        except Content.DoesNotExist:
            # コンテンツが存在しない場合、ランダムなコンテンツを取得
            random_pk = get_random_content_pk()
            if random_pk:
                return Content.objects.get(pk=random_pk)
            return redirect(reverse('accounts:post_content'))

    def get(self, request, *args, **kwargs):
        # pkがない場合、ランダムなコンテンツを取得
        if 'pk' not in kwargs:
            random_pk = get_random_content_pk()
            if random_pk:
                return redirect('accounts:home', pk=random_pk)
            return redirect(reverse('accounts:post_content'))
        
        # 通常のDetailViewの処理を継続
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # 現在のコンテンツのpkを取得
        current_pk = kwargs.get('pk')
        
        # キャッシュを使用してクリック回数を追跡
        user = request.user
        cache_key = f'user_click_count_{user.id}'
        
        # キャッシュからクリック回数を取得、なければ0から開始
        click_count = cache.get(cache_key, 0) + 1
        
        # キャッシュに更新したクリック回数を保存（1時間有効）
        cache.set(cache_key, click_count, timeout=3600)
        
        # 10回に1回、データベースを更新
        if click_count % 10 == 0:
            user.button_click_count = click_count
            user.save()
        
        # 現在のコンテンツと異なるランダムなpkを取得
        random_pk = get_random_content_pk(current_pk)
        
        if random_pk:
            # ランダムに選ばれたコンテンツのページにリダイレクト
            return redirect('accounts:home', pk=random_pk)
        else:
            # 他のコンテンツがない場合はプロフィール編集ページにリダイレクト
            return redirect(reverse('accounts:post_content'))
   
class ProfileEditView(LoginRequiredMixin, UpdateView):
    template_name = 'account/edit_profile.html'
    model = User
    form_class = ProfileForm
    success_url = '/siniagram/home/'
    
    def get_object(self):
        return self.request.user
    
    
class PostCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Content
    form_class = PostForm
    template_name = 'account/toukou.html'
    success_url = reverse_lazy('accounts:post_content')
    success_message = "投稿が完了しました！"  # SuccessMessageMixinでメッセージを自動で設定

    def form_valid(self, form):
        # ログインしているユーザーを作成者として設定
        form.instance.created_by = self.request.user
        form.save()
        # メッセージの表示は SuccessMessageMixin によって自動で行われる
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)  # フォームのエラーを表示
        return super().form_invalid(form)


class AllListView(ListView, LoginRequiredMixin):
    model = Content
    template_name = 'account/list.html' 
    login_url = 'accounts/'
    
    def get_queryset(self):
        # 新しい順でソート
        return Content.objects.all().order_by('-created_at')

class MyListView(ListView, LoginRequiredMixin):
    model = Content
    template_name = 'account/my-list.html'
    
    def get_queryset(self):
        # 自分が作成したコンテンツのみを新しい順で取得
        return Content.objects.filter(created_by=self.request.user).order_by('-created_at')
   
   
class ContentDeleteView(DeleteView):
    model = Content
    template_name = 'content_confirm_delete.html'
    success_url = reverse_lazy('accounts:my_post')