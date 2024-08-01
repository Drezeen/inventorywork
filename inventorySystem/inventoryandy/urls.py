from django.urls import path
from .views import delete_inventory, inventoryandy_list, per_product_view, add_product, update_inventory, dashboard
from .views import handle_scan
from . import views

urlpatterns = [
    path("", inventoryandy_list, name="inventoryandy_list"),
    path('handle_scan/', handle_scan, name='handle_scan'),
    path("per_product/<int:pk>", per_product_view, name="per_product"),
    path("add_inventory/", add_product, name="add_inventory"),
    path("delete/<int:pk>", delete_inventory, name="delete_inventory"),
    path("update/<int:pk>", update_inventory, name="update_inventory"),
    path('add_inventory/', views.add_product, name='add_product'),
    path("dashboard/", dashboard, name="dashboard")
]

