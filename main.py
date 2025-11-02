import air
from fastapi import Depends, HTTPException

app = air.Air()
app.add_middleware(air.SessionMiddleware, secret_key="change-me")

# --- Dependency ---
def require_login(request: air.Request):
    # Replace this with your actual login check
    user = request.session.get("user") if hasattr(request, "session") else None  

    if not user:
        # Redirect if not logged in
        raise HTTPException(
            status_code=307,
            headers={"Location": "/login"},
        )
    return user

# --- Routes ---
@app.page
async def index(request: air.Request):
    return air.layouts.mvpcss(
        air.H1('Landing page'),
        air.P(air.A('Dashboard', href='/dashboard'))
    )    

@app.page
async def login():
    return air.layouts.mvpcss(
        air.H1('Login'),
        # login the user
        air.Form(
            air.Label("Name:", for_="username"),
            air.Input(type="text", name="username", id="username", required=True, autofocus=True),
            air.Label("Password:", for_="password"),
            air.Input(type="password", name="password", id="password", required=True, autofocus=True),            
            air.Button("Login", type="submit"),
            action="/login",
            method="post",
        )    
    )


@app.page
async def dashboard(request: air.Request, user=Depends(require_login)):
    return air.layouts.mvpcss(
        air.H1(f"Dashboard for {request.session['user']['username']}"),
        air.P(air.A('Logout', href='/logout'))
    )

@app.post('/login')
async def login(request: air.Request):
    form = await request.form()
    request.session['user'] = dict(username=form.get('username'))
    return air.RedirectResponse('/dashboard', status_code=303)

@app.page
async def logout(request: air.Request):
    request.session.pop('user')
    return air.RedirectResponse('/', status_code=303)
