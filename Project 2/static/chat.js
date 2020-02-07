document.addEventListener('DOMContentLoaded', () => {
    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    socket.on('connect', () => {

        document.querySelectorAll('button').forEach(button => {
            button.onclick = () => {
                const message = document.querySelector('#message').value;
                let timestamp = '';
                let T = new Date();
                timestamp += T.getHours() + ':' + T.getMinutes();
                socket.emit('send message', {'message': message, 'time': timestamp});
                document.querySelector('#message').value = '';
            };
        });

        document.addEventListener('keypress', function(e) {
            if (e.keyCode === 13 || e.which === 13) {
                const message = document.querySelector('#message').value;
                let timestamp = '';
                let T = new Date();
                timestamp += T.getHours() + ':' + T.getMinutes();
                socket.emit('send message', {'message': message, 'time': timestamp});
                document.querySelector('#message').value = '';
            }
        });
    });

    socket.on('print msg', data => {
        const li = document.createElement('li');
        li.innerHTML = `${data.msg}`;
        document.querySelector('#messages-container').append(li);
    });
});