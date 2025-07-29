!function (jq) {
    "use strict";
    function graficas() {
        this.$body = jq("body"),
        this.charts = []
    }
    graficas.prototype.initCharts = function () {
        window.Apex = {
            chart: {
                parentHeightOffset: 0, toolbar: {
                    show: !1
                }
            },
            grid: {
                padding: {
                    left: 0, right: 0
                }
            },
            colors: ["#727cf5", "#0acf97", "#fa5c7c", "#ffbc00"]
        };
        var nombre_dias = function () {
            var fecha_nueva = new Date();
            fecha_nueva.setDate(fecha_nueva.getDate() - 14);
            
            var nuevas_fechas = [];
            for (var i = 0; i < 15; i++) {
                var copia = new Date(fecha_nueva);
                nuevas_fechas.push(copia.getDate() + " " + copia.toLocaleString("es-pe", { month: 'short' }).replace('.', ''));
                fecha_nueva.setDate(fecha_nueva.getDate() + 1);
            }
            return nuevas_fechas;
        }(),        
        colores = ["#727cf5", "#0acf97", "#fa5c7c", "#ffbc00"],
        contenedor = jq("#cantidad-ventas").data("colors");
        contenedor && (colores = contenedor.split(","));

        var r = {
            chart: { height: 309, type: "area" },
            dataLabels: { enabled: !1 },
            stroke: { curve: "smooth", width: 4 },
            series: [{ name: "Ventas", data: window.ventasDia }],
            zoom: { enabled: !1 },
            legend: { show: !1 },
            colors: colores,
            xaxis: { type: "string", categories: nombre_dias, tooltip: { enabled: !1 }, axisBorder: { show: !1 }, labels: {} },
            yaxis: { labels: { formatter: function (e) { return e }, offsetX: -15 } },
            tooltip: { enabled: false },
            fill: {
                type: "gradient",
                gradient: { type: "vertical", shadeIntensity: 1, inverseColors: !1, opacityFrom: .45, opacityTo: .05, stops: [45, 100] }
            }
        };
        new ApexCharts(document.querySelector("#cantidad-ventas"), r).render();

        var circular = { 
            chart: { height: 203, type: "donut" }, 
            legend: { show: !1 }, stroke: { colors: ["transparent"] }, 
            series: window.comprasPorcentaje, labels: ["Pendiente", "En envio", "Entregado"], 
            tooltip: { enabled: false },
            colors: ["#fa5c7c", "#ffbc00", "#0acf97"], 
            responsive: [{ breakpoint: 480, options: { chart: { width: 200 }, legend: { position: "bottom" } } }]
        }; 
        new ApexCharts(document.querySelector("#totalCompras"), circular).render();

        r = {
            chart: { height: 150, type: "bar", stacked: !0 },
            plotOptions: { bar: { horizontal: !1, endingShape: "rounded", columnWidth: "22%", dataLabels: { position: "top" } } }, 
            dataLabels: { enabled: !0, offsetY: -24, style: { fontSize: "12px", colors: ["#98a6ad"] } }, 
            series: [{ name: "Ventas: ", data: window.empleadoNVentas }], 
            zoom: { enabled: !1 }, 
            legend: { show: !1 }, 
            colors: ["#0acf97"], 
            xaxis: { categories: window.eje_x, labels: { show: true }, axisTicks: { show: true }, axisBorder: { show: true } }, 
            tooltip: { enabled: false },
            yaxis: { labels: { show: true } }, 
            fill: { type: "gradient", 
                gradient: { inverseColors: !0, shade: "light", type: "horizontal", shadeIntensity: .25, gradientToColors: void 0, opacityFrom: 1, opacityTo: 1, stops: [0, 100, 100, 100] } }, 
        };
        new ApexCharts(document.querySelector("#ventasEmpleado"), r).render(); 

        r = {
            chart: { height: 257, type: "bar", stacked: !0 }, 
            plotOptions: { bar: { horizontal: !1, columnWidth: "40%" } }, 
            dataLabels: { enabled: !1 }, 
            stroke: { show: !0, width: 2, colors: ["transparent"] }, 
            series: [{ name: "Ventas", data: window.ventas_producto_cantidad }], 
            zoom: { enabled: !1 }, legend: { show: !1 }, 
            colors: ["#727cf5"], 
            xaxis: { categories: window.ventas_producto_nombre, axisBorder: { show: !1 } }, 
            yaxis: { labels: { formatter: function (e) { return e }, offsetX: -15 } }, 
            tooltip: { enabled: false },
            fill: { opacity: 1 }, 
        };
        new ApexCharts(document.querySelector("#productosMasvendidos"), r).render(); 

    },

    graficas.prototype.init = function () {
        this.initCharts();
    }
    jq.AnalyticsDashboard = new graficas,
    jq.AnalyticsDashboard.Constructor = graficas
    
}(window.jQuery);