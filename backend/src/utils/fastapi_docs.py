from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.responses import HTMLResponse

SWAGGER_JS_URL = "https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"
SWAGGER_CSS_URL = "https://unpkg.com/swagger-ui-dist@5/swagger-ui.css"
REDOC_JS_URL = "https://unpkg.com/redoc@next/bundles/redoc.standalone.js"


def add_custom_docs_endpoints(app: FastAPI) -> None:
    """Add rewritten docs endpoints with another url of static files (JS, CSS for Swagger and Redoc).

    :param app: FastAPI-application
    :return: None
    """

    @app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html() -> HTMLResponse:
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=app.title + " - Swagger UI",
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url=SWAGGER_JS_URL,
            swagger_css_url=SWAGGER_CSS_URL,
        )

    @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
    async def swagger_ui_redirect() -> HTMLResponse:
        return get_swagger_ui_oauth2_redirect_html()

    @app.get("/redoc", include_in_schema=False)
    async def redoc_html() -> HTMLResponse:
        return get_redoc_html(
            openapi_url=app.openapi_url,
            title=app.title + " - ReDoc",
            redoc_js_url=REDOC_JS_URL,
        )
