from django.urls import path
from django.views.generic import TemplateView
from .views import HomeView, ProfileEditView, PostCreate, AllListView, MyListView,ContentDeleteView
from django.shortcuts import redirect

app_name = 'snsapp'
urlpatterns = [
    path('', lambda request: redirect('snsapp:home', pk=1)),
    path('home/<int:pk>/', HomeView.as_view(), name='home'),
    path('edit_profile/', ProfileEditView.as_view(), name='edit_profile'),
    path('post_content/', PostCreate.as_view(), name='post_content'),
    path('all_post/', AllListView.as_view(), name='all_post'),
    path('my_post/', MyListView.as_view(), name='my_post'),
    path('delete/<int:pk>/', ContentDeleteView.as_view(), name='delete_content'),

    # PWA対応：sw.jsを提供
    path('sw.js', TemplateView.as_view(template_name="sw.js", content_type='application/javascript'), name='sw.js'),
]
