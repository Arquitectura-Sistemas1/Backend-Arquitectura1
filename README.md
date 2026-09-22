# Guía Completa de Integración y Consumo de API para Frontend (React + Vite)

Documentación técnica y manual de consumo del backend para el equipo de desarrollo Frontend utilizando **React + Vite**.

---

## 1. Configuración del Entorno en Vite

### 1.1. Variables de Entorno en Vite (`.env`)
En Vite, las variables de entorno deben comenzar obligatoriamente con el prefijo `VITE_` y se acceden mediante `import.meta.env`.

Crea un archivo `.env` en la raíz de tu proyecto React + Vite:
```env
VITE_API_BASE_URL=https://luxury-roster-uncouth.ngrok-free.dev
```

### 1.2. Transmisión de Token JWT (Cookie HTTP-Only)
- El backend maneja la autenticación mediante la cookie HTTP-Only securizada `access_token`.
- En **todas** las peticiones HTTP realizadas desde React (Fetch API o Axios), se DEBE incluir la opción de credenciales:
  - **Fetch API**: `credentials: "include"`
  - **Axios**: `withCredentials: true`

#### Ejemplo de Configuración de Cliente Axios en React + Vite (`src/api/axios.js`):
```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

export default api;
```

#### Configuración Opcional de Proxy en `vite.config.js` (para entorno de desarrollo local):
```javascript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'https://luxury-roster-uncouth.ngrok-free.dev',
        changeOrigin: true,
        secure: false,
      },
    },
  },
});
```

---

### 1.3. Almacenamiento y Cache del ID de Pedido Activo (`pedido_id`)
- **Regla de Arquitectura**: No realizar consultas redundantes para obtener el ID del pedido activo.
- Al iniciar sesión (`POST /auth/login`), la respuesta devuelve la propiedad `pedido_id` (entero o `null`).
- Guardar `pedido_id` en el estado global de React (Context API, Zustand, Redux) o en `localStorage`.
- Al llamar a `POST /comercial/agregar-item-pedido` o `POST /comercial/crear-pedido`, la respuesta incluirá el `PedidoID` activo para actualizar la cache en React.
- Al pagar el pedido (`POST /comercial/procesar-pago`), el pedido se completa y la variable de cache `pedido_id` DEBE actualizarse a `null`.

---

## 2. Regla Fundamental de Frontend: Formularios y Llaves Foráneas (FKs)

> [!IMPORTANT]
> Queda totalmente prohibido solicitar al usuario que ingrese IDs numéricos manualmente en cualquier formulario.

- Todos los IDs de llaves foráneas (`plataforma_id`, `clasificacion_id`, `region_id`, `tarifa_id`, `descuento_id`, `genero_id`, `desarrolladora_id`, `MetodoPagoID`, `pais_id`) deben seleccionarse visualmente mediante componentes `<select>`, `ListBox` o Dropdowns.
- Los Listbox se pueblan consumiendo los endpoints `GET` de la capa de información (`/info`).

---

## 3. Capa de Autenticación (`/auth`)

### 3.1. Login de Usuario / Empleado
- **Endpoint**: `POST /auth/login`
- **Request Body**:
```json
{
  "usuario": "arturo_123",
  "psswd": "mi_password_segura"
}
```
- **Respuesta Exitosa (`200 OK`)**:
```json
{
  "message": "Inicio de sesión exitoso",
  "usuario": {
    "usuario_id": 5,
    "usuario": "arturo_123",
    "tipo_cuenta": "Usuario",
    "rol_id": null,
    "pedido_id": 14
  }
}
```

---

### 3.2. Cerrar Sesión (Logout)
- **Endpoint**: `POST /auth/logout`
- **Respuesta (`200 OK`)**:
```json
{
  "message": "Sesión cerrada exitosamente"
}
```
*Acción React*: Limpiar estado local y resetear `pedido_id` a `null`.

---

### 3.3. Solicitar Registro de Cliente (Paso 1 - OTP Correo)
- **Endpoint**: `POST /auth/solicitud-usuario`
- *Nota UI*: `pais_id` se selecciona con Listbox poblado desde `GET /info/paises`.
- **Request Body**:
```json
{
  "nombres": "Juan",
  "apellidos": "Pérez",
  "fecha_nacimiento": "1998-05-15",
  "correo": "juan.perez@example.com",
  "pais_id": 1,
  "usuario": "juanp98",
  "password": "Password123!",
  "telefono": "55554444"
}
```

---

