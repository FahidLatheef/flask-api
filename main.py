from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse

from routers import cardholder, customer, offer

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.include_router(offer.router)
app.include_router(cardholder.router)
app.include_router(customer.router)

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("home.html", context={'request': request})

@app.route('/home')
def home(request: Request):
    return RedirectResponse(url='/')
