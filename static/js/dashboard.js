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
            fill: {
                type: "gradient",
                gradient: { type: "vertical", shadeIntensity: 1, inverseColors: !1, opacityFrom: .45, opacityTo: .05, stops: [45, 100] }
            }
        };
        new ApexCharts(document.querySelector("#cantidad-ventas"), r).render();

        colores = ["#fa5c7c", "#ffbc00", "#0acf97"]; 
        var circular = { 
            chart: { height: 203, type: "donut" }, 
            legend: { show: !1 }, stroke: { colors: ["transparent"] }, 
            series: window.comprasPorcentaje, labels: ["Pendiente", "En envio", "Entregado"], 
            colors: colores, responsive: [{ breakpoint: 480, options: { chart: { width: 200 }, legend: { position: "bottom" } } }]
        }; 
        new ApexCharts(document.querySelector("#totalCompras"), circular).render()
    },

    graficas.prototype.init = function () {
        this.initCharts();
    }
    jq.AnalyticsDashboard = new graficas,
    jq.AnalyticsDashboard.Constructor = graficas
    
}(window.jQuery), function () { "use strict"; window.jQuery.AnalyticsDashboard.init() }();