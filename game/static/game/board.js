const socket_url = `ws://${window.location.host}/game_socket/`;
const socket = new WebSocket(socket_url);
const current_path = window.location.pathname.substring(window.location.pathname.lastIndexOf('/')+1)

socket.onopen = function(e) {
    socket.send(JSON.stringify({
        'type': 'initialize',
        'message': current_path
    }));
}

socket.onmessage = function(e){
    let data = JSON.parse(e.data)
    console.log('Data:', data)
    let jackstraws_img = {'P': '♙', 'R': '♖' ,'K': '♘', 'B': '♗', 'Q': '♕', 'I': '♔', 'C': '*', '.': ''};

    if (data.type === 'initialize') {
        remaining_time = parseInt(data.remaining_time) + 1
        setInterval(update_timer, 1000)
    }

    else if (data.type === 'kill_session')
        window.location.reload();

    else if (data.type === 'game_message') {
        let board = data.board;
        for (let key in board){
            document.getElementById(key).innerHTML = jackstraws_img[board[key]];
        }

        remaining_time = parseInt(data.remaining_time) + 1;
    }
}

let form = document.getElementById('form')
form.addEventListener('submit', (e)=> {
    e.preventDefault()

    let message = e.target.message.value 
    socket.send(JSON.stringify({
        'type': 'game_message',
        'message': message
    }))
    
    form.reset()
})

let button = document.getElementById('kill')
button.addEventListener('click', (e)=> {
    socket.send(JSON.stringify({
        'type': 'kill_session'
    }))
})

function update_timer() {
    if (--remaining_time < 0)
        return;
    
    minutes = Math.floor(remaining_time / 60);
    seconds = remaining_time - 60 * minutes;

    document.getElementById("timer").innerHTML = minutes + 'm ' + seconds + 's';
}