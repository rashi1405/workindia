from django.urls import path

from . import views

urlpatterns = [
    path('', views.MapView.as_view(), name='maps_list'),
    path('<int:map_id>/', views.MapView.as_view(), name='map_detail'),
    path('<int:map_id>/update/', views.MapView.as_view(), name='map_update'),
    path('<int:map_id>/delete/', views.MapView.as_view(), name='map_delete')
]