from django.urls import path
from . import views
from .reports import dichiarazione_intento


app_name = "documenti"

urlpatterns = [
    path(
        "dichiarazioni/",
        views.DichiarazioneListView.as_view(),
        name="dichiarazione_list",
    ),
    path(
        "dichiarazioni/nuova/",
        views.DichiarazioneIntentoCreateView.as_view(),
        name="dichiarazione_create",
    ),
    path(
        "dichiarazioni/<int:pk>/modifica/",
        views.DichiarazioneIntentoUpdateView.as_view(),
        name="dichiarazione_update",
    ),
    path(
        "dichiarazioni/<int:pk>/elimina/",
        views.DichiarazioneDeleteView.as_view(),
        name="dichiarazione_delete",
    ),
    path("fatture/", views.FatturaListView.as_view(), name="fattura_list"),
    path("fatture/nuova/", views.FatturaCreateView.as_view(), name="fattura_create"),
    path("fattura/check/", views.fattura_check, name="fattura_check"),
    path(
        "fatture/<int:pk>/modifica/",
        views.FatturaUpdateView.as_view(),
        name="fattura_update",
    ),
    path(
        "fatture/<int:pk>/elimina/",
        views.FatturaDeleteView.as_view(),
        name="fattura_delete",
    ),
    path("report/plafond/", views.ReportPlafondView.as_view(), name="report_plafond"),
    path(
        "dichiarazione/<int:pk>/stampa",
        dichiarazione_intento,
        name="dichiarazione_intento",
    ),
    path("durc/", views.DurcListView.as_view(), name="durc_list"),
    path("durc/nuovo/", views.DurcCreateView.as_view(), name="durc_create"),
    path("durc/<int:pk>/modifica/", views.DurcUpdateView.as_view(), name="durc_update"),
    path("durc/<int:pk>/elimina/", views.DurcDeleteView.as_view(), name="durc_delete"),
]
