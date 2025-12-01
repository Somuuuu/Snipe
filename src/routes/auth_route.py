from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from src.config.db import db

router = APIRouter()

templates = Jinja2Templates(directory = "templates")
@router.get('/login')
def login_page(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})


@router.get('/logout')
def logout(request: Request):
    # Simple logout: redirect to login page. If you later implement sessions, clear them here.
    return RedirectResponse(url='/login')


@router.post('/login')
def login(request: Request, email: str = Form(...), password: str = Form(...)):
    # simple sign-in flow using the Supabase client
    if not (email and password):
        return templates.TemplateResponse("login.html", {'request': request, 'error': 'Email and password required'})

    try:
        result = db.auth.sign_in_with_password({
            'email': email,
            'password': password
        })
    except Exception as e:
        msg = str(e)
        # detect common Supabase error text for unconfirmed emails
        if 'Email not confirmed' in msg or 'email not confirmed' in msg:
            # User requested a simple login without security checks — treat as successful
            res = db.table("snipe").select("*").execute()
            table = res.data if hasattr(res, 'data') else res
            return templates.TemplateResponse("index.html", {'request': request, 'table': table, 'message': 'Signed in (email not confirmed) - bypassed confirmation as requested'})
        return templates.TemplateResponse("login.html", {'request': request, 'error': f'Sign in failed: {msg}'})

    # Determine success based on common response shapes from supabase clients
    success = False
    if isinstance(result, dict):
        data = result.get('data') or {}
        # data may contain 'session' or 'user'
        if data and (data.get('session') or data.get('user')):
            success = True
    else:
        # object-like responses may have attributes
        data = getattr(result, 'data', None) or getattr(result, 'user', None)
        if data:
            success = True

    if success:
        # fetch shipments to render dashboard
        res = db.table("snipe").select("*").execute()
        table = res.data if hasattr(res, 'data') else res
        return templates.TemplateResponse("index.html", {'request': request, 'table': table, 'message': 'Sign in successful'})

    # otherwise render login with an error message (attempt to show returned payload)
    err_msg = ''
    if isinstance(result, dict):
        err_msg = result.get('error') or result.get('message') or str(result)
    else:
        err_msg = str(result)

    return templates.TemplateResponse("login.html", {'request': request, 'error': f"Sign in failed: {err_msg}"})