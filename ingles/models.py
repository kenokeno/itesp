from django.db import models
from django.urls import reverse

# Create your models here.
class Docente(models.Model):
    nombre = models.CharField(max_length=30)
    apellido_paterno = models.CharField(max_length=25)
    apellido_materno = models.CharField(max_length=25)
    telefono = models.CharField(max_length=12)
    correo = models.CharField(max_length=15)

    def __str__(self):
    	return self.nombre

    def get_absolute_url(self):
        return reverse('ingles:index_docente')

class Periodo(models.Model):
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    modalidad = models.CharField(max_length=10)

class Grupo(models.Model):
    nombre = models.CharField(max_length=3)    
    docente = models.ForeignKey(Docente, on_delete = models.PROTECT)
    periodo = models.ForeignKey(Periodo, on_delete = models.PROTECT)

class Alumno(models.Model):
    nombre = models.CharField(max_length=30)
    apellido_paterno = models.CharField(max_length=25)
    apellido_materno = models.CharField(max_length=25)
    origen = models.CharField(max_length=7)
    edad = models.IntegerField()
    
    def __unicode__(self):
        return self.nombre

class Calificaciones(models.Model):
    parcial = models.CharField(max_length=10)
    valor = models.CharField(max_length=10)
    grupo = models.ForeignKey(Grupo, on_delete = models.PROTECT)
    alumno = models.ForeignKey(Alumno, on_delete = models.PROTECT)

class Inscripcion(models.Model):
    #tipo_pago = models.CharField(max_length=1, choices=TIPO_PAGO_DESCRIPCION, default=DEPOSITO,)
    tipo_pago = models.CharField(max_length=1)
    plazo = models.CharField(max_length=10)
    fecha = models.DateField()
    alumno = models.ForeignKey(Alumno, on_delete = models.PROTECT)
    grupo = models.ForeignKey(Grupo, on_delete = models.PROTECT)

class Aula(models.Model):
    nombre = models.CharField(max_length=3)

class Horario(models.Model):
    dias = models.CharField(max_length=8)
    hora = models.TimeField()
    duracion = models.FloatField()
    aula = models.ForeignKey(Aula, on_delete = models.PROTECT)
    grupo = models.ForeignKey(Grupo, on_delete = models.PROTECT)