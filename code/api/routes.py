from . import views


route_handlers = [
    ('/note/<slot>', 'GET', views.get_note),
    ('/note/<slot>', 'POST', views.set_note),
    ('/notes/', 'GET', views.get_notes),
    ('/notes/', 'POST', views.set_notes),
    ('/', 'GET', views.home),
    ('/bootstrapcreative.js', 'GET', views.js),
    ('/bootstrap.min.css', 'GET', views.css)
]
