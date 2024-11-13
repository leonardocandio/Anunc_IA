from ddtrace import patch_all, tracer
patch_all() 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.ai_content_service.routes import router as ai_content_router
from services.auth_service.routes import router as auth_router
from services.user_service.routes import router as user_router
from services.document_service.routes import router as document_router
from services.product_service.routes import router as product_router
from dotenv import load_dotenv
import os
from mangum import Mangum  # Importar Mangum para Lambda

# Cargar las variables de entorno
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

# Configura el tracer de Datadog para FastAPI
tracer.configure(
    hostname=os.getenv("DD_AGENT_HOST", "localhost")  # Asegúrate de que apunte al Datadog Agent
)

# Crear la instancia de FastAPI
app = FastAPI(
    debug=True,
    title="Anunc IA Backend",
    description="API para gestionar el backend de Anunc IA",
    version="1.0.0"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Cambia esto a la URL de producción cuando despliegues
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Incluir el router del servicio de autenticación
app.include_router(auth_router, prefix="/auth", tags=["auth"])

# Incluir el router del servicio de contenido
app.include_router(ai_content_router, prefix="/content", tags=["ai_content"])

# Incluir el router del servicio de cuentas
app.include_router(user_router, prefix="/users", tags=["users"])

# Incluir el router del servicio de documentos
app.include_router(document_router, prefix="/documents", tags=["documents"])

# Incluir el router del servicio de documentos
app.include_router(product_router, prefix="/productos", tags=["productos"])

# Punto de entrada básico para verificar si la API está funcionando
@app.get("/")
async def root():
    return {"message": "Bienvenido a la API publicitaria"}

# Adaptador Mangum para ejecutar en AWS Lambda
handler = Mangum(app)

# Este bloque solo es necesario si deseas ejecutar la aplicación localmente con Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
