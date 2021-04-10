from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('orders/', views.OrderListView.as_view(), name='orders'),
    path('orders/create', views.OrderCreateView.as_view(), name='orders/create'),
    path('orders/<int:pk>', views.OrderUpdateView.as_view(), name='orders/detail'),
    path('orders/delete/<int:pk>', views.OrderDeleteView.as_view(), name="orders/delete"),
    path('profile/<int:pk>', views.UserProfileView.as_view(), name="profile"),
    path('masters/', views.MasterListView.as_view(), name="masters"),
    path('masters/<int:pk>', views.MasterUpdateView.as_view(), name="masters/detail"),
    path('masters/delete/<int:pk>', views.MasterDeleteView.as_view(), name="masters/delete"),
]
