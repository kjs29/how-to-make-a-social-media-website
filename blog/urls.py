from django.urls import path
from . import views
urlpatterns = [
    path('',views.home, name='home'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('thankyou/', views.thankyou, name='thankyou'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view,name='logout'),
    path('post/<int:pk>/', views.detail_view, name='detail'),
    path('post/new/', views.create_view, name='create'),
    path('post/edit/<int:pk>/', views.edit_view, name='edit'),
    path('post/delete/<int:pk>/', views.delete_post_view, name='delete_post'),
    path('post/delete_photo/<int:pk>/', views.delete_photo_view, name='delete_photo'),
    path('like_post/<pk>', views.like_post_view, name='like_post'),
    path('profile/<int:pk>/', views.profile_view, name='profile'),
    path('profile/<int:pk>/authenticate/', views.authenticate_view, name='authenticate'),
    path('profile/edit/<int:pk>/', views.profile_edit_view, name='profile_edit'),
    path('profile/delete/<int:pk>/', views.delete_user_view, name= 'delete_user'),
    path('comment/<int:pk>/', views.comment_view, name='comment'),
    path('comment/delete/<int:pk_post>/<int:pk_comment>/', views.delete_comment_view, name='delete_comment'),
]