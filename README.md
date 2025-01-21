# Chatbot API

Este repositorio contiene una API desarrollada con **FastAPI** para manejar un chatbot conversacional. La API permite la autenticación de usuarios, la gestión de conversaciones y mensajes, y la integración con un modelo de lenguaje preentrenado de Hugging Face.

## Características principales
- Autenticación con tokens JWT.
- Creación y gestión de conversaciones.
- Generación de respuestas automáticas utilizando modelos avanzados de lenguaje.
- Sistema de logging para rastrear solicitudes y respuestas que se puede observar en app.log.

---

## Instrucciones de instalación

### Prerrequisitos
- Python 3.8 o superior (Se recomienda una versión estable como Python 3.10 o 3.11, ya que para las versiones más recientes como Python 3.13 muchas librerías aún no tienen soporte, nosotros hemos utilizado Python 3.11.9).
- Git instalado en tu sistema.

### Pasos para la instalación

1. **Clonar el repositorio: (Por evitar conflictos con los permisos, si se trabaja desde Windows se recomienda clonar el repositorio en una carpeta local, que no esté sincronizada con OneDrive)**
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd <NOMBRE_DEL_REPOSITORIO>
   ```

2. **Crear un entorno virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate    # Windows
   ```

3. **Instalar dependencias: (Para evitar problemas de permisos se recomienda instalarlas con permisos de administrador)**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configurar las variables de entorno:**
   Crea un archivo `.env` en el directorio principal con el siguiente contenido:
   ```env
   SECRET_KEY="your_secret_key"
   ALGORITHM="HS256"
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   DATABASE_URL="sqlite:///./app.db"
   ENDPOINT_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
   HUGGINGFACEHUB_API_TOKEN="your_huggingface_api_key"
   ```
6. **Inicializar la base de datos:**
   Ejecuta el siguiente comando desde la carpeta raíz del proyecto para crear la base de datos SQLite utilizando las configuraciones definidas:
   ```bash
   python -m database.init_db
---

## Ejecución de la API

1. **Iniciar el servidor:**
   Desde la carpeta raíz Roams-API
   ```bash
   uvicorn main:app --reload
   ```

3. **Acceder a la documentación interactiva:**
   - Documentación Swagger: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - Documentación Redoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## Ejemplos de solicitudes a la API

### 1. **Registro de usuario**
- **Endpoint:** `POST /auth/register/`
- **Cuerpo de la solicitud:**
  ```json
  {
      "name": "Alex",
      "email": "alex@gmail.com",
      "password": "password123"
  }
  ```
- **Respuesta de ejemplo:**
  ```json
  {
      "id": 1,
      "name": "Alex",
      "email": "alex@gmail.com"
  }
  ```

### 2. **Inicio de sesión**
- **Endpoint:** `POST /auth/login/`
- **Cuerpo de la solicitud:** Debe enviarse en formato `x-www-form-urlencoded`

  - **Campos:**
    - `username`: El correo electrónico del usuario.
    - `password`: La contraseña del usuario.

- **Respuesta de ejemplo:**
  ```json
  {
      "access_token": "<JWT_TOKEN>",
      "token_type": "bearer"
  }
### 3. **Crear una conversación**
- **Endpoint:** `POST /conversation/`
- **Encabezado:**
  ```json
  {
      "Authorization": "Bearer <JWT_TOKEN>"
  }
  ```
- **Cuerpo de la solicitud:**
  ```json
  {
      "title": "ML in Sports"
  }
  ```
- **Respuesta de ejemplo:**
  ```json
  {
      "id": 1,
      "title": "ML in Sports",
      "initial_timestamp": "2025-01-20T00:00:00",
      "last_update": "2025-01-20T00:00:00"
  }
  ```
### 4. **Enviar un mensaje en una conversación**
- **Endpoint:** `POST /message/conversation/{conversation_id}`
- **Encabezado:**
  ```json
  {
      "Authorization": "Bearer <JWT_TOKEN>"
  }
  ```
- **Cuerpo de la solicitud:**
  ```json
  {
      "user_message": "Tell me more about ML in football."
  }
  ```
- **Respuesta de ejemplo:**
  ```json
  {
      "id": 1,
      "user_message": "Tell me more about ML in football.",
      "assistant_answer": "Machine Learning in football is used for player analysis, team strategies, etc.",
      "created_at": "2025-01-20T00:01:00",
      "answered_at": "2025-01-20T00:01:01"
  }
  ```
### 5. **Listar todas las conversaciones de un usuario**
- **Endpoint:** `GET /conversation/`
- **Encabezado:**
  ```json
  {
      "Authorization": "Bearer <JWT_TOKEN>"
  }
  ```
- **Respuesta de ejemplo:**
  ```json
  [
      {
          "id": 1,
          "title": "The most popular sports",
          "initial_timestamp": "2025-01-20T00:09:28.824456",
          "last_update": "2025-01-20T01:09:48.541974"
      },
      {
          "id": 2,
          "title": "The use of AI in Medicine",
          "initial_timestamp": "2025-01-20T00:10:28.902090",
          "last_update": "2025-01-20T00:10:28.902090"
      }
  ]
  ```
### 6. **Listar los mensajes de una conversación**
- **Endpoint:** `GET /message/conversation/{conversation_id}`
- **Encabezado:**
  ```json
  {
      "Authorization": "Bearer <JWT_TOKEN>"
  }
- **Respuesta de ejemplo:**
  ```json
  [
      {
        "id": 1,
        "user_message": "Which are the most popular sports?",
        "assistant_answer": "\n        The most popular sports globally vary, but some consistently rank high. Soccer (Football), Cricket, Basketball, American Football, and Tennis are among the top sports with large followings worldwide.",
        "created_at": "2025-01-20T01:09:48.191907",
        "answered_at": "2025-01-20T01:09:48.541974"
    },
    {
        "id": 2,
        "user_message": "Wow, cricket, very surprising, I thought that almost anyone played that sport",
        "assistant_answer": "\n        Cricket indeed has a large following, particularly in countries like India, Pakistan, Australia, and England. Its popularity might be surprising to some due to its unique rules and long matches.",
        "created_at": "2025-01-20T01:23:34.346887",
        "answered_at": "2025-01-20T01:23:35.254352"
    }
  ]
 ---

## Notas adicionales

- **Compatibilidad:** Este proyecto ha sido probado en Python 3.11.9 y FastAPI 0.115.6
- **Contribuciones:** Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request en este repositorio.

---

## Licencia

Este proyecto está licenciado bajo los términos de la licencia MIT. Consulta el archivo `LICENSE` para más detalles.
