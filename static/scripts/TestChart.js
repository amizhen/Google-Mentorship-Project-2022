function dateToString(epoch) {
    var datetime = new Date(epoch * 1000);
    return `${datetime.getMonth() + 1}-${datetime.getDate()}-${datetime.getFullYear()} ${datetime.getHours()}:00`;
}

function generateStorageChart() {
    chart.destroy();
    energyStoGraphConfig["options"]["scales"]["x"]["labels"] = blackouts[blackoutIndex].dateTimeRange.map(i => dateToString(i));

    data = [];
    for (var i = 0; i < blackouts[blackoutIndex].dateTimeRange.length; i++) {
        data.push([dateToString(blackouts[blackoutIndex].dateTimeRange[i]), blackouts[blackoutIndex].kstorageHistory[i]]);
    }

    energyStoGraphConfig["data"]["datasets"][0]["data"] = data;
    chart = new Chart($("#chart"), energyStoGraphConfig);
}

function generateGenChart() {
    chart.destroy();
    energyGenerationGraphConfig["options"]["scales"]["x"]["labels"] = blackouts[blackoutIndex].dateTimeRange.map(i => dateToString(i));

    var blackout = blackouts[blackoutIndex];

    var windData = [];
    var solarData = [];
    var totalData = [];

    for (var i = 0; i < blackout.dateTimeRange.length; i++) {
        var dateStr = dateToString(blackout.dateTimeRange[i])
        windData.push([dateStr, blackout.kWindPowerGenerated[i]]);
        solarData.push([dateStr, blackout.kSolarPowerGenerated[i]]);
        totalData.push([dateStr, blackout.totalKPowerGenerated[i]]);
    }

    energyGenerationGraphConfig["data"]["datasets"][0]["data"] = windData;
    energyGenerationGraphConfig["data"]["datasets"][1]["data"] = solarData;
    energyGenerationGraphConfig["data"]["datasets"][2]["data"] = totalData;

    chart = new Chart($('#chart'), energyGenerationGraphConfig);
}

function generateDemandChart() {
    chart.destroy();
    demandGraphConfig["options"]["scales"]["x"]["labels"] = blackouts[blackoutIndex].dateTimeRange.map(i => dateToString(i));

    data = [];
    for (var i = 0; i < blackouts[blackoutIndex].dateTimeRange.length; i++) {
        data.push([dateToString(blackouts[blackoutIndex].dateTimeRange[i]), blackouts[blackoutIndex].kdemand[i]]);
    }

    demandGraphConfig["data"]["datasets"][0]["data"] = data;
    chart = new Chart($("#chart"), demandGraphConfig);
}

function generateNetChart() {
    chart.destroy();
    netChangeGraphConfig["options"]["scales"]["x"]["labels"] = blackouts[blackoutIndex].dateTimeRange.map(i => dateToString(i));

    data = [];
    for (var i = 0; i < blackouts[blackoutIndex].dateTimeRange.length; i++) {
        data.push([dateToString(blackouts[blackoutIndex].dateTimeRange[i]), blackouts[blackoutIndex].knet_history[i]]);
    }

    netChangeGraphConfig["data"]["datasets"][0]["data"] = data;
    chart = new Chart($("#chart"), netChangeGraphConfig);
}

function generateGraph() {
    if (blackoutIndex == -1) {
        return;
    }

    switch (graphMode) {
        case 'Storage':
            generateStorageChart();
            break;
        case 'Generation':
            generateGenChart();
            break;
        case 'Demand':
            generateDemandChart();
            break;
        case 'Net Change':
            generateNetChart();
            break;
    }
}

document.querySelectorAll('.graphButton').forEach(elem =>
    elem.addEventListener('click', e => {
        if (!elem.classList.contains('active')) {
            graphMode = elem.textContent;
            document.querySelector('.graphButton.active').classList.toggle('active');
            elem.classList.toggle('active');
            document.querySelector('#chartContainer > span').textContent = `Energy ${graphMode} Graph`;
            generateGraph();
        }
    })
)

document.querySelectorAll('.graphButton').forEach(elem => {
    if (elem.textContent == 'Storage') {
        elem.classList.toggle("active");
        graphMode = 'Storage'
    }
})

var chart = new Chart(
    $("#chart"), energyStoGraphConfig
)