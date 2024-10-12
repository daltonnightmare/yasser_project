function map_init_basic (map, options) {
    // Coordonnées de Ouagadougou
    var center = [12.3714, -1.5197];
    
    // Définir la vue sur Ouagadougou
    map.setView(center, 12);  // Zoom augmenté pour une meilleure vue de la ville

    // Définir les limites de la carte pour le Burkina Faso (inchangé)
    var southWest = L.latLng(9.4, -5.5);
    var northEast = L.latLng(15.1, 2.4);
    var bounds = L.latLngBounds(southWest, northEast);

    // Restreindre la vue à ces limites
    map.setMaxBounds(bounds);
    map.on('drag', function() {
        map.panInsideBounds(bounds, { animate: false });
    });

    // Ajouter une couche OpenStreetMap
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // Ajouter un marqueur pour Ouagadougou
    L.marker(center).addTo(map)
        .bindPopup('Ouagadougou')
        .openPopup();
}