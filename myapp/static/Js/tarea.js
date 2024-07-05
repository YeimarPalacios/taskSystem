$(document).ready(function () {
    $("#resultadoCrear").hide();
    consultartareas(); // Llama a la función para cargar las tareas al cargar la página
});

// Función para consultar tareas
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

// Función que se ejecuta en caso de éxito al consultar tareas
// En tu archivo `tarea.js`

function obtenerNombreApellidoUsuario(idUsuario, callback) {
    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:8000/services/usuarios/" + idUsuario + "/",
        headers: {
            "Content-Type": "application/json"
        },
        success: function (usuario) {
            var nombreApellido = usuario.nombre + ' ' + usuario.apellido;
            callback(nombreApellido);
        },
        error: function (xhr, status, error) {
            console.error("Error al obtener usuario:", error);
            callback('');
        }
    });
}

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

// Función que se ejecuta en caso de éxito al consultar tareas
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
        var boton0 = "<button class='btn btn-sm btn-primary editar-task' data-id='" + tarea.id + "' onclick='EditarTareaClick(this, \"" + nombreUsuario + "\", \"" + apellidoUsuario + "\")'><i class='bi bi-pen-fill'></i></button>";
        var boton1 = "<button class='btn btn-sm btn-danger eliminar-task' data-id='" + tarea.id + "'><i class='bi bi-trash'></i></button>";
        var boton2 = `<button class='btn btn-sm btn-success asignar-usuario' data-id='${tarea.id}' onclick='mostrarModalAsignarUsuario(${tarea.id})'><i class='bi bi-person-plus'></i></button>`;
        var boton3 = "<button class='btn btn-sm btn-warning cambiar-estado' data-id='" + tarea.id + "' onclick='mostrarModalCambiarEstado(" + tarea.id + ")'><i class='bi bi-check'></i></button>";
        var boton4 = "<button class='btn btn-sm btn-info ver-historial' data-id='" + tarea.id + "' onclick='mostrarHistorialTarea(" + tarea.id + ")'><i class='bi bi-clock-history'></i></button>";
        // Obtener nombre y apellido del usuario si idUsuario no es null
        if (tarea.idUsuario) {
            obtenerNombreApellidoUsuario(tarea.idUsuario, function (nombreApellido) {
                dataTable.row.add([
                    tarea.id,
                    nombreApellido,
                    tarea.titulo,
                    tarea.descripcion,
                    tarea.fechaVencimiento,
                    tarea.estado,
                    boton4,
                    "<div class='boton-container'>" + boton0 +' '+ boton1 + "</div><div class='boton-container'>" + boton2 +' '+ boton3 + "</div>"
                ]).draw(false);
            });
        } else {
            // Si idUsuario es null, agregar una fila con datos vacíos para idUsuario
            dataTable.row.add([
                tarea.id,
                'No asignado', // Mostrar vacío si idUsuario es null
                tarea.titulo,
                tarea.descripcion,
                tarea.fechaVencimiento,
                tarea.estado,
                boton4,
                "<div class='boton-container'>" + boton0 +' '+ boton1 + "</div><div class='boton-container'>" + boton2 +' '+ boton3 + "</div>"
            ]).draw(false);
        }
    });
}

// Función que se ejecuta en caso de error al consultar tareas
function onErrortarea(xhr, status, error) {
    console.error("Error al cargar las tareas:", error);
    // Aquí puedes manejar el error, por ejemplo, mostrar un mensaje al usuario
    Swal.fire({
        icon: 'error',
        title: 'Error al cargar las tareas',
        text: 'Hubo un problema al cargar las tareas. Inténtelo de nuevo más tarde.'
    });
}

// Llamar a la función para consultar tareas al cargar la página u otro evento apropiado


function mostrarHistorialTarea(idTarea) {
    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:8000/services/historial_tareas/" + idTarea,
        headers: {
            "Content-Type": "application/json"
        },
        success: function(data) {
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
                    historial.idTarea,
                    historial.detalle
                ]).draw(false);
            });

            // Mostrar el modal
            $('#historialTareaModal').modal('show');
        },
        error: function(xhr, status, error) {
            console.error("Error al cargar el historial de tareas:", error);
            Swal.fire({
                icon: 'error',
                title: 'Error al cargar el historial de tareas',
                text: 'Hubo un problema al cargar el historial de tareas. Inténtelo de nuevo más tarde.'
            });
        }
    });
}




