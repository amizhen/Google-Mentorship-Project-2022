
function extractData(data, start, end) {
    var datetimes = Object.keys(data);
    return datetimes.filter(function(datetime) {
        return datetime >= start && datetime <= end;
    }).map(datetime => data[datetime]);
}

class Blackout {
    constructor(startDateTime, endDateTime, data) {
        this.startDateTime = startDateTime;
        this.endDateTime = endDateTime;
        
    }
}

var test = {
    1: 2,
    2: 3,
    3: 4,
    4: 6
}

console.log(extractData(test, 2, 4));