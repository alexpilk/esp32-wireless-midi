from . import views


route_handlers = [
    ('/note/<slot>', 'GET', views.get_note),
    ('/note/<slot>', 'POST', views.set_note),
    ('/', 'GET', views.home),
    ('/bootstrapcreative.js', 'GET', views.js),
    ('/bootstrap.min.css', 'GET', views.css)
]
