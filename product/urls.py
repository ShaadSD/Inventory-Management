from django.urls import path
from . import views

urlpatterns = [
    path('product_list/', views.product_list, name='product_list'),
    path('add/', views.add_product, name='add_product'),
    path('products/edit/<int:pk>/', views.product_edit, name='product_edit'),
    path('products/delete/<int:pk>/', views.product_delete, name='product_delete'),
    path('sales_list/', views.sales_list, name='sales_list'),
    path('sales/add/', views.add_sale, name='add_sale'),
    path('sales/edit/<int:sale_id>/', views.edit_sale, name='edit_sale'),
    path('sales/delete/<int:sale_id>/', views.delete_sale, name='delete_sale'),
    path('stock_list/', views.stock_list, name='stock_list'),
    path('stock/in/', views.stock_in, name='stock_in'),
    path('stock/out/', views.stock_out, name='stock_out'),
    path('reports/products/pdf/', views.download_product_report, name='download_product_report'),
    path('reports/sales/pdf/', views.download_sales_report, name='download_sales_report'),
    path('report/', views.reports, name='report'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
