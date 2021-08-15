from django.urls import path
from . import views

app_name = "imagilink_app"

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('dashboard', views.Dashboard.as_view(), name='dashboard'),
    path('upload', views.Saveimagedata.as_view(), name="saveimagedata"),
    path('logout', views.Logout.as_view(), name='logout'),
    path('login', views.Login.as_view(), name='login'),
    path('accounts/login/', views.LoginRedirect.as_view(), name='login_redirect'),
    path('receive', views.ReceivePayload.as_view(), name='receive'),
    path('create', views.Create.as_view(), name='create'),
    path('preview/<str:link_id>', views.Preview.as_view(), name='preview'),
    path('delete', views.Delete.as_view(), name='delete'),
    path('u/<str:link_id>', views.TargetForwardView.as_view(), name='target_forward'),
]