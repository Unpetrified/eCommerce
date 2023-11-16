from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.Store.as_view(), name='store'),
    path('view_item/<int:id>', views.View.as_view(), name='view'),
    path('cart', views.Cart.as_view(), name='cart'),
    path('checkout', views.Checkout.as_view(), name='checkout'),
    path('register', views.Register.as_view(), name='register'),
    path('addtocart', views.UpdateCart.as_view(), name='update'),
    path('login', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('password_reset', auth_views.PasswordResetView.as_view(template_name='emails/reset.html'), name='password_reset'),
    path('password_reset/done', auth_views.PasswordResetDoneView.as_view(template_name='emails/reset_done.html'), name='password_reset_done'),
    path('password_reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='emails/login.html'), name='password_reset_confirm'),
    path('<str:name>', views.Categories.as_view(), name='categories'),
]
