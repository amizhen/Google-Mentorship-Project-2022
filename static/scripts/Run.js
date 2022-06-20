function run() {
    fetch(window.location.href + "run",
    {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'Accept': 'application/json'
        },
        body: ""
    }).then(res => {
        if (res.ok) {
            return res.json();
        } else alert('An unexpected error has occurred');
    }).then(jsonResponse => {
        console.log(jsonResponse);
    })
}