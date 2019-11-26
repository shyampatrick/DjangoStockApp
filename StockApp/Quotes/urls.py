from django.urls import path
from Quotes import views

urlpatterns = [path('', views.Quotes, name="Quotes"),
path('singlepage/', views.singlepage, name="singlepage"),
path('add_stock/', views.add_stock, name="add_stock"),
path('delete/<stock_id>/', views.delete, name="delete"),
path('delete_stock/', views.delete_stock, name="delete_stock"),
path('singlepage_delete/<stock_id>', views.singlepage_delete, name="singlepage_delete"),
path('singlepage_addstock/', views.singlepage_addstock, name="singlepage_addstock"),]

