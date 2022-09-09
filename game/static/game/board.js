const socket_url = `ws://${window.location.host}/game_socket/`;
const socket = new WebSocket(socket_url);
const current_path = window.location.pathname.substring(window.location.pathname.lastIndexOf('/')+1)

const jackstraws_img = {'P': '♙', 'R': '♖' ,'K': '♘', 'B': '♗', 'Q': '♕', 'I': '♔', 'C': '*', '.': ''};

let remaining_time;
let which_turn;
let all_moves;
let board;
let my_turn;
let last_clicked_id;

socket.onopen = function(e) {
    socket.send(JSON.stringify({
        'type': 'initialize',
        'message': current_path
    }));
}

socket.onmessage = function(e){
    let data = JSON.parse(e.data)
    console.log('Data:', data)

    if (data.type === 'initialize') {
        update_globals(data)
        setInterval(update_timer, 1000);
    }

    else if (data.type === 'kill_session')
        window.location.reload();

    else if (data.type === 'game_message')
        update_globals(data)
}

let button = document.getElementById('kill');
button.addEventListener('click', (e)=> {
    socket.send(JSON.stringify({
        'type': 'kill_session'
    }))
});

let chess_board = document.getElementsByClassName('chess-board')[0]
chess_board.addEventListener('click', (e)=> {
    console.log(e.target)
    if (my_turn === undefined || my_turn === false)
        return
    else if (e.target.classList.contains("highlighted")) {
        let message = last_clicked_id + ' ' + e.target.id;
        console.log(message)
        socket.send(JSON.stringify({
            'type': 'game_message',
            'message': message
        }))
    }
    else if (e.target.tagName !== 'TD')
        return
    else if(e.target.textContent === '')
        return
    else if (e.target.textContent === '*' && which_turn === 0)
        return
    else if (e.target.textContent !== '*' && which_turn === 1)
        return
    else {
        last_clicked_id = e.target.id;
        reset_board();
        for (let key of all_moves[e.target.id]) {
            div = document.getElementById(key)
            div.classList.add("highlighted");
        }
    }
});

function update_timer() {
    if (--remaining_time < 0)
        return;
    
    minutes = Math.floor(remaining_time / 60);
    seconds = remaining_time - 60 * minutes;

    document.getElementById("timer").innerHTML = minutes + 'm ' + seconds + 's';
}

function reset_board() {
    for (let key in board) {
        div = document.getElementById(key)
        div.innerHTML = jackstraws_img[board[key]];
        div.classList.remove("highlighted");
    }
}

let which_one_div = document.getElementById('which_one')
let my_turn_div = document.getElementById('my_turn')

function update_globals(data) {
    remaining_time = parseInt(data.remaining_time) + 1
    board = data.board;
    all_moves = data.all_legal_moves;
    which_turn = data.which_player_turn;
    my_turn = data.my_turn;
    reset_board();

    my_turn_div.innerHTML =  my_turn ? 'Your turn' : 'Opponent turn'
    which_one_div.innerHTML =  my_turn && which_turn == 0 || !my_turn && which_turn == 1 ? 'You are chess' : 'You are checkers'
}