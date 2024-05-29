from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("graph/", views.create_graph, name='graph'),
    path('graph_view/', views.graph_view, name='graphview'),
]
