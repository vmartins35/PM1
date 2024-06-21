from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from starlette.responses import RedirectResponse, JSONResponse

from controller.task_controller import task_router

app = FastAPI(
    title="Task API",
    description="Tarefas",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url=None,
    redoc_url=None,
    contact={
        "name": "Vinicius Santos",
        "email": "vmartins3577@gmail.com",
        "url": "https://www.linkedin.com/in/vinicius-martins-it/"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    },
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Development server"
        },
    ],
)

app.include_router(task_router)


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": str(exc.detail)}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred"}
    )


@app.get("/", tags=["Redirect"], include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")


@app.get("/docs", tags=["Redirect"], include_in_schema=False)
async def get_swagger_ui():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Swagger UI"
    )


@app.get("/openapi.json", tags=["Redirect"], include_in_schema=False)
async def get_openapi():
    return get_swagger_ui(
        title="Tasks API",
        version="1.0.0",
        description="Tarefas",
        routes=app.routes,
    )

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
