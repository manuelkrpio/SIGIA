# -*- encoding: utf-8 -*-

from django.views.generic import ListView 
from django.views.generic.detail import DetailView 
from .models import Vehiculo 
from .models import SucursalVehiculo
from apps.sucursal.models import Sucursal

class ListaVehiculosSucursal(ListView): 
	"""Lista los vehiculos por sucursal."""
	
	model = Vehiculo
	context_object_name = 'lista_vehiculos'
	template_name = 'vehiculo/vehiculo_list.html'

	def get_queryset(self):
		'''Permite filtrar los vehiculos que seran mostrados.

		Dada la pk de la sucursal se sobre escribe el metodo
		para que se listen los vehiculos que pertenecen a una
		sucursal dada.

		'''
		sucursal_id = self.kwargs['pk']
		sucursal = Sucursal.objects.get(id=sucursal_id)
		vehiculos = sucursal.vehiculo_set.all()
		return vehiculos

	def get_context_data(self,**kwargs):
		"""Perime agregar al contexto la sucursal a la cual pertenecen los vehiculos listados
		en el query_set."""

		context = super(ListaVehiculosSucursal,self).get_context_data(**kwargs)
		sucursal_id = self.kwargs['pk']
		sucursal = Sucursal.objects.get(id=sucursal_id)
		context['sucursal'] = sucursal
		return context


class ParcialListaVehiculosSucursal(ListView): 
	"""Lista los vehiculos por sucursal."""
	
	model = Vehiculo
	context_object_name = 'lista_vehiculos'
	template_name = 'vehiculo/parciales/vehiculo_list.html'

	def get_queryset(self):
		'''Permite filtrar los vehiculos que seran mostrados.

		Dada la pk de la sucursal se sobre escribe el metodo
		para que se listen los vehiculos que pertenecen a una
		sucursal dada.

		'''
		sucursal_id = self.kwargs['pk']
		sucursal = Sucursal.objects.get(id=sucursal_id)
		vehiculos = sucursal.vehiculo_set.all()
		return vehiculos

	def get_context_data(self,**kwargs):
		"""Perime agregar al contexto la sucursal a la cual pertenecen los vehiculos listados
		en el query_set."""
		
		context = super(ParcialListaVehiculosSucursal,self).get_context_data(**kwargs)
		sucursal_id = self.kwargs['pk']
		sucursal = Sucursal.objects.get(id=sucursal_id)
		context['sucursal'] = sucursal
		return context

