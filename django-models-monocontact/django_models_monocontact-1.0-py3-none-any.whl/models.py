from django.db import models
# from .managers import PersonaManager


class Persona(models.Model):
    nombre = models.CharField(db_column='Nombre', primary_key=True, max_length=50)  # Field name made lowercase.
    apellido = models.CharField(db_column='Apellido', max_length=45, blank=True, null=True)  # Field name made lowercase.
    telefono = models.IntegerField(db_column='Telefono', blank=True, null=True)  # Field name made lowercase.

    # persona_manager = PersonaManager()

    class Meta:
        managed = False
        db_table = 'persona'
