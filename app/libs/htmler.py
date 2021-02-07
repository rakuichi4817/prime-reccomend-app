from flask import Markup, Blueprint


app = Blueprint("htmler", __name__)

@app.template_filter('cr')
def cr(arg):
    return Markup(arg.replace('\r', '<br>'))
