from django.urls import path
from . import views
urlpatterns = [
    path('', views.index.as_view() , name="ShopHome"),
    path('product_detail/<int:pk>', views.product_detail.as_view(),name="product_detail"),
    path('send', views.send , name="send"),
    path('signup', views.signup.as_view() , name="signup"),
    path('login', views.login.as_view() , name="login"),
    path('logout', views.logout.as_view() , name="logout"),
    path('cart_list', views.cart_list , name="cart_list"),
    path('get_data', views.get_data, name='get_data'),
    path('popular_item', views.PopularItemListView.as_view(), name='popular_item'),
    path('newArrivals', views.newArrivals.as_view(), name='newArrivals'),
    path('delete_add_item', views.delete_add_item, name='delete_add_item'),
    path('boys', views.Boys.as_view(), name='boys'),
    path('Electronics', views.Electronics.as_view(), name='Electronics'),
    path('Accessories', views.Accessories.as_view(), name='Accessories'),
    path('girls', views.girls.as_view(), name='girls'),
    path('checkout', views.checkout.as_view(), name='checkout'), 
    path('payment', views.payment, name='payment'),
]
