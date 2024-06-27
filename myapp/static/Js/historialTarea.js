$(document).ready(function () {
    $("#resultadoCrear").hide();
    consultarHistorialTareas(); // Llama a la función para cargar las tareas al cargar la página
});

function consultarHistorialTareas() {
    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:8000/services/historial_tareas/",
        headers: {
            "Content-Type": "application/json"
        },
        success: onExitoHistorialTarea,
        error: onErrorHistorialTarea
    });
}

// Función que se ejecuta en caso de éxito al consultar el historial de tareas
function onExitoHistorialTarea(data) {
    // Destruir la DataTable existente si ya ha sido inicializada
    if ($.fn.DataTable.isDataTable('#tablaHistorialTarea')) {
        $('#tablaHistorialTarea').DataTable().destroy();
    }

    // Inicializar DataTable con las opciones y el idioma configurados
    var dataTable = $('#tablaHistorialTarea').DataTable({
        dom: '<"row"<"col-md-6"l><"col-md-6"f>>tip',
        pageLength: 5,
        lengthMenu: [5, 10, 25, 50],
        language: {
            "sProcessing": "Procesando...",
            "sLengthMenu": "Mostrar _MENU_ registros",
            "sZeroRecords": "No se encontraron resultados",
            "sEmptyTable": "Ningún dato disponible en esta tabla",
            "sInfo": "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
            "sInfoEmpty": "Mostrando registros del 0 al 0 de un total de 0 registros",
            "sInfoFiltered": "(filtrado de un total de _MAX_ registros)",
            "sInfoPostFix": "",
            "sSearch": "Buscar:",
            "sUrl": "",
            "sInfoThousands": ",",
            "sLoadingRecords": "Cargando...",
            "oPaginate": {
                "sFirst": "Primero",
                "sLast": "Último",
                "sNext": "Siguiente",
                "sPrevious": "Anterior"
            },
            "oAria": {
                "sSortAscending": ": Activar para ordenar la columna de manera ascendente",
                "sSortDescending": ": Activar para ordenar la columna de manera descendente"
            }
        }
    });

    // Limpiar y agregar filas a la DataTable
    dataTable.clear().draw();
    $.each(data, function (index, historial) {
        dataTable.row.add([
            historial.id,
            historial.idTarea,
            historial.detalle
        ]).draw(false);
    });
}

// Función que se ejecuta en caso de error al consultar el historial de tareas
function onErrorHistorialTarea(xhr, status, error) {
    console.error("Error al cargar el historial de tareas:", error);
    // Aquí puedes manejar el error, por ejemplo, mostrar un mensaje al usuario
    Swal.fire({
        icon: 'error',
        title: 'Error al cargar el historial de tareas',
        text: 'Hubo un problema al cargar el historial de tareas. Inténtelo de nuevo más tarde.'
    });
}
