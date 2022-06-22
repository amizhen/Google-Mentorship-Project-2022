var region = ""

var regionMap = {
    "New York": {
        "coord": [-75.29431981428755, 41.968898861229064],
        "zoom": 6.18
    },
    "California": {
        "coord": [-120.44734591530451, 35.62064384761716],
        "zoom": 5
    },
    "Florida": {
        "coord": [-84.20241994744073, 26.42828845522473],
        "zoom": 5.9
    },
    "New England": {
        "coord": [-71.5658320324526, 44.334146985948166],
        "zoom": 5.8
    },
    "Tennessee": {
        "coord": [-85.86549142844251, 35.76639768350098],
        "zoom": 5.9
    },
    "Texas": {
        "coord": [-98.94458440209038, 31.751587499650128],
        "zoom": 5.1
    },
    "North Carolina & South Carolina": {
        "coord": [-79.85268253156312, 33.05334867920635],
        "zoom": 6
    },
    "Central": {
        "coord": [-98.281848622276, 43.56810866464568],
        "zoom": 4.9
    },
    "Mid-Atlantic": {
        "coord": [-80.44748275282002, 39.11034002063266],
        "zoom": 5.5
    },
    "Midwest": {
        "coord": [-86.1589375539239, 42.06725994414461],
        "zoom": 5.2
    },
    "North West": {
        "coord": [-113.62174282264907, 43.51164500713821],
        "zoom": 4.7
    },
    "South East": {
        "coord": [-88.14832407220518, 32.11557872919383],
        "zoom": 5.3
    },
    "South West": {
        "coord": [-109.03430441839342, 34.956532325008666],
        "zoom": 4.8
    }
}

var percentagePower = 25
var windFarmSize = 100 // number of plants
var solarFarmSize = 100 // in square kilometersmeters
var solarPlants = []
var windPlants = []
var storageCap = 50000
var startDate = [2020, 1, 1]
var endDate = [2021, 1, 1]

var data = null
var blackouts = [];
var blackoutIndex = -1;

var graphMode = null;

const defaultDelay = 100;
const previousY = (ctx) => {
    return ctx.index === 0 ? ctx.chart.scales.y.getPixelForValue(0) : ctx.chart.getDatasetMeta(ctx.datasetIndex).data[ctx.index - 1].getProps(['y'], true).y;
}


const scales = {
    x: {
        type: 'category',
        labels: [],
        ticks: { color: "#FFFFFF" },
        grid: { 
            borderColor: "#FFFFFF",
            color: "rgba(98, 98, 98, 0.4)"
        },
        title: {
            display: true,
            text: "Date and Time",
            color: "#FFFFFF"
        }
    },
    y: {
        type: 'linear',
        ticks: { color: "#FFFFFF" },
        grid: { 
            borderColor: "#FFFFFF",
            color: "rgba(98, 98, 98, 0.4)"
        },
        title: {
            display: true,
            text: "Energy [kWh]",
            color: "#FFFFFF"
        }
    }
}

const animation = {
    x: {
        type: 'number',
        easing: 'linear',
        duration: defaultDelay,
        from: NaN,
        delay(ctx) {
            if (ctx.type !== 'data' || ctx.xStarted) {
                return 0;
            }
            ctx.xStarted = true;
            return ctx.index * defaultDelay
        }
    },
    y: {
        type: 'number',
        easing: 'linear',
        duration: defaultDelay,
        from: previousY,
        delay(ctx) {
            if (ctx.type !== 'data' || ctx.yStarted) {
                return 0;
            }
            ctx.yStarted = true;
            return ctx.index * defaultDelay;
        }
    }
}

var energyStoGraphConfig = {
    type: 'line',
    data: {
        datasets: [{
            borderColor: '#FFFFFF',
            borderWidth: 1,
            radius: 0,
            data: [],
            fill: {
                target: "origin",
                above: "rgba(0, 255, 0, 0.4)",
                below: "rgba(255, 0, 0, 0.4)"
            }
        }]
    },
    options: {
        animation,
        interaction: {
            intersect: false
        },
        plugins: { 
            legend: false,
        },
        scales
    }
}

var energyGenerationGraphConfig = {
    type: 'line',
    data: {
        datasets: [{ // wind
            borderColor: '#0000FF',
            borderWidth: 1,
            radius: 0,
            data: []
        },
        { // solar
            borderColor: '#FF0000',
            borderWidth: 1,
            radius: 0,
            data: []
        },
        { // total
            borderColor: '#FFFFFF',
            borderWidth: 1,
            radius: 0,
            data: []
        }]
    },
    options: {
        animation,
        interaction: {
            intersect: false
        },
        plugins: { 
            legend: false,
        },
        scales
    }
}

var demandGraphConfig = {
    type: 'line',
    data: {
        datasets: [{
            borderColor: '#FFFFFF',
            borderWidth: 1,
            radius: 0,
            data: []
        }]
    },
    options: {
        animation,
        interaction: {
            intersect: false
        },
        plugins: { 
            legend: false,
        },
        scales
    }
}

var netChangeGraphConfig = {
    type: 'line',
    data: {
        datasets: [{
            borderColor: '#FFFFFF',
            borderWidth: 1,
            radius: 0,
            data: [],
            fill: {
                target: "origin",
                above: "rgba(0, 255, 0, 0.4)",
                below: "rgba(255, 0, 0, 0.4)"
            }
        }]
    },
    options: {
        animation,
        interaction: {
            intersect: false
        },
        plugins: { 
            legend: false,
        },
        scales
    }
}