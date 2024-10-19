import django_tables2 as tables
import django_filters
from django_tables2.utils import A
from .models import Docente

class DocentesTable(tables.Table):
	editar = tables.TemplateColumn("<a href={% url 'ingles:edit_docente' record.pk %}> &#x270e;</a>")
	eliminar = tables.TemplateColumn("<a href={% url 'ingles:delete_docente' record.pk %}> &#10060;</a>")
	id = tables.LinkColumn("ingles:detail_docente", args=[A("pk")])
	class Meta:
		model = Docente
		attrs = {"class": "table"}

class DocenteFilter(django_filters.FilterSet):
	class Meta:
		model = Docente
		fields = ['nombre', 'apellido_paterno', 'apellido_materno'] 