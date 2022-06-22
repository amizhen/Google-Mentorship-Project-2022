var region = ""
var percentagePower = 25
var windFarmSize = 100 // number of plants
var solarFarmSize = 100 // in square kilometersmeters
var solarPlants = []
var windPlants = []
var storageCap = 50000

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