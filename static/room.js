document.addEventListener('DOMContentLoaded', () => {

    window.scrollTo(0,document.body.scrollHeight);

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);


    // When you add new message with submit, server should append it to the room's messages

    socket.on('connect', () => {
        document.querySelector("#new_message").onsubmit = function () {
            var new_message_body = document.querySelector("#new_message_body").value;
            socket.emit("new_message_submit", new_message_body);
            document.querySelector("#new_message_body").value = '';
            return false
        }
    });


        // When a new message is announced, reload all messages on page
    socket.on('update_messages', updated_list=> {
        var last_room = window.location.href.split("/").pop();
        if (updated_list["room"] === last_room){
            var messages_last_100 = document.getElementById("messages_last_100");
            messages_last_100.innerHTML = "";
            var posts;
            // console.log(updated_list); // debugging
            for (posts in updated_list["message_list"])
            {
                var post = document.createElement('div');
                var inHTML = '<div class="post"><span style=\'color: #946e09; font-weight:bold\'>';
                inHTML += "USERNAME";
                inHTML += "</span> on date XXX said: </br>";
                inHTML += updated_list["message_list"][posts];
                inHTML += "</div>";
                post.innerHTML = inHTML;
                messages_last_100.appendChild(post);
            }
            window.scrollTo(0,document.body.scrollHeight);
            return false
    }});

});


