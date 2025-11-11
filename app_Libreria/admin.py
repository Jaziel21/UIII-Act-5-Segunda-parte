# app_Libreria/admin.py - REEMPLAZAR COMPLETAMENTE

from django.contrib import admin
from .models import Autor, Libro, Venta

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'nacionalidad', 'fecha_nacimiento', 'email', 'activo', 'created_at']
    list_filter = ['activo', 'nacionalidad', 'created_at']
    search_fields = ['nombre', 'email', 'nacionalidad']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'isbn', 'genero', 'precio', 'stock', 'disponible']
    list_filter = ['genero', 'fecha_publicacion']
    search_fields = ['titulo', 'isbn']
    filter_horizontal = ['autores']

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ['id', 'libro', 'cantidad', 'total', 'fecha_venta', 'estado']
    list_filter = ['estado', 'fecha_venta']