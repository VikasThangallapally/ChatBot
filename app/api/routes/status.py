from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/status", summary="Service status and registered routes")
async def service_status(request: Request):
    """Return basic service status and the list of OpenAPI paths.

    Useful for debugging deployed routing issues (e.g., missing /api/register).
    """
    app = request.app
    try:
        openapi = app.openapi()
        paths = sorted(list(openapi.get("paths", {}).keys()))
    except Exception:
        paths = []

    return {
        "status": "ok",
        "title": app.title if hasattr(app, "title") else None,
        "version": app.version if hasattr(app, "version") else None,
        "paths": paths,
    }
