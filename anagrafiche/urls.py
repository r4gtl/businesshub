from django.urls import path
from . import views

app_name = 'anagrafiche'

urlpatterns = [
    path('fornitori/', views.FornitoreListView.as_view(), name='fornitore_list'),
    path('fornitori/nuovo/', views.FornitoreCreateView.as_view(), name='fornitore_create'),
    path('fornitori/<int:pk>/modifica/', views.FornitoreUpdateView.as_view(), name='fornitore_update'),
    path('fornitori/<int:pk>/elimina/', views.FornitoreDeleteView.as_view(), name='fornitore_delete'),
]
