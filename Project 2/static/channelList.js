document.addEventListener('DOMContentLoaded', (e) => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    socket.on('connect', () => {

        document.querySelectorAll('.remove').forEach(link => {
            link.onclick = () => {
                const number = link.parentElement.dataset.index;
                socket.emit('delete channel', {'index': number});
            };
        });
        document.querySelectorAll('.channel').forEach(link => {
            link.onclick = () => {
                const index = link.dataset.index;
                e.preventDefault();
                console.log(index)
                socket.emit('channel id', {'index': index});
            };
        });
    });
});