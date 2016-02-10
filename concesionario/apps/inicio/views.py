# -*- encoding: utf-8 -*-

from django.shortcuts import render, render_to_response
from django.views.generic import TemplateView
from django.contrib.auth.forms import PasswordResetForm
from django.db.models import Count, Sum
from django.core.urlresolvers import reverse
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.template import RequestContext
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout

from apps.empleado.models import Empleado, VENDEDOR, JEFE_TALLER, GERENTE
from apps.sucursal.models import SucursalVehiculo
from apps.venta.models import Venta
from apps.sucursal.models import Sucursal
from apps.factura_orden_de_trabajo.models import FacturaOrdenDeTrabajo



class Login(TemplateView):

	#Cuando la peticion es tipo GET, se muestra el template de login
	def get(self,request,*args,**kwargs):
		#Si el usuario esta autenticado, se le muestra su perfil
		if request.user.is_authenticated() and not request.user.is_staff:
			return self.get_user_template(request)
		#En caso de que no este autenticado, se le muestra el formulario de login
		else:
			return render_to_response(
				'inicio/login.html',
				context_instance=RequestContext(request))
		
	#Cunado la peticion es tipo POST se hace el proceso de login con la informacion del formulario de login
	def post(self,request,*args,**kwargs):
		username = request.POST.get('username')
		password = request.POST.get('password')

		#Usando el la funcion authenticate, obtenemos el usuario que corresponde con los datos 
		#pasados como argumentos
		user = authenticate(username=username,password=password)
		if user is not None:
			if user.is_active:
				login(request,user)
											
				#Retornamos una respuesta con el perfil del usuario
				return self.get_user_template(request)
			else:
				context = {'message':'Su usuario no esta activo'}
				return render_to_response(
					'inicio/login.html',
					context,
					context_instance=RequestContext(request))
		else:
			context = {'message':'Usuario o contraseña invalido'}
			return render_to_response(
				'inicio/login.html',
				context,
				context_instance=RequestContext(request))

	def get_user_template(self,request):
		if request.user.empleado.tipo == GERENTE:

			sucursales = Sucursal.objects.aggregate(
				valor_ventas=Sum('sucursalvehiculo__ventas__precio_venta')
				)

			print "sucursales", sucursales

			num_empleados = Empleado.objects.all().count()

			valor_ventas = Venta.dinero_acumulado(Venta)

			valor_ordenes_de_trabajo = FacturaOrdenDeTrabajo.dinero_en_facturas(FacturaOrdenDeTrabajo)

			vendedores = Empleado.objects.filter(tipo=VENDEDOR).annotate(
				num_ventas=Count('ventas')).order_by('-num_ventas')

			sucursales_vehiculos = SucursalVehiculo.objects.annotate(
				num_ventas=Count('ventas')).order_by('-num_ventas')
			
			context = {
				'sucursales':sucursales,
				'valor_ordenes_de_trabajo':valor_ordenes_de_trabajo,
				'valor_ventas':valor_ventas,
				'num_empleados':num_empleados,
				'vendedores':vendedores,
				'sucursales_vehiculos':sucursales_vehiculos
				}
			
			return render_to_response(
				'cuenta/perfil_gerente.html',
				context,
				context_instance=RequestContext(request))

		elif request.user.empleado.tipo == VENDEDOR:

			return render_to_response(
				'cuenta/perfil_vendedor.html',
				context_instance=RequestContext(request))
		
		elif request.user.empleado.tipo == JEFE_TALLER: 
		
			return render_to_response(
				'cuenta/perfil_jefe_taller.html',
				context_instance=RequestContext(request))

class Logout(TemplateView):

	def dispatch(self,request,*args,**kwargs):
		logout(request)
		context = {}
		return render_to_response('inicio/login.html',context,context_instance=RequestContext(request))


class RecuperarLogin(TemplateView):

	def dispatch(self,request,*args,**kwargs):
		return password_reset(
			request,
			template_name = 'inicio/recuperar_login_form.html',
			email_template_name = 'inicio/recuperar_login_email.html',
			subject_template_name = 'inicio/recuperar_login_email_asunto.txt',
			post_reset_redirect = reverse('inicio:recuperar_login_email_enviado'))

class RecuperarLoginEmailEnviado(TemplateView):

	def dispatch(self,request,*args,**kwargs):
		return render(request,'inicio/recuperar_login_email_enviado.html')

class RecuperarLoginConfirmacion(TemplateView):

	def dispatch(self,request,*args,**kwargs):
		
		return password_reset_confirm(
			request,
			template_name = 'inicio/recuperar_login_confirmacion.html',
			uidb64=kwargs['uidb64'], token=kwargs['token'], 
			post_reset_redirect=reverse('inicio:recuperar_login_terminado'))

class RecuperarLoginTerminado(TemplateView):

	def dispatch(self,request,*args,**kwargs):
		return render_to_response('inicio/recuperar_login_terminado.html',context_instance=RequestContext(request))