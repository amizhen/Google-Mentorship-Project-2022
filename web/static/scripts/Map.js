mapboxgl.accessToken = 'pk.eyJ1IjoibGVnZW5kb2YiLCJhIjoiY2wzZGs4bm1nMDk5cjNkbzVxZ3FhNDNlaiJ9.TsW1Ops9bd0umixj9t9EbQ';

const map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v11',
    center: [-74.5, 40],
    zoom: 9
});

const markers = [];

function selectPowerPlant(lat_coord, lng_coord, endpoint, className) {
    fetch(window.location.href + endpoint,
        {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({ lat: lat_coord, lng: lng_coord })
        }).then(res => {
            if (res.ok) {
                return res.json()
            } else { alert("An unexpected error has occurred.") }
        })

    var marker_element = document.createElement('div');
    marker_element.className = className;

    var marker = new mapboxgl.Marker({ element: marker_element })
    markers.push(marker);
    marker.setLngLat([lng_coord, lat_coord]).addTo(map);

    var popups = document.getElementsByClassName("mapboxgl-popup");
    if (popups.length) {
        popups[0].remove();
    }
}

function generatePopup(e) {
    return new mapboxgl.Popup(
        {
            offset: 5,
            closeButton: false,
            maxWidth: 480,
            className: "powerplantSelectPopup"
        }
    ).setLngLat([e.lngLat.lng, e.lngLat.lat]).setHTML(
        `
            <button class="powerplantButton" onclick="selectPowerPlant(${e.lngLat.lat}, ${e.lngLat.lng}, 'place/solar', 'solarMarker');">Solar Panel</button>
            <button class="powerplantButton" onclick="selectPowerPlant(${e.lngLat.lat}, ${e.lngLat.lng}, 'place/wind', 'windMarker');">Wind Plant</button>
        `
    )
}

// implement this
function removePowerPlant(index) {
    markers[index].remove();
    markers.splice(index, 1);
}

map.on('click', (e) => {
    generatePopup(e).addTo(map);
}); 