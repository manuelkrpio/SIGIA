from django.views.generic import TemplateView
from django.http import HttpResponseRedirect 
from django.core.urlresolvers import reverse_lazy
from .models import VENDEDOR, GERENTE, JEFE_TALLER

# Create your views here.
class PerfilGerente(TemplateView):
	template_name = 'cuenta/perfil_gerente.html'
	
class PerfilJefeTaller(TemplateView):
	template_name = 'cuenta/perfil_jefe_taller.html'

class PerfilVendedor(TemplateView):
	template_name = 'cuenta/perfil_vendedor.html'
	