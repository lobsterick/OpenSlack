document.addEventListener('DOMContentLoaded', () => {

    window.scrollTo(0,document.body.scrollHeight);
    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);


    // When you add new room with submit, server should update it's table of rooms

    socket.on('connect', () => {
        document.querySelector("#new_message").onsubmit = function () {
            const new_message_body = document.querySelector("#new_message_body").value;
            socket.emit("new_message_submit", new_message_body)
        }
    });
});
