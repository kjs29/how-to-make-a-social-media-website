from django.urls import path
from . import views
urlpatterns = [
    path('',views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view,name='logout'),
    path('post/<int:pk>/', views.detail_view, name='detail'),
    path('post/new/', views.create_view, name='create'),
    path('post/edit/<int:pk>/', views.edit_view, name='edit'),
    path('like_post/<pk>', views.like_post, name='like_post'),
    path('profile/<int:pk>/', views.profile_view, name='profile'),
    path('profile/<int:pk>/authenticate/', views.authenticate_view, name='authenticate'),
    path('profile/edit/<int:pk>/', views.profile_edit_view, name='profile_edit'),
    path('comment/<int:pk>/', views.comment, name='comment'),
    path('comment/delete/<int:pk_post>/<int:pk_comment>/', views.delete_comment, name='delete_comment'),
]