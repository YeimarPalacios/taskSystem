$(document).ready(function() {
    $('.task-status').on('change', function() {
        // Lógica para manejar el cambio de estado
    });

    $('.edit-task').on('click', function() {
        const currentTask = $(this).closest('.list-group-item');
        const title = currentTask.find('h5').text();
        const desc = currentTask.find('p').text();
        const assign = currentTask.find('small').text().replace('Asignado a: ', '');
        
        $('#edit-task-title').val(title);
        $('#edit-task-desc').val(desc);
        $('#edit-task-assign').val(assign);
    });


});

function eliminarTask(){
    const currentTask = $(this).closest('.list-group-item');
    
    Swal.fire({
        title: '¿Estás seguro?',
        text: "¡No podrás revertir esto!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: 'Sí, eliminarlo'
    }).then((result) => {
        if (result.isConfirmed) {
            currentTask.remove();
            Swal.fire(
                '¡Eliminado!',
                'Tu tarea ha sido eliminada.',
                'success'
            ); 
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    // Obtén el elemento que contiene el nombre de usuario
    const usernameElement = document.getElementById('username');
    // Obtén el nombre de usuario del atributo data
    const username = usernameElement.dataset.username;// Asegúrate de pasar el nombre de usuario desde la vista
    nombreSinEspacios = username.replace(/\s/g, '');
    const taskForm = document.getElementById('task-form');
    const taskList = document.getElementById('task-list');

    const wsScheme = window.location.protocol === "https:" ? "wss" : "ws";
    const socket = new WebSocket(`${wsScheme}://${window.location.host}/ws/notifications/${nombreSinEspacios}/`);

    socket.onmessage = function(event) {
        const data = JSON.parse(event.data);
        console.log(data)
        showNotification(data.message);
    };

    function showNotification(message, type = 'success') {
        Swal.fire({
            position: 'top-end',
            icon: type,
            title: message,
            showConfirmButton: true,
        });
    }

    taskForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const title = document.getElementById('task-title').value;
        const desc = document.getElementById('task-desc').value;
        const assign = document.getElementById('task-assign').value;

        addTask(title, desc, assign);
        taskForm.reset();

        const notificationMessage = `Nueva tarea asignada a ${assign}`;
        socket.send(JSON.stringify({
            'message': notificationMessage
        }));
    });

    function addTask(title, desc, assign) {
        fetch(`/render_task_item/?title=${title}&desc=${desc}&assign=${assign}`)
            .then(response => response.json())
            .then(data => {
                const listItem = document.createElement('div');
                listItem.innerHTML = data.html;
                taskList.appendChild(listItem.firstChild);
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification("Error al agregar la tarea", 'error');
            });
    }
});
