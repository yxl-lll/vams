
from fastapi.responses import RedirectResponse
from fastapi import Request
def h5config(app):
    
    @app.middleware("http")
    async def add_request_id_header(request: Request, call_next):
        response = await call_next(request)
        if response.status_code == 401 and request.base_url.path != '/login':
            return RedirectResponse('/login')
        return response

