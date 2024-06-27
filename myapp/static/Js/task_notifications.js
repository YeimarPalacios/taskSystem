
document.addEventListener('DOMContentLoaded', function() {
    // Obtén el elemento que contiene el nombre de usuario
    const usernameElement = document.getElementById('username');
    // Obtén el nombre de usuario del atributo data
    const username = usernameElement.dataset.username;// Asegúrate de pasar el nombre de usuario desde la vista
    nombreSinEspacios = username.replace(/[^\w.-]/g, '').substring(0, 100);
    const taskForm = document.getElementById('task-form');
    const taskList = document.getElementById('task-list');

    const wsScheme = window.location.protocol === "https:" ? "wss" : "ws";
    const socket = new WebSocket(`${wsScheme}://${window.location.host}/ws/notifications/${nombreSinEspacios}/`);
    // const sessionKey = getSessionKeyFromCookies();
    // const socket = new WebSocket(`${wsScheme}://${window.location.host}/ws/notifications/?session_key=${sessionKey}`);

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

    
  
});