// Función para agregar una nueva tarea
function mostrarFormularioCrearTarea(nombreUsuario, apellidoUsuario) {
    // Cambiar el título del formulario
    var titulo = $("#agregarTareaModalLabel");
    titulo.text("Agregar Tarea");

    // Cambiar el texto del botón de submit
    var btnform = $("#btn-form-tarea");
    btnform.text("Agregar Tarea");

    // Asignar la función de creación de tarea al clic del botón
    btnform.off("click").click(function() {
        crearTarea(nombreUsuario, apellidoUsuario); // Llamar a la función para crear tarea
    });

    // Mostrar la modal
    $('#agregarTareaModal').modal('show');
}

// Función para crear una tarea
function crearTarea(nombreUsuario, apellidoUsuario) {
    var formData = {
        titulo: $('#task-title').val(),
        descripcion: $('#task-desc').val(),
        fechaVencimiento: $('#task-deadline').val(),
        estado: 'Pendiente', // Estado inicial
        idUsuario: '' // IdUsuario inicialmente vacío
    };

    $.ajax({
        url: 'http://127.0.0.1:8000/services/tareas/',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(formData),
        success: function(response) {
            mostrarAlertaExito('La tarea se ha creado correctamente.');
            $('#task-form').trigger('reset'); // Limpiar el formulario
            $('#agregarTareaModal').modal('hide'); // Cerrar la modal
 
            var detalleHistorial = 'Se creó la tarea por ' + nombreUsuario + ' ' + apellidoUsuario; // Construir el detalle
            crearHistorialTareaCrear(response.id, detalleHistorial);
            consultartareas(); // Volver a cargar las tareas
        },
        error: function(xhr, status, error) {
            console.error('Error al crear la tarea:', xhr.responseText);
            mostrarAlertaError('Hubo un problema al crear la tarea. Inténtelo de nuevo.');
        }
    });
}

function crearHistorialTareaCrear(idTarea, detalleHistorial) {
    var formData = {
        idTarea: idTarea,
        detalle: detalleHistorial
    };

    $.ajax({
        url: 'http://127.0.0.1:8000/services/historial_tareas/',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(formData),
        success: function(response) {
            mostrarAlertaExito('El historial de tarea se ha creado correctamente.');
            // Limpiar el formulario y cerrar la modal del historial si es necesario
            // consultarHistorialTareas(); // Volver a cargar el historial de tareas si es necesario
        },
        error: function(xhr, status, error) {
            console.error('Error al crear el historial de tarea:', xhr.responseText);
            mostrarAlertaError('Hubo un problema al crear el historial de tarea. Inténtelo de nuevo.');
        }
    });
}


// Función para mostrar una alerta de éxito
function mostrarAlertaExito(mensaje) {
    Swal.fire({
        icon: 'success',
        title: 'Éxito',
        text: mensaje,
        showConfirmButton: false,
        timer: 2500
    });
}

// Función para mostrar una alerta de error
function mostrarAlertaError(mensaje) {
    Swal.fire({
        icon: 'error',
        title: 'Error',
        text: mensaje
    });
}



$(document).on('click', '.eliminar-task', function() {
    var taskId = $(this).data('id');
    
    // Mostrar modal de confirmación
    Swal.fire({
        title: '¿Estás seguro?',
        text: '¿Estás seguro de eliminar la tarea?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d5c429',
        confirmButtonText: 'Eliminar',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            // Realizar la solicitud de eliminación AJAX
            $.ajax({
                url: `http://127.0.0.1:8000/services/tareas/${taskId}/`,  // Ruta de la API para eliminar la tarea
                method: 'DELETE',
                success: function(response) {
                    Swal.fire('Eliminado', 'La tarea ha sido eliminada correctamente', 'success');
                    // Recargar la tabla de tareas después de eliminar
                    consultartareas(); // Asegúrate de llamar a tu función para cargar las tareas
                },
                error: function(error) {
                    console.error('Error al eliminar tarea:', error);
                    Swal.fire({
                        icon: 'error',
                        title: 'Error al eliminar tarea',
                        text: 'Hubo un problema al intentar eliminar la tarea. Inténtelo de nuevo más tarde.'
                    });
                }
            });
        }
    });
});

function EditarTareaClick(button, nombreUsuario, apellidoUsuario) {
    var taskId = $(button).data('id');

    // Aquí deberías obtener los datos de la tarea usando el ID.
    // Asumiendo que tienes una función o una forma de obtener los datos de la tarea.
    var taskData = obtenerDatosTarea(taskId);
    EditarTarea(taskData, nombreUsuario, apellidoUsuario);
}

