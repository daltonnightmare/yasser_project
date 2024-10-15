function initMap() {
    var map = L.map('map').setView([12.3714, -1.5197], 13); // Coordonnées de Ouagadougou

    // Ajouter une couche de tuiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap'
    }).addTo(map);

    // Ajouter un marqueur
    var marker = L.marker([12.3714, -1.5197]).addTo(map); // Marqueur initial à Ouagadougou

    // Événement de clic sur la carte
    map.on('click', function(e) {
        // Récupérer les coordonnées du clic
        var lat = e.latlng.lat;
        var lng = e.latlng.lng;

        // Mettre à jour le champ caché avec les coordonnées
        document.getElementById('localisation').value = lat + ',' + lng;

        // Déplacer le marqueur à la position cliquée
        marker.setLatLng([lat, lng]);
    });
}

// Appeler la fonction d'initialisation de la carte
document.addEventListener('DOMContentLoaded', initMap);
