from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Fornitore
from .forms import FornitoreForm
class FornitoreListView(LoginRequiredMixin, ListView):
    model = Fornitore
    template_name = "anagrafiche/fornitore_list.html"
    context_object_name = "fornitori"

from .forms import FornitoreForm

class FornitoreCreateView(LoginRequiredMixin, CreateView):
    model = Fornitore
    form_class = FornitoreForm
    template_name = "anagrafiche/fornitore_form.html"
    success_url = reverse_lazy("anagrafiche:fornitore_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class FornitoreUpdateView(LoginRequiredMixin, UpdateView):
    model = Fornitore
    form_class = FornitoreForm
    template_name = "anagrafiche/fornitore_form.html"
    success_url = reverse_lazy("anagrafiche:fornitore_list")

class FornitoreDeleteView(LoginRequiredMixin, DeleteView):
    model = Fornitore
    template_name = "anagrafiche/fornitore_confirm_delete.html"
    success_url = reverse_lazy("anagrafiche:fornitore_list")

