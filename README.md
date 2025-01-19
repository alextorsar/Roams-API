# Chatbot API

Este repositorio contiene una API desarrollada con **FastAPI** para manejar un chatbot conversacional. La API permite la autenticación de usuarios, la gestión de conversaciones y mensajes, y la integración con un modelo de lenguaje preentrenado de Hugging Face.

## Características principales
- Autenticación con tokens JWT.
- Creación y gestión de conversaciones.
- Generación de respuestas automáticas utilizando modelos avanzados de lenguaje.
- Sistema de logging para rastrear solicitudes y respuestas.

---

## Instrucciones de instalación

### Prerrequisitos
- Python 3.8 o superior.
- Git instalado en tu sistema.

### Pasos para la instalación

1. **Clonar el repositorio:**
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

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar las variables de entorno:**
   Crea un archivo `.env` en el directorio principal con el siguiente contenido:
   ```env
   SECRET_KEY="your_secret_key"
   ALGORITHM="HS256"
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   DATABASE_URL="sqlite:///./app.db"
   MODEL_NAME="mistralai/Mistral-7B-Instruct-v0.2"
   HUGGINGFACEHUB_API_TOKEN="your_huggingface_api_key"
   ```

---

## Ejecución de la API

1. **Iniciar el servidor:**
   ```bash
   uvicorn main:app --reload
   ```

2. **Acceder a la documentación interactiva:**
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
- **Cuerpo de la solicitud:**
  ```json
  {
      "username": "alex@gmail.com",
      "password": "password123"
  }
  ```
- **Respuesta de ejemplo:**
  ```json
  {
      "access_token": "<JWT_TOKEN>",
      "token_type": "bearer"
  }
  ```

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

---

## Notas adicionales

- **Compatibilidad:** Este proyecto ha sido probado en Python 3.10 y FastAPI 0.95.0.
- **Contribuciones:** Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request en este repositorio.

---

## Licencia

Este proyecto está licenciado bajo los términos de la licencia MIT. Consulta el archivo `LICENSE` para más detalles.
