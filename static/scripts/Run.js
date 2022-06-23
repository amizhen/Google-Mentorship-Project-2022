document.querySelector(".runButton").addEventListener('click', function () {
    this.classList.toggle('active')
    document.querySelectorAll(".dataContent").forEach(element => element.remove());
    document.querySelectorAll('.collapsible.open').forEach(elem => elem.classList.toggle("open"));
    document.body.style.cursor = "wait";
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
                storageCap,
                startDate,
                endDate
            })
        }).then(res => {
            if (res.ok) {
                return res.json();
            } else alert('An unexpected error has occurred');
        }).then(jsonResponse => {
            this.classList.toggle('active')
            document.body.style.cursor = "default";
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
            <strong>Energy Deficit:</strong> ${Math.abs(blackout.storageHistory[0])} MWh <br>
            <strong>Energy Generated:</strong> ${blackout.totalPowerGenerated[0]} MWh <br>
            <strong>Wind Energy Generated:</strong> ${blackout.windPowerGenerated[0]} MWh <br>
            <strong>Solar Energy Generated:</strong> ${blackout.solarPowerGenerated[0]} MWh
        ` : `
            <strong>Duration:</strong> ${(blackout.endDateTime - blackout.startDateTime) / 3600} h <br>
            <strong>Max Energy Deficit:</strong> ${Math.abs(Math.min(...blackout.storageHistory))} MWh <br>
            <strong>Min Energy Deficit:</strong> ${Math.abs(Math.max(...blackout.storageHistory))} MWh <br>
            <strong>Max Energy Generated:</strong> ${Math.max(...blackout.totalPowerGenerated)} MWh <br>
            <strong>Min Energy Generated:</strong> ${Math.min(...blackout.totalPowerGenerated)} MWh <br>
            <strong>Average Energy Deficit:</strong> ${Math.abs(blackout.averageDeficit)} MWh <br>
            <strong>Average Energy Generated:</strong> ${blackout.averagePowerGenerated} MWh <br>
            <strong>Average Wind Energy Generated:</strong> ${blackout.averageWindGenerated} MWh <br>
            <strong>Average Solar Energy Generated:</strong> ${blackout.averageSolarGenerated} MWh
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