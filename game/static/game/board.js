const socket_url = `wss://${window.location.host}/game_socket/`;
const socket = new WebSocket(socket_url);
const current_path = window.location.pathname.substring(window.location.pathname.lastIndexOf('/')+1)

socket.onopen = function(e) {
    socket.send(JSON.stringify({
        'type': 'initialize',
        'message': current_path
    }));
}

console.log( window.location.hostname)

socket.onmessage = function(e){
    let data = JSON.parse(e.data)
    console.log('Data:', data)

    if (data.type === 'timeout_message')
        window.location.href = window.location.hostname

    document.getElementById('messages').insertAdjacentHTML(
        'beforeend', `<div><p>${data.message}</p></div>`
    )
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