class ListaProductosViews(LoginRequiredMixin, ExportMixin, SingleTableView):
    model = Productos
    table_class = ProductosTable
    template_name = "inventario/listaProductos.html"
    context_object_name = "productos"
    paginate_by = 10
    SingleTableView.table_pagination = False

    def post(self, request):
        # Verificar si es una solicitud AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                data = json.loads(request.body.decode('utf-8'))
                nombre = data.get('nombre')
                descripcion = data.get('descripcion', '')
                precio = data.get('precio')
                stock = data.get('stock')
                fecha_expiracion = data.get('fecha_expiracion')
                foto = data.get('foto')
                codigo_barras = data.get('codigo_barras')
                
                # Validar que el nombre no esté vacío
                if not nombre:
                    return JsonResponse({
                        'success': False,
                        'message': 'El nombre es obligatorio'
                    }, status=400)
                
                nuevo_producto = Productos(
                    nombre=nombre,
                    descripcion=descripcion,
                    precio=precio,
                    stock=stock,
                    fecha_expiracion=fecha_expiracion,
                    foto=foto,
                    codigo_barras=codigo_barras,
                    negocio_id=request.user.negocio.negocio_id,
                    categoria_id="",
                    unidad_id=""
                )
                nuevo_producto.save()
                
                return JsonResponse({
                    'success': True,
                    'message': 'Producto creada con éxito',
                    'producto': {
                        'producto_id': nuevo_producto.producto_id,
                        'nombre': nuevo_producto.nombre,
                        'categoria': nuevo_producto.categoria_id,
                        'precio': nuevo_producto.precio,
                        'stock': nuevo_producto.stock,
                        "unidad": nuevo_producto.unidad_id
                    }
                })
            except Exception as e:
                print(f'Error al guardar: {str(e)}')
                return JsonResponse({
                    'success': False,
                    'message': f'Error al guardar: {str(e)}'
                }, status=500)
        else:
            # Si no es AJAX, mantener el comportamiento original
            return super().get(request)
        
class ProductoDetalleViews(LoginRequiredMixin, View):
        
    def get(self, request, producto_id):
        try:
            producto = Productos.objects.get(producto_id=producto_id)
            return JsonResponse({
                'success': True,
                'producto': {
                    'producto_id': producto.producto_id,
                        'nombre': producto.nombre,
                        'categoria': producto.categoria_id,
                        'precio': producto.precio,
                        'stock': producto.stock,
                        "unidad": producto.unidad_id
                }
            })
        except Productos.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Categoria no encontrada'
            }, status=404)
        