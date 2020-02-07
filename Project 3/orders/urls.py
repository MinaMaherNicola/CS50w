from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('index', views.index, name='index'),
    path('<int:type_id>/indexf', views.indexf, name='indexf'),
    path("<int:item_id>", views.item, name='item'),
    path("<int:order_id>/<int:item_id>/selected_toppings", views.selected_toppings, name='selected_toppings'),
    path('cancel_item', views.cancel_item, name='cancel_item'),
    path('review_order', views.review_order, name='review_order'),
    path('<int:line_id>/delete_line', views.delete_line, name='delete_line'),
    path('delete_order', views.delete_order, name='delete_order'),
    path("<int:user_id>", views.profile, name='profile'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('new_user', views.new_user, name='new_user'),
    path('add_user', views.add_user, name='add_user')
]