### 3.4. Confirmar Registro con Código Verificador (Paso 2 - OTP)
- **Endpoint**: `POST /auth/confirmar-registro`
- **Request Body**:
```json
{
  "usuario": "juanp98",
  "codigo": "A1B2C3"
}
```

---

### 3.5. Registrar Empleado (Exclusivo Administradores)
- **Endpoint**: `POST /auth/registrar-empleado` (Requiere sesión de empleado Admin)
- **Request Body**:
```json
{
  "rol_id": 2,
  "codigo_empleado": "EMP-005",
  "nombres": "Carlos",
  "apellidos": "Gómez",
  "cui": "1234567890101",
  "correo": "carlos.gomez@empresa.com",
  "usuario": "cgomez",
  "password": "EmpleadoPassword123!",
  "telefono": "44332211"
}
```

---

### 3.6. Consultar Estado de Sesión Actual
- **Endpoint**: `GET /auth/me`
- Devuelve la información básica guardada en la cookie para verificar sesión activa.

---

## 4. Capa de Información (`/info`)

### 4.1. Endpoints GET para Poblar Formularios y Listbox
| Endpoint | Descripción | Objeto de Retorno |
| :--- | :--- | :--- |
| `GET /info/paises` | Listado de países | `[{ "ID": 1, "Nombre": "Guatemala" }]` |
| `GET /info/plataformas` | Listado de plataformas | `[{ "ID": 1, "Nombre": "PC", "Fabricante": "Microsoft" }]` |
| `GET /info/regiones` | Listado de regiones | `[{ "id": 1, "nombre": "GLOBAL" }]` |
| `GET /info/clasificaciones` | Listado de clasificaciones ESRB | `[{ "ID": 1, "Codigo": "T", "EdadMinima": 13, "Descripcion": "Teen" }]` |
| `GET /info/tarifas` | Listado de tarifas | `[{ "ID": 1, "PrecioVenta": 59.99, "PrecioRenta": 9.99, "DuracionRentaHoras": 48 }]` |
| `GET /info/descuentos` | Listado de descuentos | `[{ "ID": 1, "Tipo": "PORCENTAJE", "Valor": 10.0, "FechaInicio": "...", "FechaFin": "..." }]` |
| `GET /info/generos` | Listado de géneros | `[{ "ID": 1, "Nombre": "Acción", "Descripcion": "..." }]` |
| `GET /info/desarrolladoras` | Listado de desarrolladoras | `[{ "id": 1, "nombre": "Ubisoft", "sitio_web": "..." }]` |
| `GET /info/metodospago` | Listado de métodos de pago | `[{ "ID": 1, "Nombre": "Tarjeta de Crédito", "Instrucciones": "..." }]` |
| `GET /info/devoluciones` | Listado de solicitudes de devolución | `[{ "ID": 1, "PedidoItemID": 20, "Estado": "PENDIENTE", ... }]` |

---

### 4.2. Obtener Ítems del Pedido Activo (Carrito de Compras)
- **Endpoint**: `GET /info/pedido-items` (Requiere autenticación)
- **Uso**: Poblar la vista del Carrito de Compras sin necesidad de enviar el `PedidoID` en los parámetros.
- **Respuesta (`200 OK`)**:
```json
{
  "PedidoID": 14,
  "Subtotal": 120.00,
  "DescuentoTotal": 15.00,
  "Total": 105.00,
  "Items": [
    {
      "PedidoItemID": 20,
      "PedidoID": 14,
      "ProductoID": 1,
      "TipoItem": "VENTA",
      "PrecioAplicado": 60.00,
      "DescuentoAplicado": 10.00,
      "Subtotal": 50.00,
      "VideojuegoID": 18,
      "VideojuegoTitulo": "Nebula Horizon",
      "SKU": "NEBULA-PC-LATAM",
      "CodigoLicencia": "PROD-KEY-001",
      "PortadaURL": "https://res.cloudinary.com/..."
    }
  ]
}
```

---

## 5. Capa de Inventario (`/inv`)

### 5.1. Listar Catálogo Completo de Videojuegos
- **Endpoint**: `GET /inv/videojuegos`
- Retorna el listado masivo para tarjetas de productos en la tienda.

---

### 5.2. Buscar Videojuego por ID
- **Endpoint**: `POST /inv/buscar-videojuego`
- **Request Body**: `{"id": 18}`

---

