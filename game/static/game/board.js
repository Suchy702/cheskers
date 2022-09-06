const socket_url = `ws://${window.location.host}/game_socket/`;

const chatSocket = new WebSocket(socket_url);

chatSocket.onmessage = function(e){
    let data = JSON.parse(e.data)
    console.log('Data:', data)

    if(data.type === 'chat'){
        let messages = document.getElementById('messages')

        messages.insertAdjacentHTML('beforeend', `<div>
                                <p>${data.message}</p>
                            </div>`)
    }
}

let form = document.getElementById('form')
form.addEventListener('submit', (e)=> {
    e.preventDefault()
    let message = e.target.message.value 
    chatSocket.send(JSON.stringify({
        'message':message
    }))
    form.reset()
})