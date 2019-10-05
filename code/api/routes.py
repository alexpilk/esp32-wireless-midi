from code.api import views


route_handlers = [
    ('/note/<slot>', 'GET', views.get_note),
    ('/note/<slot>', 'POST', views.set_note)
]
