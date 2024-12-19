from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.exception_handlers import http_exception_handler
from starlette.exceptions import HTTPException as StarletteHTTPException


def add_single_page_application_endpoints(application: FastAPI, static_dir: str) -> FastAPI:

    @application.exception_handler(StarletteHTTPException)
    async def _spa_server(req: Request, exc: StarletteHTTPException):
        if exc.status_code == 404 and "api" not in req.url.path:
            return FileResponse(f'{static_dir}/index.html', media_type='text/html')
        else:
            return await http_exception_handler(req, exc)

    @application.get("/favicon.ico")
    def get_favicon():
        return FileResponse(f'{static_dir}/favicon.ico', media_type='image/x-icon')

    application.mount(
        '/assets/',
        StaticFiles(directory=f'{static_dir}/assets'),
        name='React app static files',
    )
    return application
