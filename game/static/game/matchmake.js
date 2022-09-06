let button = document.getElementById("matchmake")

button.addEventListener("click", async () => {
    // Add to queue
    const csrftoken = getCSRF();
    let request = new Request(
        "/game/add_to_waiting_list/",
        {headers: {'X-CSRFToken': csrftoken}}
    );

    let response = await fetch(request, {
        method: "POST",
        credentials: "include"
    });

    redirect_if_possible(response);
    
    // Periodically try to pair
    setInterval(try_to_pair, 1000);
});

function getCSRF() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

async function try_to_pair() {
    console.log("Trying to match");

    const csrftoken = getCSRF();
    const request = new Request(
        "/game/try_to_pair/",
        {headers: {'X-CSRFToken': csrftoken}}
    );
    let response = await fetch(request, {
        method: "POST",
        credentials: "include",
    });
    
    redirect_if_possible(response);
}

function redirect_if_possible(response) {
    if (response.redirected) {
        console.log("Match found");
        window.location.href = response.url;
    }
}