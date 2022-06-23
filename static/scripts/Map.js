mapboxgl.accessToken = 'pk.eyJ1IjoibGVnZW5kb2YiLCJhIjoiY2wzZGs4bm1nMDk5cjNkbzVxZ3FhNDNlaiJ9.TsW1Ops9bd0umixj9t9EbQ';

const map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/outdoors-v11?optimize=true',
    center: regionMap[region]["coord"],
    zoom: regionMap[region]["zoom"]
});

map.on('load', () => {
    map.getStyle().layers.map(function(layer) {
        if (layer.id.indexOf("road") >= 0 || layer.id.indexOf("label") >= 0) {
            map.setLayoutProperty(layer.id, "visibility", "none");
        }
    })
});

map.dragRotate.disable();
/* map.touchZoomRotate.disable(); */

var markers = [];

function selectPowerPlant(lat_coord, lng_coord, className) {
    if (className == "solarMarker") {
        solarPlants.push([lat_coord, lng_coord]);
    } else if (className == "windMarker") {
        windPlants.push([lat_coord, lng_coord]);
    }

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
            offset: 2,
            closeButton: false,
            maxWidth: 480,
            className: "powerplantSelectPopup"
        }
    ).setLngLat([e.lngLat.lng, e.lngLat.lat]).setHTML(
        `
            <button class="powerplantButton" onclick="selectPowerPlant(${e.lngLat.lat}, ${e.lngLat.lng}, 'solarMarker');">Solar Panel</button>
            <button class="powerplantButton" onclick="selectPowerPlant(${e.lngLat.lat}, ${e.lngLat.lng}, 'windMarker');">Wind Plant</button>
        `
    )
}

function removePowerPlants() {
    markers.forEach(marker => marker.remove());
    markers = [];
    solarPlants = [];
    windPlants = [];
}

map.on('click', (e) => {
    generatePopup(e).addTo(map);
}); 

function moveToLocation() {
    map.flyTo({
        center: regionMap[region]["coord"],
        zoom: regionMap[region]["zoom"],
        speed: 0.4
    })
}