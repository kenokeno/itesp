from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django_tables2 import SingleTableView
from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView
from django.conf import settings
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Table, TableStyle
from reportlab.lib.units import cm
from reportlab.lib import colors

from .tables import DocentesTable, DocenteFilter
from .models import Docente

class DocenteList(SingleTableMixin, FilterView):
	model = Docente
	template_name = "docente/index.html"
	table_class = DocentesTable
	filterset_class = DocenteFilter

class DocenteDetail(generic.DetailView):
	model = Docente
	template_name = "docente/detail.html"

class DocenteUpdate(UpdateView):
	model = Docente
	fields = ['nombre', 'apellido_paterno', 'apellido_materno', 'telefono', 'correo']
	template_name = "docente/edit.html"

class DocenteDelete(DeleteView):
	model = Docente
	template_name = "docente/delete.html"
	success_url = reverse_lazy("ingles:index_docente")

class DocenteCreate(CreateView):
	model = Docente
	template_name = 'docente/new.html'
	fields = '__all__'

class ReporteDocentesPDF(generic.View):
	    def cabecera(self,pdf):
	        logo = ImageReader(settings.MEDIA_ROOT + '/images/ingles.png')
	        pdf.drawImage(logo, 40, 750, 120, 90, preserveAspectRatio = True)
	        pdf.setFont("Helvetica", 16)
	        pdf.drawString(230, 790, u"DEPARTAMENTO DE INGLES")
	        pdf.setFont("Helvetica", 14)
	        pdf.drawString(245, 770, u"REPORTE DE DOCENTES")

	    def tabla(self,pdf,y):
	        #Creamos una tupla de encabezados para neustra tabla
	        encabezados = ('Nombre', 'Apellido Paterno', 'Apellido Materno', 'Telefono', 'Correo')
	        #Creamos una lista de tuplas que van a contener a las personas
	        detalles = [(docente.nombre, docente.apellido_paterno, docente.apellido_materno, docente.telefono, docente.correo) for docente in Docente.objects.all()]
	        #Establecemos el tamaño de cada una de las columnas de la tabla
	        detalle_orden = Table([encabezados] + detalles, colWidths=[2 * cm, 4 * cm, 4 * cm, 4 * cm])
	        #Aplicamos estilos a las celdas de la tabla
	        detalle_orden.setStyle(TableStyle(
	            [
	            #La primera fila(encabezados) va a estar centrada
	            ('ALIGN',(0,0),(3,0),'CENTER'),
	            #Los bordes de todas las celdas serán de color negro y con un grosor de 1
	            ('GRID', (0, 0), (-1, -1), 1, colors.black),
	            #El tamaño de las letras de cada una de las celdas será de 10
	            ('FONTSIZE', (0, 0), (-1, -1), 10),
	            ]
	        ))
	        #Establecemos el tamaño de la hoja que ocupará la tabla
	        detalle_orden.wrapOn(pdf, 800, 600)
	        #Definimos la coordenada donde se dibujará la tabla
	        detalle_orden.drawOn(pdf, 60,y)

	    def get(self, request, *args, **kwargs):
	        response = HttpResponse(content_type='application/pdf')
	        buffer = BytesIO()
	        pdf = canvas.Canvas(buffer)
	        self.cabecera(pdf)
	        y = 600
	        self.tabla(pdf, y)
	        pdf.showPage()
	        pdf.save()
	        pdf = buffer.getvalue()
	        buffer.close()
	        response.write(pdf)
	        return response