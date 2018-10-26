document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);


    // When you add new room with submit, server should update it's table of rooms

    socket.on('connect', () => {
            document.querySelector("#new_room_form").onsubmit = function () {
                let new_room_name = document.querySelector("#new_room_name").value;
                new_room_name = new_room_name.replace(/[^a-z0-9]/gi,''); // sanitizing
                if (!(new_room_name === '')) {
                    socket.emit("update_room_list", new_room_name)
                }
            }
        }
    );

    // When a new room is announced, add to the dropdown rooms list
    // TODO Page jump up when open dropdownlist, even when start position was bottom of the page
    socket.on('Update room list', data => {
        let dropdownlist = document.getElementById("dropdown_rooms_list");
        let opt = document.createElement('option');
        opt.innerHTML = data;
        opt.value = `/room/${data}`;
        dropdownlist.appendChild(opt)
    });
});



