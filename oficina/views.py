from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Oficina  # Assuming Persona is defined in the same app
from persona.models import Persona  # Importa el modelo Persona
from django.db.models import Q 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator


# Create your views here.
class OficinaListView(ListView):
    model = Oficina
    template_name = 'oficina/lista.html'
    context_object_name = 'oficinas'
    paginate_by = 4  
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['home_url'] = 'oficina:lista'
        context['titulo'] = 'Lista de Oficinas'
        context['search_action'] = 'oficina:buscar'
        return context

class OficinaSearchView(ListView):
    model = Oficina
    template_name = 'oficina/buscar.html'
    context_object_name = 'oficinas'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Oficina.objects.filter(
                Q(nombre__icontains=query)     
            ).distinct()
        return Oficina.objects.all().distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Busqueda de Oficinas"
        context['home_url'] = 'oficina:lista'
        context['search_query'] = self.request.GET.get('q', '')
        return context

class OficinaDetailView(DetailView):
    model = Oficina
    template_name = 'oficina/detalle.html'
    context_object_name = 'oficina'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        oficina = self.get_object()
        context['titulo'] = 'Detalle de Oficina'
        context['cantidad_empleados'] = oficina.personas.count()  # type: ignore # Suma empleados relacionados
        return context

class OficinaEmpleadoListView(ListView):
    model = Persona
    template_name = 'oficina/empleados.html'
    context_object_name = 'empleados'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        oficina = Oficina.objects.get(pk=self.kwargs['pk'])
        context['oficina'] = oficina
        context['titulo'] = 'Empleados de la Oficina'
        context['cantidad_empleados'] = oficina.personas.count()  # type: ignore # personas relacionadas
        context['empleados'] = oficina.personas.all() # type: ignore
        context['home_url'] = 'oficina:lista'
        return context

class OficinaCreateView(LoginRequiredMixin, CreateView):
    model = Oficina
    template_name = 'oficina/crear.html'
    fields = ['nombre','nombre_corto']
    success_url = reverse_lazy('oficina:lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Oficina'
        return context
    
class OficinaUpdateView(LoginRequiredMixin, UpdateView):
    model = Oficina
    template_name = 'oficina/crear.html'
    fields = ['nombre','nombre_corto']
    success_url = reverse_lazy('oficina:lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Oficina'
        return context

class OficinaDeleteView(LoginRequiredMixin, DeleteView):
    model = Oficina
    template_name = 'oficina/eliminar.html'
    success_url = reverse_lazy('oficina:lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Oficina'
        context['confirm_message'] = "¿Estás seguro de que quieres eliminar esta oficina?"  
        context['cancel_url'] = reverse_lazy('oficina:lista')
        return context
    
    def lista_personas(request):
        personas = Persona.objects.all().order_by('apellido')
        paginator = Paginator(personas, 10)  # 10 por página
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'persona/lista.html', {'page_obj': page_obj})