from django.contrib import admin
from django.urls import path
from . import docentes
from .docentes import *
from . import views

app_name = 'ingles'
urlpatterns = [
	path('', views.index, name='index'),
	path('docentes/', DocenteList.as_view(), name="index_docente"),
	path('docentes/detail/<int:pk>', DocenteDetail.as_view(), name="detail_docente"),
	path('docentes/edit/<int:pk>', DocenteUpdate.as_view(), name="edit_docente"),
	path('docentes/delete/<int:pk>', DocenteDelete.as_view(), name="delete_docente"),
	path('docentes/new/', DocenteCreate.as_view(), name="new_docente"),
	path('docentes/report/', ReporteDocentesPDF.as_view(), name="report_docente"),
]