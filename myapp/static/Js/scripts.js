document.addEventListener('DOMContentLoaded', () => {
    const taskForm = document.getElementById('task-form');
    const taskList = document.getElementById('task-list');
    const editTaskForm = document.getElementById('edit-task-form');
    let currentTask = null;

    taskForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const title = document.getElementById('task-title').value;
        const desc = document.getElementById('task-desc').value;
        const assign = document.getElementById('task-assign').value;

        addTask(title, desc, assign);

        taskForm.reset();
        
    });

    function addTask(title, desc, assign) {
        fetch(`/render_task_item/?title=${title}&desc=${desc}&assign=${assign}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                const listItem = document.createElement('div');
                listItem.innerHTML = data.html;
                showNotification("Nueva tarea asignada a " + assign);
                
               const taskItem = listItem.firstChild;
                taskList.appendChild(taskItem);
   //
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification("Error al agregar la tarea", 'error');
            });
    }
    
    document.getElementById('save-changes').addEventListener('click', () => {
        const title = document.getElementById('edit-task-title').value;
        const desc = document.getElementById('edit-task-desc').value;
        const assign = document.getElementById('edit-task-assign').value;

        if (currentTask) {
            currentTask.querySelector('h5').innerText = title;
            currentTask.querySelector('p').innerText = desc;
            currentTask.querySelector('small').innerText = "Asignado a: " + assign;
        }

        $('#editTaskModal').modal('hide');
        showNotification("Tarea actualizada");
    });

    function showNotification(message, type = 'info') {
        Swal.fire({
            title: 'Notificación',
            text: message,
            icon: type,
            timer: 3000,
            showConfirmButton: false
        });
    }
});
