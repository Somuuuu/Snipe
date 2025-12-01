from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from src.routes.task_route import router as task_router
from src.routes.auth_route import router as auth_router
from src.config.db import db

app = FastAPI()

app.include_router(task_router)
app.include_router(auth_router)

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    # Fetch shipments from Supabase and pass them to the template as `table`
    result = db.table("snipe").select("*").execute()
    table = result.data if hasattr(result, 'data') else result
    # compute overview counts
    total = len(table) if table else 0
    in_transit = sum(1 for t in table if (t.get('status') if isinstance(t, dict) else getattr(t, 'status', None)) == 'In Transit') if table else 0
    delivered = sum(1 for t in table if (t.get('status') if isinstance(t, dict) else getattr(t, 'status', None)) == 'Delivered') if table else 0
    delayed = sum(1 for t in table if (t.get('status') if isinstance(t, dict) else getattr(t, 'status', None)) == 'Delayed') if table else 0

    return templates.TemplateResponse("login.html", {"request": request, "table": table, "total": total, "in_transit": in_transit, "delivered": delivered, "delayed": delayed})