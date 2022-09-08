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

    if (data.type === 'kill_session')
        window.location.reload();

    else {
        document.getElementById("board_row_1").innerHTML = data.board_row_1;
        document.getElementById("board_row_2").innerHTML = data.board_row_2;
        document.getElementById("board_row_3").innerHTML = data.board_row_3;
        document.getElementById("board_row_4").innerHTML = data.board_row_4;
        document.getElementById("board_row_5").innerHTML = data.board_row_5;
        document.getElementById("board_row_7").innerHTML = data.board_row_6;
        document.getElementById("board_row_6").innerHTML = data.board_row_7;
        document.getElementById("board_row_8").innerHTML = data.board_row_8;
        document.getElementById("board_row_9").innerHTML = data.board_row_9;
        document.getElementById("board_row_10").innerHTML = data.board_row_10;
    }
}

let form = document.getElementById('form')
form.addEventListener('submit', (e)=> {
    e.preventDefault()

    let message = e.target.message.value 
    socket.send(JSON.stringify({
        'message':message
    }))
    
    form.reset()
})

let button = document.getElementById('kill')
button.addEventListener('click', (e)=> {
    socket.send(JSON.stringify({
        'type': 'kill_session'
    }))
})