var map;
var marker;

function iniciarMap() {
  var coord = { lat: -34.1701324, lng: -70.7406259 };
  map = new google.maps.Map(document.getElementById('map'), {
    zoom: 10,
    center: coord
  });
  marker = new google.maps.Marker({
    position: coord,
    map: map
  });
}

function cambiarCoordenadas(latitud, longitud) {
  // Obtener las nuevas coordenadas
  var nuevasCoordenadas = { lat: latitud, lng: longitud };

  // Actualizar la posición del marcador
  marker.setPosition(nuevasCoordenadas);

  // Centrar el mapa en las nuevas coordenadas
  map.setCenter(nuevasCoordenadas);
}

(() => {
  'use strict'

  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  const forms = document.querySelectorAll('.needs-validation')

  // Loop over them and prevent submission
  Array.from(forms).forEach(form => {
      form.addEventListener('submit', event => {
          if (!form.checkValidity()) {
              event.preventDefault()
              event.stopPropagation()
          }

          form.classList.add('was-validated')
      }, false)
  })
})()