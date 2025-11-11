# app_Libreria/urls.py - REEMPLAZAR COMPLETAMENTE

from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio_libreria, name='inicio_libreria'),
    
    # Rutas para Autores
    path('autores/agregar/', views.agregar_autor, name='agregar_autor'),
    path('autores/', views.ver_autores, name='ver_autores'),
    path('autores/editar/<int:autor_id>/', views.actualizar_autor, name='actualizar_autor'),
    path('autores/editar/guardar/<int:autor_id>/', views.realizar_actualizacion_autor, name='realizar_actualizacion_autor'),
    path('autores/borrar/<int:autor_id>/', views.borrar_autor, name='borrar_autor'),
    
    # Rutas para Libros
    path('libros/agregar/', views.agregar_libro, name='agregar_libro'),
    path('libros/', views.ver_libros, name='ver_libros'),
    path('libros/editar/<int:libro_id>/', views.actualizar_libro, name='actualizar_libro'),
    path('libros/editar/guardar/<int:libro_id>/', views.realizar_actualizacion_libro, name='realizar_actualizacion_libro'),
    path('libros/borrar/<int:libro_id>/', views.borrar_libro, name='borrar_libro'),
    
    # Rutas para Ventas
    path('ventas/agregar/', views.agregar_venta, name='agregar_venta'),
    path('ventas/', views.ver_ventas, name='ver_ventas'),
    path('ventas/editar/<int:venta_id>/', views.actualizar_venta, name='actualizar_venta'),
    path('ventas/editar/guardar/<int:venta_id>/', views.realizar_actualizacion_venta, name='realizar_actualizacion_venta'),
    path('ventas/borrar/<int:venta_id>/', views.borrar_venta, name='borrar_venta'),
]