function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

let button = document.getElementById("matchmake")

button.addEventListener("click", async () => {
    const csrftoken = getCookie("csrftoken");
    let request = new Request(
        "/game/add_to_waiting_list/",
        {headers: {'X-CSRFToken': csrftoken}}
    );
    let data = await fetch(request, {
        method: "POST",
        credentials: "include"
    });
    console.log(data);
    request = new Request(
        "/game/try_to_pair/",
        {headers: {'X-CSRFToken': csrftoken}}
    );
    data = await fetch(request, {
        method: "POST",
        credentials: "include",
    });

    if (data.redirected)
        window.location.href = data.url;
    console.log(data)
});