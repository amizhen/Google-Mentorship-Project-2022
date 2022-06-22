document.querySelector(".runButton").addEventListener('click', function () {
    this.classList.toggle('active')
    document.querySelectorAll(".dataContent").forEach(element => element.remove());
    document.querySelectorAll('.collapsible.open').forEach(elem => elem.classList.toggle("open"));
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
            blackouts = getBlackoutsFromData();
            updateDropDowns();
        })
})

function formatDateObject(date) {
    return `${date.getMonth() + 1}/${date.getDate()}/${date.getFullYear()} ${date.getHours()}:00`
}

function updateDropDowns() {
    var parentElem = document.querySelector("#dataPanel")
    var i = 0;
    for (blackout of blackouts) {
        var pDataContent = document.createElement('p');
        pDataContent.innerHTML = (blackout.endDateTime - blackout.startDateTime) / 3600 == 1 ? `
            <strong>Duration:</strong> 1 h <br>
            <strong>Energy Deficit:</strong> ${Math.abs(blackout.storageHistory[0])} kWh <br>
            <strong>Energy Generated:</strong> ${blackout.totalPowerGenerated[0]} kWh <br>
            <strong>Wind Energy Generated:</strong> ${blackout.windPowerGenerated[0]} kWh <br>
            <strong>Solar Energy Generated:</strong> ${blackout.solarPowerGenerated[0]} kWh
        ` : `
            <strong>Duration:</strong> ${(blackout.endDateTime - blackout.startDateTime) / 3600} h <br>
            <strong>Max Energy Deficit:</strong> ${Math.abs(Math.min(...blackout.storageHistory))} kWh <br>
            <strong>Min Energy Deficit:</strong> ${Math.abs(Math.max(...blackout.storageHistory))} kWh <br>
            <strong>Max Energy Generated:</strong> ${Math.max(...blackout.totalPowerGenerated)} kWh <br>
            <strong>Min Energy Generated:</strong> ${Math.min(...blackout.totalPowerGenerated)} kWh <br>
            <strong>Average Energy Deficit:</strong> ${blackout.averageDeficit} kWh <br>
            <strong>Average Energy Generated:</strong> ${blackout.averagePowerGenerated} kWh <br>
            <strong>Average Wind Energy Generated:</strong> ${blackout.averageWindGenerated} kWh <br>
            <strong>Average Solar Energy Generated:</strong> ${blackout.averageSolarGenerated} kWh
            `

        var innerDataContent = document.createElement('div');
        innerDataContent.className = "dataContent";
        innerDataContent.id = `blackout-${i++}`;
        innerDataContent.appendChild(pDataContent);

        var pDate = document.createElement('p');
        pDate.textContent = `${formatDateObject(new Date(blackout.startDateTime * 1000))} - ${formatDateObject(new Date(blackout.endDateTime * 1000))}`

        var innerCollapsible = document.createElement('div');
        innerCollapsible.className = "collapsible";
        innerCollapsible.appendChild(pDate);

        var outDataContent = document.createElement('div');
        outDataContent.className = "dataContent";
        outDataContent.appendChild(innerCollapsible);
        outDataContent.appendChild(innerDataContent);

        parentElem.appendChild(outDataContent)
    }

    addEventListenersToCollapsibles();
}