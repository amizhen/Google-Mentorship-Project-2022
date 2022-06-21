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
            windPlants,
            percentagePower,
            windFarmSize,
            solarFarmSize,
            storageCap
        })
    }).then(res => {
        if (res.ok) {
            return res.json();
        } else alert('An unexpected error has occurred');
    }).then(jsonResponse => {
        this.classList.toggle('active')
        data = jsonResponse;
        console.log(jsonResponse); // TODO: Remove this
    })
})

function updateDropDowns() {
    
}