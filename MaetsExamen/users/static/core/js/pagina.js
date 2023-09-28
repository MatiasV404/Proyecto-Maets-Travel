var isLoggedIn = false;

// Función para verificar si el usuario ha iniciado sesión
function checkLoginStatus() {
  // Realiza alguna lógica para determinar si el usuario ha iniciado sesión
  // Puedes utilizar cookies, almacenamiento local, tokens de autenticación, etc.

  // Ejemplo: si el usuario tiene un token de autenticación válido, se considera que ha iniciado sesión
  var authToken = localStorage.getItem("authToken");
  isLoggedIn = authToken !== null && authToken !== undefined;

  // Actualiza la interfaz de usuario según el estado de inicio de sesión
  updateUI();
}

// Función para actualizar la interfaz de usuario según el estado de inicio de sesión
function updateUI() {
  var iniciarSesionLink = document.getElementById("iniciarSesionLink");
  var registrarseLink = document.getElementById("registrarseLink");
  var profileButton = document.getElementById("profileButton");

  if (isLoggedIn) {
    // Si el usuario ha iniciado sesión, muestra el botón de perfil y oculta los enlaces "Iniciar Sesión" y "Registrarse"
    iniciarSesionLink.style.display = "none";
    registrarseLink.style.display = "none";
    profileButton.style.display = "block";
  } else {
    // Si el usuario no ha iniciado sesión, muestra los enlaces "Iniciar Sesión" y "Registrarse" y oculta el botón de perfil
    iniciarSesionLink.style.display = "block";
    registrarseLink.style.display = "block";
    profileButton.style.display = "none";
  }
}

// Llama a la función checkLoginStatus para verificar el estado de inicio de sesión al cargar la página
checkLoginStatus();