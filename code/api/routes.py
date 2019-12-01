from . import views


route_handlers = [
    ('/notes/', 'GET', views.get_notes),
    ('/notes/', 'POST', views.set_notes)
]
