document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    socket.on('connect', () => {

        document.querySelectorAll('.remove').forEach(link => {
            link.onclick = () => {
                const number = link.parentElement.dataset.index;
                console.log(number)
                socket.emit('delete channel', {'index': number});
            };
        });
        document.querySelectorAll('.room').forEach(link => {
            link.onclick = () => {
                const index = link.dataset.index;
                socket.emit('channel id', {'index': index});
            };
        });
    });
});