function obtenerDatosTarea(taskId) {
    // Supongamos que tienes una lista de tareas en tu script o quieres obtenerlo del servidor
    // Esto es solo un ejemplo, ajusta según tu implementación
    var taskData;
    $.ajax({
        url: `http://127.0.0.1:8000/services/tareas/${taskId}/`,
        method: 'GET',
        async: false,  // Usamos async: false para que la llamada sea síncrona (no recomendado en producción)
        success: function (response) {
            taskData = response;
        },
        error: function (error) {
            console.error('Error al obtener los datos de la tarea:', error);
        }
    });
    return taskData;
}

function mostrarFormularioActualizarTarea() {
    var titulo = $("#editTaskModalLabel");
    titulo.text("Editar Tarea");
    var btnGuardar = $("#save-changes");
    btnGuardar.text("Guardar cambios");
}


function EditarTarea(taskData, nombreUsuario, apellidoUsuario) {
    mostrarFormularioActualizarTarea();
    $('#edit-task-title').val(taskData.titulo);
    $('#edit-task-desc').val(taskData.descripcion);
    
    // Formatear la fecha para mostrarla en el input de tipo datetime-local
    var fechaVencimiento = moment(taskData.fechaVencimiento).format('YYYY-MM-DDTHH:mm');
    $('#edit-task-deadline').val(fechaVencimiento);

    $('#editTaskModal').modal('show');

    var btnSaveChanges = $("#save-changes");
    btnSaveChanges.off("click").click(function () {
        var formData = {
            titulo: $('#edit-task-title').val(),
            descripcion: $('#edit-task-desc').val(),
            fechaVencimiento: $('#edit-task-deadline').val(),
        };

        $.ajax({
            url: `http://127.0.0.1:8000/services/tareas/${taskData.id}/`,
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(formData),
            success: function (response) {
                // Recargar la lista de tareas después de editar
                consultartareas();
                var detalleHistorialA = 'Se modificó la tarea por ' + nombreUsuario + ' ' + apellidoUsuario;
                crearHistorialTarea(response.id, detalleHistorialA); 
                $('#editTaskModal').modal('hide');  // Ocultar el modal de edición

                Swal.fire({
                    title: 'Éxito',
                    text: 'Los cambios han sido guardados correctamente.',
                    icon: 'success',
                    showCancelButton: false,
                    confirmButtonColor: '#3085d6',
                    confirmButtonText: 'Aceptar'
                });
            },
            error: function (error) {
                console.error('Error al guardar cambios en la tarea:', error);
                Swal.fire({
                    title: 'Error',
                    text: 'Hubo un problema al guardar los cambios.',
                    icon: 'error',
                    showCancelButton: false,
                    confirmButtonColor: '#d33',
                    confirmButtonText: 'Aceptar'
                });
            }
        });
    });
}


function crearHistorialTarea(idTarea, detalleHistorialA) {
    var formData = {
        idTarea: idTarea,
        detalle: detalleHistorialA
    };

    $.ajax({
        url: 'http://127.0.0.1:8000/services/historial_tareas/',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(formData),
        success: function(response) {
            mostrarAlertaExito('El historial de tarea se ha creado correctamente.');
            // Limpiar el formulario y cerrar la modal del historial si es necesario
            // consultarHistorialTareas(); // Volver a cargar el historial de tareas si es necesario
        },
        error: function(xhr, status, error) {
            console.error('Error al crear el historial de tarea:', xhr.responseText);
            mostrarAlertaError('Hubo un problema al crear el historial de tarea. Inténtelo de nuevo.');
        }
    });
}






function mostrarModalAsignarUsuario(taskId) {
    // Guardar el ID de la tarea en un atributo de datos del botón
    $('#confirm-assign-user').data('task-id', taskId);

    // Cargar dinámicamente los usuarios en el select
    $.ajax({
        url: 'http://127.0.0.1:8000/services/usuarios/', // URL para obtener la lista de usuarios
        method: 'GET',
        success: function(response) {
            console.log('Respuesta del servidor:', response); // Depuración
            var usuarios = response; // Ajusta según la estructura real
            if (!usuarios || usuarios.length === 0) {
                console.error('No se encontraron usuarios en la respuesta.');
                mostrarAlertaError('No se encontraron usuarios en la respuesta.');
                return;
            }
            var select = $('#assign-user');
            select.empty();
            usuarios.forEach(function(usuario) {
                select.append('<option value="' + usuario.id + '">' + usuario.nombre + ' ' + usuario.apellido + '</option>');
            });
            // Mostrar el modal
            $('#assignUserModal').modal('show');
        },
        error: function(error) {
            console.error('Error al cargar los usuarios:', error);
            mostrarAlertaError('Hubo un problema al cargar los usuarios. Inténtelo de nuevo.');
        }
    });
}



