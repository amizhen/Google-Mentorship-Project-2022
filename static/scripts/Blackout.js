
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
    constructor(startDateTime, endDateTime, outerStart, outerEnd, data) {
        this.startDateTime = startDateTime;
        this.endDateTime = endDateTime;
        this.outerStart = outerStart;
        this.outerEnd = outerEnd;
        this.powerGenerated = extractData(data["gen_history"], startDateTime, endDateTime);
        this.storageHistory = extractData(data["storage_history"], startDateTime, endDateTime);
        this.net_history = extractData(data["net_history"], startDateTime, endDateTime);
        this.demand = extractData(data["demand"], startDateTime, endDateTime);

        this.kpowerGenerated = extractData(data["gen_history"], outerStart, outerEnd);
        this.kstorageHistory = extractData(data["storage_history"], outerStart, outerEnd);
        this.knet_history = extractData(data["net_history"], outerStart, outerEnd);
        this.kdemand = extractData(data["demand"], outerStart, outerEnd);
    }

    get dateTimeRange() {
        var arr = [];
        for (var time = this.outerStart; time < this.outerEnd; time += 3600) {
            arr.push(time);
        }
        return arr;
    }

    get totalPowerGenerated() {
        return this.powerGenerated.map(value => value[0] + value[1]);
    }

    get totalKPowerGenerated() {
        return this.kpowerGenerated.map(value => value[0] + value[1]);
    }

    get windPowerGenerated() {
        return this.powerGenerated.map(value => value[1]);
    }

    get kWindPowerGenerated() {
        return this.kpowerGenerated.map(value => value[1]);
    }

    get solarPowerGenerated() {
        return this.powerGenerated.map(value => value[0]);
    }

    get kSolarPowerGenerated() {
        return this.kpowerGenerated.map(value => value[0]);
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

var blackoutPadding = 1;

function getBlackoutsFromData() {
    var blackouts = [];
    var isInBlackout = false;
    var startBlackout = null; // first data for default

    var keys = Object.keys(data["storage_history"])
    var min = keys[0];
    var max = keys[keys.length - 1];

    for (key of keys) {
        if (!isInBlackout && data["storage_history"][key] < 0) {
            isInBlackout = true;
            startBlackout = +key;
        } else if (isInBlackout && data["storage_history"][key] >= 0) {
            blackouts.push(new Blackout(startBlackout, +key, Math.max(min, startBlackout - 3600 * blackoutPadding), Math.min(max, +key + 3600 * blackoutPadding), data))
            isInBlackout = false;
        }
    }

    if (isInBlackout) {
        var keys = Object.keys(data["storage_history"])
        blackouts.push(new Blackout(startBlackout, +key, Math.max(min, startBlackout - 3600 * blackoutPadding), Math.min(max, +key + 3600 * blackoutPadding), data));
    }
    return blackouts;
}