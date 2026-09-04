from fastapi.templating import Jinja2Templates

# Mount templates externally from the config folder
templates = Jinja2Templates(directory="app/templates")
