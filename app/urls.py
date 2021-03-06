from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.product_list, name='product_list'),
    url(r'^post/all/$', views.post_list, name='post_list'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post/(?P<pk>[0-9]+)/remove/$', views.post_remove, name='post_remove'),
    url(r'^signup/$', views.signup, name='signup'),    
    url(r'^account/settings/$', views.update_profile, name='settings_profile'),  
    url(r'^account/delete/$', views.delete_profile, name='delete_profile'),      
    url(r'^users/$', views.users_list, name='users_list'),      
    url(r'^product/new/$', views.product_new, name='product_new'),      
    url(r'^product/(?P<pk>[0-9]+)/$', views.product_detail, name='product_detail'),      
    url(r'^product/(?P<pk>[0-9]+)/edit/$', views.product_edit, name='product_edit'),      
    url(r'^product/(?P<pk>[0-9]+)/remove/$', views.product_remove, name='product_remove'),      
    url(r'^product/all/$', views.product_list, name='product_list'),
    url(r'^product/(?P<user>[0-9]+)/all/$', views.product_list, name='product_list'),
    url(r'^product/mine/$', views.my_products, name='my_products'),
    url(r'^product/(?P<product>[0-9]+)/bidding/$', views.bidding, name='bidding'),    
    url(r'^product/(?P<product>[0-9]+)/buy_now/$', views.buy_now, name='buy_now'),    
    url(r'^product/(?P<pk>[0-9]+)/share/$', views.share_email, name='share_email'),    
    url(r'^product/purchased/$', views.purchase_history, name='purchase_history'),
    url(r'^product/search/$', views.search_list, name='search_list'),
    url(r'^product/search/advanced/$', views.advanced_search, name='advanced_search'),
    url(r'^category/new/$', views.category_new, name='category_new'),

    # API
    url(r'^api/get_categories/', views.get_categories, name='get_categories'),
    url(r'^api/rates/products/', views.rate_product, name='rate_product'),

]