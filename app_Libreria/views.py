# app_Libreria/views.py - REEMPLAZAR COMPLETAMENTE

from django.shortcuts import render, redirect, get_object_or_404
from .models import Autor, Libro, Venta
from django.utils import timezone

# ==========================================
# VISTAS PARA PÁGINA PRINCIPAL
# ==========================================

def inicio_libreria(request):
    contexto = {
        'titulo': 'Sistema de Administración Libreria AJMG 1194',
        'now': timezone.now()
    }
    return render(request, 'inicio.html', contexto)

# ==========================================
# VISTAS PARA MODELO AUTOR
# ==========================================

def agregar_autor(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        nacionalidad = request.POST.get('nacionalidad')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        fecha_fallecimiento = request.POST.get('fecha_fallecimiento') or None
        biografia = request.POST.get('biografia')
        email = request.POST.get('email')
        activo = True if request.POST.get('activo') == 'on' else False

        Autor.objects.create(
            nombre=nombre,
            nacionalidad=nacionalidad,
            fecha_nacimiento=fecha_nacimiento,
            fecha_fallecimiento=fecha_fallecimiento,
            biografia=biografia,
            email=email,
            activo=activo,
        )
        return redirect('ver_autores')

    return render(request, 'autor/agregar_autor.html')

def ver_autores(request):
    autores = Autor.objects.all()
    return render(request, 'autor/ver_autores.html', {'autores': autores})

def actualizar_autor(request, autor_id):
    autor = get_object_or_404(Autor, id=autor_id)
    return render(request, 'autor/actualizar_autor.html', {'autor': autor})

def realizar_actualizacion_autor(request, autor_id):
    autor = get_object_or_404(Autor, id=autor_id)
    if request.method == 'POST':
        autor.nombre = request.POST.get('nombre')
        autor.nacionalidad = request.POST.get('nacionalidad')
        autor.fecha_nacimiento = request.POST.get('fecha_nacimiento')
        fecha_fallecimiento = request.POST.get('fecha_fallecimiento') or None
        autor.fecha_fallecimiento = fecha_fallecimiento
        autor.biografia = request.POST.get('biografia')
        autor.email = request.POST.get('email')
        autor.activo = True if request.POST.get('activo') == 'on' else False
        autor.save()
        return redirect('ver_autores')
    return redirect('actualizar_autor', autor_id=autor_id)

def borrar_autor(request, autor_id):
    autor = get_object_or_404(Autor, id=autor_id)
    if request.method == 'POST':
        autor.delete()
        return redirect('ver_autores')
    return render(request, 'autor/borrar_autor.html', {'autor': autor})

# ==========================================
# VISTAS PARA MODELO LIBRO
# ==========================================

def agregar_libro(request):
    if request.method == 'POST':
        try:
            # Procesar formulario manualmente
            titulo = request.POST.get('titulo')
            isbn = request.POST.get('isbn')
            genero = request.POST.get('genero')
            fecha_publicacion = request.POST.get('fecha_publicacion')
            precio = request.POST.get('precio')
            stock = request.POST.get('stock')
            descripcion = request.POST.get('descripcion')
            autores_ids = request.POST.getlist('autores')
            
            # Crear el libro
            libro = Libro.objects.create(
                titulo=titulo,
                isbn=isbn,
                genero=genero,
                fecha_publicacion=fecha_publicacion,
                precio=precio,
                stock=stock,
                descripcion=descripcion
            )
            
            # Manejar relación ManyToMany con autores
            if autores_ids:
                autores = Autor.objects.filter(id__in=autores_ids)
                libro.autores.set(autores)
            
            return redirect('ver_libros')
            
        except Exception as e:
            # En caso de error, mostrar el formulario nuevamente
            autores = Autor.objects.filter(activo=True)
            generos = Libro.GENEROS
            return render(request, 'libro/agregar_libro.html', {
                'autores': autores,
                'generos': generos,
                'error': 'Error al crear el libro. Verifique los datos.'
            })
    
    # GET request - mostrar formulario
    autores = Autor.objects.filter(activo=True)
    generos = Libro.GENEROS
    return render(request, 'libro/agregar_libro.html', {
        'autores': autores,
        'generos': generos
    })

def ver_libros(request):
    libros = Libro.objects.all().prefetch_related('autores')
    return render(request, 'libro/ver_libros.html', {'libros': libros})

def actualizar_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    autores = Autor.objects.filter(activo=True)
    generos = Libro.GENEROS
    
    return render(request, 'libro/actualizar_libro.html', {
        'libro': libro,
        'autores': autores,
        'generos': generos
    })

def realizar_actualizacion_libro(request, libro_id):
    if request.method == 'POST':
        try:
            libro = get_object_or_404(Libro, id=libro_id)
            
            # Actualizar campos
            libro.titulo = request.POST.get('titulo')
            libro.isbn = request.POST.get('isbn')
            libro.genero = request.POST.get('genero')
            libro.fecha_publicacion = request.POST.get('fecha_publicacion')
            libro.precio = request.POST.get('precio')
            libro.stock = request.POST.get('stock')
            libro.descripcion = request.POST.get('descripcion')
            
            libro.save()
            
            # Actualizar relación ManyToMany con autores
            autores_ids = request.POST.getlist('autores')
            if autores_ids:
                autores = Autor.objects.filter(id__in=autores_ids)
                libro.autores.set(autores)
            else:
                # Si no se seleccionaron autores, limpiar la relación
                libro.autores.clear()
            
            return redirect('ver_libros')
            
        except Exception as e:
            # Regresar a la página de actualización con error
            libro = get_object_or_404(Libro, id=libro_id)
            autores = Autor.objects.filter(activo=True)
            generos = Libro.GENEROS
            return render(request, 'libro/actualizar_libro.html', {
                'libro': libro,
                'autores': autores,
                'generos': generos,
                'error': 'Error al actualizar el libro.'
            })
    
    return redirect('actualizar_libro', libro_id=libro_id)

def borrar_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    
    if request.method == 'POST':
        libro.delete()
        return redirect('ver_libros')
    
    return render(request, 'libro/borrar_libro.html', {'libro': libro})

def agregar_venta(request):
    if request.method == 'POST':
        try:
            # Procesar formulario manualmente
            libro_id = request.POST.get('libro')
            cantidad = int(request.POST.get('cantidad'))
            precio_unitario = float(request.POST.get('precio_unitario'))
            cliente_nombre = request.POST.get('cliente_nombre')
            cliente_email = request.POST.get('cliente_email')
            estado = request.POST.get('estado')
            
            libro = Libro.objects.get(id=libro_id)
            
            # Verificar stock disponible
            if libro.stock < cantidad:
                libros = Libro.objects.filter(stock__gt=0)
                return render(request, 'venta/agregar_venta.html', {
                    'libros': libros,
                    'error': f'Stock insuficiente. Solo hay {libro.stock} unidades disponibles.'
                })
            
            # Crear la venta
            venta = Venta.objects.create(
                libro=libro,
                cantidad=cantidad,
                precio_unitario=precio_unitario,
                cliente_nombre=cliente_nombre,
                cliente_email=cliente_email,
                estado=estado
            )
            
            # Actualizar stock del libro
            libro.stock -= cantidad
            libro.save()
            
            return redirect('ver_ventas')
            
        except Exception as e:
            libros = Libro.objects.filter(stock__gt=0)
            return render(request, 'venta/agregar_venta.html', {
                'libros': libros,
                'error': f'Error al crear la venta: {str(e)}'
            })
    
    # GET request - mostrar formulario
    libros = Libro.objects.filter(stock__gt=0)
    return render(request, 'venta/agregar_venta.html', {'libros': libros})

def ver_ventas(request):
    ventas = Venta.objects.all().select_related('libro')
    return render(request, 'venta/ver_ventas.html', {'ventas': ventas})

def actualizar_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    libros = Libro.objects.all()
    
    return render(request, 'venta/actualizar_venta.html', {
        'venta': venta,
        'libros': libros
    })

def realizar_actualizacion_venta(request, venta_id):
    if request.method == 'POST':
        try:
            venta = get_object_or_404(Venta, id=venta_id)
            libro_anterior = venta.libro
            cantidad_anterior = venta.cantidad
            
            # Obtener nuevos valores
            libro_id = request.POST.get('libro')
            cantidad = int(request.POST.get('cantidad'))
            precio_unitario = float(request.POST.get('precio_unitario'))
            cliente_nombre = request.POST.get('cliente_nombre')
            cliente_email = request.POST.get('cliente_email')
            estado = request.POST.get('estado')
            
            libro_nuevo = Libro.objects.get(id=libro_id)
            
            # Manejar cambios en libro y cantidad
            if libro_anterior != libro_nuevo or cantidad != cantidad_anterior:
                # Restaurar stock del libro anterior
                libro_anterior.stock += cantidad_anterior
                libro_anterior.save()
                
                # Verificar stock del nuevo libro
                if libro_nuevo.stock < cantidad:
                    libros = Libro.objects.all()
                    return render(request, 'venta/actualizar_venta.html', {
                        'venta': venta,
                        'libros': libros,
                        'error': f'Stock insuficiente. Solo hay {libro_nuevo.stock} unidades disponibles.'
                    })
                
                # Actualizar stock del nuevo libro
                libro_nuevo.stock -= cantidad
                libro_nuevo.save()
            
            # Actualizar la venta
            venta.libro = libro_nuevo
            venta.cantidad = cantidad
            venta.precio_unitario = precio_unitario
            venta.cliente_nombre = cliente_nombre
            venta.cliente_email = cliente_email
            venta.estado = estado
            venta.save()  # Esto actualiza automáticamente el total
            
            return redirect('ver_ventas')
            
        except Exception as e:
            venta = get_object_or_404(Venta, id=venta_id)
            libros = Libro.objects.all()
            return render(request, 'venta/actualizar_venta.html', {
                'venta': venta,
                'libros': libros,
                'error': f'Error al actualizar la venta: {str(e)}'
            })
    
    return redirect('actualizar_venta', venta_id=venta_id)

def borrar_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    
    if request.method == 'POST':
        # Restaurar stock antes de eliminar
        libro = venta.libro
        libro.stock += venta.cantidad
        libro.save()
        
        venta.delete()
        return redirect('ver_ventas')
    
    return render(request, 'venta/borrar_venta.html', {'venta': venta})