// Importamos React Hooks y Axios
import { useState, useEffect } from 'react'; 
import axios from "axios";

// Componente principal
export default function Home() {

  // Estados para manejar el nombre de usuario y si está logueado
  const [username, setUsername] = useState(""); // Guarda el nombre del usuario
  const [isLoggedIn, setLoggedIn] = useState(false); // Indica si el usuario está logueado

  // Efecto para verificar si el usuario está logueado cuando el componente se monta
  useEffect(() => {
    const checkLoggedInUser = async () => {
      try {
        // Obtenemos el token de acceso del almacenamiento local
        const token = localStorage.getItem("accessToken");
        if (token) {
          // Configuramos los headers con el token para la solicitud
          const config = {
            headers: {
              "Authorization": `Bearer ${token}`
            }
          };
          // Hacemos la solicitud a la API para obtener los datos del usuario
          const response = await axios.get("http://127.0.0.1:8000/api/user/", config);
          setLoggedIn(true); // Marcamos que el usuario está logueado
          setUsername(response.data.username); // Guardamos el nombre del usuario
        } else {
          // Si no hay token, el usuario no está logueado
          setLoggedIn(false);
          setUsername("");
        }
      } catch (error) {
        // Si hay un error, limpiamos el estado y mostramos el error en consola
        console.error(error);
        setLoggedIn(false);
        setUsername("");
      }
    };

    // Llamamos a la función al montar el componente
    checkLoggedInUser();
  }, []); // Dependencias vacías para ejecutar solo una vez

  // Función para manejar el logout del usuario
  const handleLogout = async () => {
    try {
      // Obtenemos los tokens de acceso y refresh del almacenamiento local
      const accessToken = localStorage.getItem("accessToken");
      const refreshToken = localStorage.getItem("refreshToken");

      if (accessToken && refreshToken) {
        // Configuramos los headers con el token de acceso
        const config = {
          headers: {
            "Authorization": `Bearer ${accessToken}`
          }
        };
        // Enviamos la solicitud de logout a la API con el token de refresh
        await axios.post("http://127.0.0.1:8000/api/logout/", { "refresh": refreshToken }, config);
        
        // Eliminamos los tokens del almacenamiento local
        localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");

        // Actualizamos el estado para reflejar que el usuario ha cerrado sesión
        setLoggedIn(false);
        setUsername("");
        console.log("Log out successful!");
      }
    } catch (error) {
      // Mostramos cualquier error en consola
      console.error("Failed to logout", error.response?.data || error.message);
    }
  };

  // Renderizamos el componente
  return (
    <div>
      {isLoggedIn ? ( // Si el usuario está logueado
        <>
          <h2>Hi, {username}. Thanks for logging in!</h2>
          <button onClick={handleLogout}>Logout</button> {/* Botón para cerrar sesión */}
        </>
      ) : ( // Si el usuario no está logueado
        <h2>Please Login</h2>
      )}
    </div>
  );
}
