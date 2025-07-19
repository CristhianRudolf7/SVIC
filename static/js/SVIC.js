document.addEventListener("DOMContentLoaded", function () {
  fetch("/inventario/api/dashboard-data/")
    .then(response => response.json())
    .then(data => {
      window.ventasDia = data.ventas_dia;
      window.comprasPorcentaje = data.comprasPorcentaje;
      window.ventas_producto = data.ventas_producto;
      window.ventas_producto_cantidad = data.ventas_producto.cantidad;
      window.ventas_producto_nombre = data.ventas_producto.nombre;

      const eje_x = [];
      const empleadoNVentas = [];
      let n = 1;
      for (const emp of data.ventas_empleado) {
        empleadoNVentas.push(emp.cantidad);
        eje_x.push(n);
        n++;
      }

      window.eje_x = eje_x;
      window.empleadoNVentas = empleadoNVentas;

      if (window.jQuery?.AnalyticsDashboard) {
        window.jQuery.AnalyticsDashboard.init();
      }

    })
});
