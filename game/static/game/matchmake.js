function getCSRF() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

async function try_to_pair() {
    const csrftoken = getCSRF();
    const request = new Request(
        "/game/try_to_pair/",
        {headers: {'X-CSRFToken': csrftoken}}
    );
    let data = await fetch(request, {
        method: "POST",
        credentials: "include",
    });

    console.log("Trying to match")

    if (data.redirected) {
        console.log("Match found")
        window.location.href = data.url;
    }
}

let button = document.getElementById("matchmake")

button.addEventListener("click", async () => {
    // Add to queue
    const csrftoken = getCSRF();
    let request = new Request(
        "/game/add_to_waiting_list/",
        {headers: {'X-CSRFToken': csrftoken}}
    );

    let data = await fetch(request, {
        method: "POST",
        credentials: "include"
    });
    
    // Periodically try to pair
    setInterval(try_to_pair, 1000);
});