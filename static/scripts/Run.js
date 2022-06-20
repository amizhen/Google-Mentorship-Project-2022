document.querySelector(".runButton").addEventListener('click', function() {
    this.classList.toggle('active')
    fetch(window.location.href + "run",
    {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify({
            region,
            solarPlants,
            windPlants
        })
    }).then(res => {
        if (res.ok) {
            return res.json();
        } else alert('An unexpected error has occurred');
    }).then(jsonResponse => {
        this.classList.toggle('active')
        console.log(jsonResponse);
    })
})