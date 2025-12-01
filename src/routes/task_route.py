from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from src.config.db import db

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.post('/shipments/add')
def add_shipment(request: Request,
                 product_name: str = Form(...),
                 source: str = Form(...),
                 destination: str = Form(...),
                 status: str = Form(...),
                 eta: str = Form(...)):
    db.table("snipe").insert({
        "product_name": product_name,
        "source": source,
        "destination": destination,
        "status": status,
        "ddate": eta
    }).execute()
    # Redirect to dashboard so Jinja2 renders fresh data
    return RedirectResponse(url='/', status_code=303)


@router.post('/shipments/update')
def edit_shipment(request: Request,
                  shipment_id: str = Form(...),
                  status: str = Form(...),
                  log_event: str = Form(None),
                  eta: str = Form(...)):
    update_payload = {
        "status": status,
        "ddate": eta
    }
    if log_event:
        update_payload["log"] = log_event

    db.table("snipe").update(update_payload).eq("id", shipment_id).execute()
    return RedirectResponse(url='/', status_code=303)


@router.get('/shipments')
def shipment_list(request: Request):
    result = db.table("snipe").select("*").execute()
    table = result.data if hasattr(result, 'data') else result
    return templates.TemplateResponse('index.html', {"request": request, "table": table})


@router.get('/shipments/{shipment_id}')
def shipment_detail(request: Request, shipment_id: str, action: str = None):
    # fetch selected shipment and all shipments for dashboard
    res_all = db.table("snipe").select("*").execute()
    table = res_all.data if hasattr(res_all, 'data') else res_all
    res = db.table("snipe").select("*").eq("id", shipment_id).execute()
    selected = None
    if hasattr(res, 'data') and res.data:
        selected = res.data[0]
    elif isinstance(res, list) and res:
        selected = res[0]

    return templates.TemplateResponse('index.html', {"request": request, "table": table, "selected": selected, "edit": action == 'edit'})


