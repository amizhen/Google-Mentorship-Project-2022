function addEventListenerToInput(id, func) {
    document.getElementById(id).addEventListener('input', (e) => {
        var value = +e.target.value;
        if (value > +e.target.max || value < +e.target.min) {
            if (!e.target.classList.contains("error")) {
                e.target.classList.toggle("error");
                var span = e.target.previousElementSibling;
                span.style.display = "inline";
            }
        } else {
            if (e.target.classList.contains("error")) {
                e.target.classList.toggle("error");
                var span = e.target.previousElementSibling;
                span.style.display = "none";
            }
            func(value)
        }
    })  
}

addEventListenerToInput('powerPercentage', val => percentagePower = val)
addEventListenerToInput('solarFarmSize', val => solarFarmSize = val)
addEventListenerToInput('windFarmSize', val => windFarmSize = val)