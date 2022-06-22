function addEventListenerToValueInput(id, func) {
    document.getElementById(id).addEventListener('input', (e) => {
        var value = +e.target.value;
        if (value > +e.target.max || value < +e.target.min) {
            if (!e.target.classList.contains("error")) {
                e.target.classList.toggle("error");
                var span = e.target.previousElementSibling;
                span.style.display = "inline";
            }
            func(value > +e.target.max ? +e.target.max : +e.target.min)
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

addEventListenerToValueInput('powerPercentage', val => percentagePower = val)
addEventListenerToValueInput('solarFarmSize', val => solarFarmSize = val)
addEventListenerToValueInput('windFarmSize', val => windFarmSize = val)
addEventListenerToValueInput('storageCap', val => storageCap = val)

var startDateElem = document.getElementById("startDate");
var endDateElem = document.getElementById("endDate")

function toggleDateRangeError() {
    if (startDateElem.classList.contains('error')) {
        startDateElem.previousElementSibling.style.display = "none";
        endDateElem.previousElementSibling.style.display = "none";
    } else {
        startDateElem.previousElementSibling.style.display = "inline";
        endDateElem.previousElementSibling.style.display = "inline";
    }
    startDateElem.classList.toggle('error')
    endDateElem.classList.toggle('error')
}

function createDateObj(data) {
    var str = "";
    str += data[0] + "-";
    str += data[1] < 10 ? "0" + data[1] + "-" : data[1] + "-";
    str += data[2] < 10 ? "0" + data[2] : data[2];
    return new Date(str); 
}

startDateElem.addEventListener('input', e => {
    var start = new Date(e.target.value);
    var end = createDateObj(endDate)
    if (start < end && start >= new Date(e.target.min) && start < new Date(e.target.max) && start != end) {
        if (e.target.classList.contains('error')) {
            toggleDateRangeError()
        }
        startDate = [start.getUTCFullYear(), start.getUTCMonth() + 1, start.getUTCDate()]
    } else {
        if (!e.target.classList.contains('error')) {
            toggleDateRangeError()
        }
    }
})

endDateElem.addEventListener('input', e => {
    var start = createDateObj(startDate);
    var end = new Date(e.target.value)
    if (end > start && end > new Date(e.target.min) && end <= new Date(e.target.max)) {
        if (e.target.classList.contains('error')) {
            toggleDateRangeError()
        }
        endDate = [end.getUTCFullYear(), end.getUTCMonth() + 1, end.getUTCDate()]
    } else {
        if (!e.target.classList.contains('error')) {
            toggleDateRangeError()
        }
    }
})
