
""" admin's Views """

# Django
from concurrent.futures import process
from operator import is_
from tkinter.ttk import Progressbar
from urllib import request
from django.views.generic import View,CreateView,TemplateView,DeleteView,DetailView
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.http import JsonResponse
import json
from datetime import datetime,timezone
from datetime import timedelta


from ..models import LinkInfo,ProcessSteps,ProcessStatus

class AdminHomeView(TemplateView):
	def get(self, request, **kwargs):     
		return render(request, 'admin_home.html')


class LinkGeneratorView(CreateView):
	def get(self, request, **kwargs):     
		return render(request, 'link_generator.html')
		
	def post(self, request, **kwargs):     
	
		link_name = request.POST.get('link_name')
		
		link = LinkInfo()
		link.link_name = link_name
		link.save()

		return HttpResponseRedirect(self.get_success_url(link.pk))

	def get_success_url(self,link):
		# return reverse('teachers:planifications_list', )
		return reverse("administrators:link_generator_final_step", args=[link])
		# return reverse('administrators:link_generator_final_step')


class LinkGeneratorFinalStepView(View):
	def get(self, request, **kwargs):     
		pk=self.kwargs.get('pk', None)
		context= {}
		link_info=LinkInfo.objects.get(pk=pk)
		context['link_info'] = link_info
		return render(request, 'link_generator_final_step.html',context)
	
	def post(self, request, **kwargs):	
		pk=self.kwargs.get('pk', None)

		comments = request.POST.get('comments',None)
		

		last_link = LinkInfo.objects.get(pk=pk)
		last_link.comments = comments
		last_link.attachment = request.FILES.get('file',None)
		last_link.save()
		
		steps = request.POST.getlist('steps',None)
		
		for step in steps:
			if step == "":
				print('vacio')
			else:
				process_steps = ProcessSteps()
				process_steps.step_name = step
				process_steps.link_info = last_link
				process_steps.process_status = ProcessStatus.objects.get(description__icontains="WithoutProcess")
				process_steps.save()

		# guardar lo creado en una session
		self.request.session['last_link'] = last_link.pk
		return HttpResponseRedirect(self.get_success_url())

	def get_success_url(self):
		return reverse('administrators:opened_links')


class LinkDetailView(View):
	model = ProcessSteps

	def get(self,request,**kwargs):
		context={}
		pk=self.kwargs.get('pk', None)

		processes = ProcessSteps.objects.filter(link_info=pk).order_by('pk')
		link_info=LinkInfo.objects.get(pk=pk)

		buttons = []
		for x in processes:
			print()
			buttons.append({'id':x.id,'range':range(1,int((x.hours*60)/30+1))})

		context['steps'] = processes
		context['link_info'] = link_info
		context['buttons'] = buttons

		
		print('buttons',buttons)
			
		return render(request, 'detail.html',context)

	def post(self, request, **kwargs):     
		# comment = request.POST.get('comment',None)
		print('hice post')
		process_steps= ProcessSteps.objects.get(pk=request.POST.get('step', None))
		if process_steps.is_done == False:
			process_steps.is_done=True
		else:
			process_steps.is_done=False
		process_steps.save()

		# last_link = LinkInfo.objects.last()
		# last_link.comment = comment
		# last_link.save()
		
		# steps = request.POST.getlist('steps',None)
		
		# for step in steps:
		# 	if step == "":
		# 		print('vacio')
		# 	else:
		# 		process_steps = ProcessSteps()
		# 		process_steps.step_name = step
		# 		process_steps.link_info = last_link
		# 		process_steps.save()		
		return HttpResponseRedirect(self.request.path_info)

		# return HttpResponseRedirect(self.get_success_url())

	def get_success_url(self):
		return reverse('administrators:opened_links')


class OpenedLinksView(CreateView):
	def get(self, request, **kwargs):
		context={}
		if self.verify_session() == None:
			print('no hacer nada')
		else:
			context['link'] = self.verify_session()
			del self.request.session['last_link']
		opened_links = LinkInfo.objects.all().order_by('pk')
		context['opened_links'] = opened_links
		return render(request, 'opened_links.html',context)

	def verify_session(self):	
		if 'last_link' in self.request.session:
			return self.request.session['last_link']
		else:
			return None


class LinksDeleteView(DeleteView):
	model = LinkInfo
	success_url = reverse_lazy("administrators:opened_links")


class CancelView(View):
	def get(self, request, **kwargs):
		print('cancelar')
		context={}
		pk=self.kwargs.get('pk', None)
		print('verificar',pk)
		LinkInfo.objects.get(pk=pk).delete()
		print('borra')

		return HttpResponseRedirect(self.get_success_url())

		# return reverse("administrators:link_generator")

	def get_success_url(self):
			# return reverse('teachers:planifications_list', )
		return reverse("administrators:link_generator")		# return render(request, 'opened_links.html',context)


