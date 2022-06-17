var data = [];
var zeroLine = [];

var fillColors = data.map((value) => value["y"] < 0 ? "rgba(255, 0, 0, 0.2)" : "rgba(0, 255, 0, 0.2)");

function generateData() {
    let prev = 0;
    for (let i = 0; i < 1000; i++) {
        prev += 5 - Math.random() * 10;
        data.push({ x: i, y: prev });
        zeroLine.push({x: i, y: 0});
    }
}

generateData();

const delayBetweenPoints = 100;
const previousY = (ctx) => ctx.index === 0 ? ctx.chart.scales.y.getPixelForValue(0) : ctx.chart.getDatasetMeta(ctx.datasetIndex).data[ctx.index - 1].getProps(['y'], true).y;

const animation = {
    x: {
        type: 'number',
        easing: 'linear',
        duration: delayBetweenPoints,
        from: NaN,
        delay(ctx) {
            if (ctx.type !== 'data' || ctx.xStarted) {
                return 0;
            }
            ctx.xStarted = true;
            return ctx.index * delayBetweenPoints
        }
    },
    y: {
        type: 'number',
        easing: 'linear',
        duration: delayBetweenPoints,
        from: previousY,
        delay(ctx) {
            if (ctx.type !== 'data' || ctx.yStarted) {
                return 0;
            }
            ctx.yStarted = true;
            return ctx.index * delayBetweenPoints;
        }
    }
};

var config = {
    type: 'line',
    data: {
        datasets: [{
            borderColor: '#FFFFFF',
            borderWidth: 1,
            radius: 0,
            data: data.slice(0, 100),
            fill: {
                target: "origin",
                above: "rgba(0, 255, 0, 0.4)",
                below: "rgba(255, 0, 0, 0.4)"
            }
        },
        {
            borderColor: '#FFFFFF',
            borderWidth: 1,
            radius: 0,
            data: zeroLine.slice(0, 100)
        }]
    },
    options: {
        animation,
        plugins: { legend: false },
        scales: {
            x: {
                type: 'linear',
                ticks: { color: "#FFFFFF" },
                grid: { borderColor: "#FFFFFF" }
            },
            y: {
                type: 'linear',
                ticks: { color: "#FFFFFF" },
                grid: { borderColor: "#FFFFFF" }
            }
        }
    }
}

var chart = new Chart(
    $("#chart"), config
)

function resetChart() {
    chart.destroy();
    data = [];
    generateData();
    config["data"]["datasets"][0]["data"] = data.slice(0,100);
    chart = new Chart($("#chart"), config);
}