from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Cheese
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db import models
from django.views.generic import FormView
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    
)

class CheeseListView(ListView):
    model = Cheese

class CheeseDetailView(DetailView):
    model = Cheese


class CheeseCreateView(LoginRequiredMixin, CreateView):
    model = Cheese
    fields = [
    'name',
    'description',
    'firmness',
    'country_of_origin',]

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)
    
class CheeseUpdateView(LoginRequiredMixin, UpdateView):
    model = Cheese
    fields = [
        'name',
        'description',
        'firmness',
        'country_of_origin',
        ]
    action = "Update"

class CheeseDeleteView(LoginRequiredMixin, DeleteView):
    model = Cheese
    
    # This works. Next try django loader for getting the .HTML page
    template_name = '../templates/cheeses/cheese_confirm_delete.html'

    success_url=reverse_lazy("cheeses:list")

class CheeseRatingView(LoginRequiredMixin, FormView):
    model = Cheese
    