class GetLinkView(View):
	context_object_name = 'calendar_homeworks_list'

	def get(self, request, **kwargs):
		pk=self.kwargs.get('pk', None)
		
		
		link_info = LinkInfo.objects.filter(pk=pk).values('pk')
		
		return JsonResponse(list(link_info), status = 200,safe=False)



class FinalLinkView(View):

	def get(self,request,**kwargs):
		context={}
		pk=self.kwargs.get('pk', None)

		
		processes = ProcessSteps.objects.filter(link_info=pk).order_by('pk')
			
		print('verificar pk',pk)
		progress_bar = []
		elapsed_time = []
		for x in processes:
			# print(x.calendar_date)
			if x.calendar_date is not None:
				print('dia de registro',x.register_date)
				
				# delta = x.calendar_date - x.register_date
				print('dia de calendario',x.calendar_date)
				

				# today = datetime.today().strftime('%Y-%m-%d')
				# This add (n) days no borrar
				today = datetime.now().date()
				print('verificar progreso',x.progress)
				# print('today',today)
				print('register date',x.register_date)
				if x.progress > 0:
					
					percentage = ((today - x.register_date)/x.progress)*100
					progress_bar.append({'id':x.pk,'percentage':percentage.days})
				else:
					percentage = 0;
			else:
				print('interesante')
				# print('register date type',type(x.register_date_time),'register date',x.register_date_time)
				# dt = datetime.strptime(str(x.register_date_time), '%Y-%m-%d %H:%M:%S')
				# print('register end date',x.register_date_time+timedelta(hours=3))
				# today = datetime.now()
				# today = datetime.now(timezone.utc)

				# print('todays datetime',today)
				print('horas',x.hours)
				print('minutos totales',x.hours * 60)
				print('etapas',(x.hours * 60)/30)
				elapsed_time.append({'id':x.pk,'progress':(x.hours * 60 )/30})
				# print('registrar ')
				# print('register date just date',x.register_date_time.date())
				# print('resta',today-x.register_date_time)
				# elapsed_time = today - x.register_date_time
				# print('el proceso se tiene que hacer con las horas',elapsed_time)	
		# print('verificar progreso',progress_bar)
		print('procesos',processes)
		# if processes
		try:
			link_info=LinkInfo.objects.get(pk=pk)
		except LinkInfo.DoesNotExist:
			link_info = None
		context['steps'] = processes
		# context['range_hours'] = range(1,hours)
		context['link_info'] = link_info
		context['progress_bar'] = progress_bar
		context['elapsed_time'] = elapsed_time
		return render(request, 'final_link.html',context)


class StatusChangeView(View):
	# context_object_name = 'calendar_homeworks_list'

	def post(self, request, **kwargs):
		pk=self.kwargs.get('pk', None)
		status=self.kwargs.get('status', None)

		
		print('pk',pk,'status',status)
		print('pk',type(pk),'status',type(status))

		

		status = ProcessStatus.objects.get(description__icontains=status)
		process_steps = ProcessSteps.objects.get(pk=pk)
		
		if status.description == "InProcess":
			if process_steps.calendar_date != None:
				print('calendar date',process_steps.calendar_date)
				print('register date',process_steps.register_date)
				delta = process_steps.calendar_date - process_steps.register_date
				days = delta.days
				
				process_steps.progress = days

		process_steps.process_status = status
		process_steps.save()


		print('process_steps.process_status',type(process_steps.process_status))
		return JsonResponse({'status':str(process_steps.process_status)}, status = 200,safe=False)

		
class SetDateView(View):
	# context_object_name = 'calendar_homeworks_list'

	def post(self, request, **kwargs):
		pk=self.kwargs.get('pk', None)
		
		data = json.load(request)
		calendar_value = data['calendarValue']
		
		process_steps = ProcessSteps.objects.get(pk=pk)
		process_steps.calendar_date = calendar_value
		process_steps.hours = None
		process_steps.save()
		
		return JsonResponse({'status':'ok'}, status = 200,safe=False)
		# return JsonResponse({'status':str(process_steps.process_status)}, status = 200,safe=False)

		
class SetHourView(View):
	# context_object_name = 'calendar_homeworks_list'

	def post(self, request, **kwargs):
		pk=self.kwargs.get('pk', None)
		
		data = json.load(request)
		hour_value = data['hourValue']
		print('verificar pk',pk)
		process_steps = ProcessSteps.objects.get(pk=pk)
		process_steps.hours = hour_value
		process_steps.register_date_time = datetime.today()
		process_steps.save()
		
		return JsonResponse({'pk':process_steps.pk}, status = 200,safe=False)
		# return JsonResponse({'status':str(process_steps.process_status)}, status = 200,safe=False)
