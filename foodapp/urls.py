from django.urls import path
from .import views

urlpatterns = [ 
    path('', views.home_page, name='home_page'),
    path('manager/', views.manager, name='manager'),
    path('recommend/', views.recommend, name='recommend'),
    path('recommend_user/', views.recommend_user, name='recommend_user'),
    path('manager_cat_id/<int:id>', views.manager_cat_id, name='manager_cat_id'),
    path('cat_id/<int:id>', views.cat_id, name='cat_id'),
    path('orders/', views.order_page, name='order_page'),
    path('confirm/', views.confirm_order, name='confirm_order'),
    path('confirm_code/', views.confirm_code, name='confirm_code'),
    path('login/', views.login_page, name='login_page'),
    path('logout/', views.logout, name='logged_out'),
    path('signup/', views.signup_page, name='signup_page'),
    path('register_user/', views.register_user, name='register_user'),
    
]