$('#confirm-assign-user').click(function() {
    var taskId = $(this).data('task-id');
    var userId = $('#assign-user').val();

    if (!userId) {
        mostrarAlertaError('Seleccione un usuario.');
        return;
    }

    var formData = {
        idUsuario: userId
    };

    fetch(`/asignar_tarea/?userId=${userId}&taskId=${taskId}`)
    .then(response => response.json())
    .then(data => {
        mostrarAlertaExito('El usuario ha sido asignado correctamente a la tarea.');
        $('#assign-user-form').trigger('reset'); // Limpiar el formulario
        $('#assignUserModal').modal('hide'); // Cerrar la modal
        consultartareas(); // Volver a cargar las tareas
    })
    .catch(error => {
        console.error('Error al asignar el usuario a la tarea:', error);
        mostrarAlertaError('Hubo un problema al asignar el usuario. Inténtelo de nuevo.');

    });
});



function mostrarAlertaExito(mensaje) {
    Swal.fire({
        icon: 'success',
        title: 'Éxito',
        text: mensaje,
        showConfirmButton: false,
        timer: 2500
    });
}

function mostrarAlertaError(mensaje) {
    Swal.fire({
        icon: 'error',
        title: 'Error',
        text: mensaje
    });
}
    // Eventos para cambiar estado de una tarea
    function mostrarModalCambiarEstado(taskId) {
        // Preparar el modal para mostrar el título adecuado
        var titulo = $("#changeStatusModalLabel");
        titulo.text("Cambiar Estado de Tarea");
    
        // Preparar el botón de confirmación
        var btnConfirmar = $("#confirm-change-status");
        btnConfirmar.text("Cambiar Estado");
    
        // Asignar el evento click al botón de confirmación
        btnConfirmar.off("click").click(function() {
            cambiarEstadoTarea(taskId); // Llamar a la función para cambiar el estado
        });
    
        // Mostrar el modal
        $('#changeStatusModal').modal('show');
    }
    
    // Función para cambiar el estado de la tarea
    function cambiarEstadoTarea(taskId) {
        var nuevoEstado = $('#task-status').val();
    
        var formData = {
            estado: nuevoEstado
        };
    
        $.ajax({
            url: 'http://127.0.0.1:8000/services/tareas/' + taskId + '/',
            method: 'POST', // Usar PUT para actualizar el estado
            contentType: 'application/json',
            data: JSON.stringify(formData),
            success: function(response) {
                mostrarAlertaExito('El estado de la tarea ha sido actualizado correctamente.');
                $('#change-status-form').trigger('reset'); // Limpiar el formulario
                $('#changeStatusModal').modal('hide'); // Cerrar la modal
                consultartareas(); // Volver a cargar las tareas
                if (nuevoEstado === 'completada' || nuevoEstado === 'Completada') {
                    crearHistorialTareaEstado(taskId);
                }
            },
            error: function(error) {
                console.error('Error al cambiar el estado de la tarea:', error);
                mostrarAlertaError('Hubo un problema al cambiar el estado de la tarea. Inténtelo de nuevo.');
            }
        });
    }
    
    function crearHistorialTareaEstado(idTarea) {
        // Obtener la fecha y hora actual del sistema
        var now = new Date();
        var formattedDate = now.toLocaleString('es-ES', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
    
        // Construir el detalle con la fecha y hora
        var detalle = `Tarea completada el ${formattedDate}`;
    
        var formData = {
            idTarea: idTarea,
            detalle: detalle
        };
    
        $.ajax({
            url: 'http://127.0.0.1:8000/services/historial_tareas/',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(formData),
            success: function(response) {
                mostrarAlertaExito('El historial de tarea se ha creado correctamente.');
                // Limpiar el formulario y cerrar la modal del historial si es necesario
                // consultarHistorialTareas(); // Volver a cargar el historial de tareas si es necesario
            },
            error: function(xhr, status, error) {
                console.error('Error al crear el historial de tarea:', xhr.responseText);
                mostrarAlertaError('Hubo un problema al crear el historial de tarea. Inténtelo de nuevo.');
            }
        });
    }
    


