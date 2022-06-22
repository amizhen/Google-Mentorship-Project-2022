
function extractData(data, start, end) {
    var datetimes = Object.keys(data);
    return datetimes.filter(function(datetime) {
        return datetime >= start && datetime < end;
    }).map(datetime => data[datetime]);
}

function avg(arr) {
    return arr.reduce((a, b) => a + b, 0) / arr.length;
}

class Blackout {
    constructor(startDateTime, endDateTime, data) {
        this.startDateTime = startDateTime;
        this.endDateTime = endDateTime;
        this.powerGenerated = extractData(data["gen_history"], startDateTime, endDateTime);
        this.storageHistory = extractData(data["storage_history"], startDateTime, endDateTime);
        this.net_history = extractData(data["net_history"], startDateTime, endDateTime);
        this.demand = extractData(data["demand"], startDateTime, endDateTime);
    }

    get dateTimeRange() {
        var arr = [];
        for (var time = this.startDateTime; time < this.endDateTime; time += 3600) {
            arr.push(time);
        }
        return arr;
    }

    get totalPowerGenerated() {
        return this.powerGenerated.map(value => value[0] + value[1]);
    }

    get windPowerGenerated() {
        return this.powerGenerated.map(value => value[1]);
    }

    get solarPowerGenerated() {
        return this.powerGenerated.map(value => value[0]);
    }

    get averagePowerGenerated() {
        return avg(this.totalPowerGenerated);
    }

    get averageWindGenerated() {
        return avg(this.windPowerGenerated);
    }

    get averageSolarGenerated() {
        return avg(this.solarPowerGenerated);
    }

    get averageDeficit() {
        return avg(this.storageHistory);
    }

}

function getBlackoutsFromData(data) {
    var blackouts = [];
    var isInBlackout = false;
    var startBlackout = null; // first data for default
    for (key in data["storage_history"]) {
        if (!isInBlackout && data["storage_history"][key] < 0) {
            isInBlackout = true;
            startBlackout = +key;
        } else if (isInBlackout && data["storage_history"][key] >= 0) {
            blackouts.push(new Blackout(startBlackout, +key, data))
            isInBlackout = false;
        }
    }

    if (isInBlackout) {
        var keys = Object.keys(data["storage_history"])
        blackouts.push(new Blackout(startBlackout, +keys[keys.length - 1] + 3600, data));
    }

    return blackouts;
}