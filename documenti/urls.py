from django.urls import path
from . import views
from .reports import dichiarazione_intento
from .provareport import genera_report


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
        "documenti/dichiarazione/<int:pk>/stampa/",
        dichiarazione_intento,
        name="dichiarazione_intento",
    ),
    path('genera_report/<int:pk>/', genera_report, name='genera_report'),
]
