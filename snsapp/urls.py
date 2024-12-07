from django.urls import path
from django.views.generic import TemplateView
from .views import HomeView, ProfileEditView

app_name = 'accounts'
urlpatterns = [
    path('home/<int:pk>/', HomeView.as_view(), name='home'),
    path('edit_profile/', ProfileEditView.as_view(), name='edit_profile'),

    # PWA対応：sw.jsを提供
    path('sw.js', TemplateView.as_view(template_name="sw.js", content_type='application/javascript'), name='sw.js'),
]