### 5.3. Crear Videojuego
- **Endpoint**: `POST /inv/crear-videojuego`
- **Formato**: `FormData` (`multipart/form-data`)
- **Campos a enviar desde React**:
  - `plataforma_id` (de Select `/info/plataformas`)
  - `clasificacion_id` (de Select `/info/clasificaciones`)
  - `region_id` (de Select `/info/regiones`)
  - `tarifa_id` (de Select `/info/tarifas`)
  - `descuento_id` (Opcional, por defecto `1` "Sin Descuento")
  - `titulo` (Texto)
  - `descripcion` (Texto)
  - `fecha_lanzamiento` (Fecha YYYY-MM-DD)
  - `num_jugadores` (Número)
  - `edicion` (Texto)
  - `genero_id` (de Select `/info/generos`)
  - `desarrolladora_id` (de Select `/info/desarrolladoras`)
  - `file` (File desde `<input type="file" />`)

---

## 6. Capa Financiera (`/financiero`)

### 6.1. Crear Descuento
- **Endpoint**: `POST /financiero/crear-descuento`
- *Nota UI*: Poner un control de radio botones o selector con las opciones `"PORCENTAJE"` o `"MONTO_FIJO"`.
- **Request Body**:
```json
{
  "Tipo": "PORCENTAJE",
  "Valor": 15.00,
  "FechaInicio": "2026-10-01T00:00:00",
  "FechaFin": "2026-10-31T23:59:59"
}
```

---

### 6.2. Crear Cupón Promocional
- **Endpoint**: `POST /financiero/crear-cupon`
- *Nota UI*: Poner radio botones para la opción `Tipo` (`"PORCENTAJE"` o `"MONTO_FIJO"`).
- **Request Body**:
```json
{
  "Codigo": "OFERTA2026",
  "Tipo": "MONTO_FIJO",
  "Valor": 30.00,
  "FechaExpiracion": "2026-12-31T23:59:59"
}
```

---

### 6.3. Asignar Descuento a un Videojuego
- **Endpoint**: `POST /financiero/asignar-descuento`
- *Nota UI*: Renderizar un Listbox de videojuegos y un Listbox con descuentos cargado desde `GET /info/descuentos`.
- **Request Body**:
```json
{
  "VideojuegoID": 18,
  "DescuentoID": 3
}
```

---

## 7. Capa Comercial (`/comercial`)

### 7.1. Crear Pedido Inicial
- **Endpoint**: `POST /comercial/crear-pedido` (Requiere autenticación)

---

### 7.2. Agregar Ítem al Pedido
- **Endpoint**: `POST /comercial/agregar-item-pedido`
- **Request Body**:
```json
{
  "VideojuegoID": 18,
  "TipoItem": "VENTA"
}
```
- **Respuesta (`201 Created`)**:
```json
{
  "PedidoID": 14,
  "ProductoID": 12,
  "PedidoItemID": 25,
  "SKU": "NEBULA-PC-LATAM-002",
  "CodigoLicencia": "PROD-KEY-025"
}
```
*Acción React*: Actualizar el `pedido_id` en cache con el `PedidoID` devuelto.

---

### 7.3. Aplicar Cupón de Descuento
- **Endpoint**: `POST /comercial/aplicar-cupon`
- **Request Body**:
```json
{
  "Codigo": "OFERTA2026"
}
```

---

### 7.4. Procesar Pago y Generar Factura
- **Endpoint**: `POST /comercial/procesar-pago`
- *Nota UI*: `MetodoPagoID` se selecciona con el Listbox poblado desde `GET /info/metodospago`.
- **Request Body**:
```json
{
  "MetodoPagoID": 1,
  "NITCliente": "1234567-8",
  "NombreCliente": "Arturo Pérez"
}
```
- **Respuesta (`201 Created`)**:
```json
{
  "TransaccionID": 8,
  "FacturaID": 8,
  "NumeroFactura": "FAC-20260922173000-A1B2C3",
  "PDFUrl": "https://res.cloudinary.com/...",
  "MontoTotal": 70.00
}
```
*Acción React*:
1. Renderizar o redirigir a la imagen de factura enviada en `PDFUrl`.
2. Resetear el cache local de `pedido_id` a `null`.

---

### 7.5. Gestionar Pedido (Exclusivo Empleados / Administradores)
- **Endpoint**: `POST /comercial/gestionar-pedido`
- **Ejemplo Acción REVISAR**:
```json
{
  "Accion": "REVISAR",
  "PedidoID": 14,
  "EmpleadoID": 2,
  "Aprobar": true,
  "Observacion": "Pedido verificado correctamente"
}
```
- **Ejemplo Acción COMPLETAR**:
```json
{
  "Accion": "COMPLETAR",
  "PedidoID": 14
}
```
