$(document).ready(function () {
    $("#resultadoCrear").hide();
    consultartareas(); // Llama a la función para cargar las tareas al cargar la página
});

function consultartareas() {
    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:8000/services/tareas/",
        headers: {
            "Content-Type": "application/json"
        },
        success: onExitotarea,
        error: onErrortarea
    });
}

function onExitotarea(data) {
    // Destruir la DataTable existente si ya ha sido inicializada
    if ($.fn.DataTable.isDataTable('#tablaTarea')) {
        $('#tablaTarea').DataTable().destroy();
    }

    // Inicializar DataTable con las opciones y el idioma configurados
    var dataTable = $('#tablaTarea').DataTable({
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
    $.each(data, function (index, tarea) {
        var boton0 = "<button class='btn btn-sm btn-primary editar-task' data-id='${tarea.id}'>Edit</button>";
        var boton1 = "<button class='btn btn-sm btn-danger eliminar-task' data-id='${tarea.id}'>Delete</button>";
        var boton2 = "<button class='btn btn-sm btn-success asignar-usuario' data-id='${tarea.id}'>Asignar</button>";
        var boton3 = "<button class='btn btn-sm btn-warning cambiar-estado' data-id='${tarea.id}'>Estado</button>";

        dataTable.row.add([
            tarea.id,
            tarea.idUsuario,
            tarea.titulo,
            tarea.descripcion,
            tarea.fechaVencimiento,
            tarea.estado,
            boton0 + ' ' + boton1 + ' ' + boton2 + ' ' + boton3
        ]).draw(false);

    });
}

function onErrortarea(xhr, status, error) {
    console.error("Error al cargar las tareas:", error);
    // Aquí puedes manejar el error, por ejemplo, mostrar un mensaje al usuario
    Swal.fire({
        icon: 'error',
        title: 'Error al cargar las tareas',
        text: 'Hubo un problema al cargar las tareas. Inténtelo de nuevo más tarde.'
    });
}









    $('#task-form').submit(function(event) {
        event.preventDefault();
        var formData = {
            titulo: $('#task-title').val(),
            descripcion: $('#task-desc').val(),
            fecha_vencimiento: $('#task-deadline').val(),
            estado: $('#task-status').val()
        };

        $.ajax({
            url: 'http://127.0.0.1:8000/services/tareas/',  // Ruta de la API para crear una nueva tarea
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(formData),
            success: function(response) {
                cargarTareas();  // Recargar la lista de tareas después de agregar una nueva
                $('#task-form').trigger('reset');  // Limpiar el formulario
            },
            error: function(error) {
                console.error('Error al agregar tarea:', error);
            }
        });
    });

    // Evento para eliminar una tarea
    $(document).on('click', '.eliminar-task', function() {
        var taskId = $(this).data('id');
        
        // Mostrar modal de confirmación
        $('#confirmDeleteModal').modal('show');

        // Confirmar la eliminación de la tarea
        $('#confirm-delete').click(function() {
            $.ajax({
                url: `http://localhost:8000/services/tareas/${taskId}/`,  // Ruta de la API para eliminar la tarea
                method: 'DELETE',
                success: function(response) {
                    cargarTareas();  // Recargar la lista de tareas después de eliminar
                    $('#confirmDeleteModal').modal('hide');  // Ocultar el modal de confirmación
                },
                error: function(error) {
                    console.error('Error al eliminar tarea:', error);
                }
            });
        });
    });

    // Eventos para editar una tarea (abrir el modal y guardar cambios)
    $(document).on('click', '.editar-task', function() {
        var taskId = $(this).data('id');
        
        // Llamar a la API para obtener los detalles de la tarea
        $.ajax({
            url: `http://localhost:8000/services/tareas/${taskId}/`,  // Ruta de la API para obtener detalles de la tarea
            method: 'GET',
            success: function(data) {
                // Llenar el formulario de edición con los datos de la tarea
                $('#edit-task-title').val(data.titulo);
                $('#edit-task-desc').val(data.descripcion);

                // Mostrar el modal de edición
                $('#editTaskModal').modal('show');
            },
            error: function(error) {
                console.error('Error al cargar detalles de la tarea:', error);
            }
        });

        // Guardar cambios en la tarea
        $('#save-changes').click(function() {
            var formData = {
                titulo: $('#edit-task-title').val(),
                descripcion: $('#edit-task-desc').val()
            };

            $.ajax({
                url: `http://localhost:8000/services/tareas/${taskId}/`,  // Ruta de la API para actualizar la tarea
                method: 'PUT',
                contentType: 'application/json',
                data: JSON.stringify(formData),
                success: function(response) {
                    cargarTareas();  // Recargar la lista de tareas después de editar
                    $('#editTaskModal').modal('hide');  // Ocultar el modal de edición
                },
                error: function(error) {
                    console.error('Error al guardar cambios en la tarea:', error);
                }
            });
        });
    });

    // Eventos para asignar usuario a una tarea (abrir el modal y confirmar asignación)
    $(document).on('click', '.asignar-usuario', function() {
        var taskId = $(this).data('id');

        // Llamar a la API para obtener la lista de usuarios disponibles
        $.ajax({
            url: 'http://localhost:8000/services/usuarios/',  // Ruta de la API para obtener la lista de usuarios
            method: 'GET',
            success: function(usuarios) {
                var selectOptions = '';
                $.each(usuarios, function(index, usuario) {
                    selectOptions += `<option value="${usuario.id}">${usuario.nombre} ${usuario.apellido}</option>`;
                });
                $('#assign-user').html(selectOptions);

                // Mostrar el modal de asignación de usuario
                $('#assignUserModal').modal('show');
            },
            error: function(error) {
                console.error('Error al cargar la lista de usuarios:', error);
            }
        });

        // Confirmar la asignación de usuario a la tarea
        $('#confirm-assign-user').click(function() {
            var userId = $('#assign-user').val();

            $.ajax({
                url: `http://localhost:8000/services/tareas/${taskId}/asignar-usuario/`,  // Ruta de la API para asignar usuario a la tarea
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ usuario_id: userId }),
                success: function(response) {
                    cargarTareas();  // Recargar la lista de tareas después de asignar usuario
                    $('#assignUserModal').modal('hide');  // Ocultar el modal de asignación de usuario
                },
                error: function(error) {
                    console.error('Error al asignar usuario a la tarea:', error);
                }
            });
        });
    });

    // Eventos para cambiar estado de una tarea
    $(document).on('click', '.cambiar-estado', function() {
        var taskId = $(this).data('id');

        // Llamar a la API para cambiar el estado de la tarea
        $.ajax({
            url: `http://localhost:8000/services/tareas/${taskId}/cambiar-estado/`,  // Ruta de la API para cambiar estado de la tarea
            method: 'POST',
            success: function(response) {
                cargarTareas();  // Recargar la lista de tareas después de cambiar estado
            },
            error: function(error) {
                console.error('Error al cambiar estado de la tarea:', error);
            }
        });
    });


