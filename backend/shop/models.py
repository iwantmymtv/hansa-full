import uuid
from django.db import models
from django.utils import timezone


class Partner(models.Model):
  nev = models.CharField(max_length=256)

  def __str__(self) -> str:
    return self.nev

class Bolt(models.Model):
  nev = models.CharField(max_length=256)
  partner = models.ForeignKey('Partner', on_delete=models.SET_NULL,null=True, related_name='boltok')
  
  def __str__(self) -> str:
      return self.nev

class Penztargep(models.Model):
  uuid = models.UUIDField(default=uuid.uuid4, editable=False)
  bolt = models.ForeignKey('Bolt', on_delete=models.SET_NULL,null=True, related_name='penztargepek')

  def __str__(self) -> str:
    return str(self.uuid)

class Vasarlas(models.Model):
  esemenydatumido = models.DateTimeField(default=timezone.now)
  vasarlasosszeg = models.FloatField()
  partner = models.ForeignKey('Partner', on_delete=models.SET_NULL,null=True,related_name='vasarlasok')
  bolt = models.ForeignKey('Bolt', on_delete=models.SET_NULL,null=True,related_name='vasarlasok')
  penztargep = models.ForeignKey('Penztargep', on_delete=models.SET_NULL,null=True, related_name='vasarlasok')

  def __str__(self) -> str:
      return str(self.id)

class VasarlasTetel(models.Model):
  vasarlas = models.ForeignKey('Vasarlas', on_delete=models.CASCADE,related_name="vasarlas_tetelek")
  mennyiseg = models.FloatField()
  brutto = models.FloatField()
  partner = models.ForeignKey('Partner', on_delete=models.SET_NULL,null=True,related_name='vasarlas_tetelek')
  partnercikk = models.ForeignKey('Cikk',on_delete=models.SET_NULL,null=True,related_name='vasarlas_tetelek')

  def __str__(self) -> str:
      return str(self.id)
      
class Cikk(models.Model):
  nev = models.CharField(max_length=256)
  cikkszam = models.CharField(max_length=256)
  vonalkod = models.CharField(max_length=256)
  mennyisegiegyseg = models.CharField(max_length=256)
  nettoegysegar = models.FloatField()
  verzio = models.PositiveIntegerField(default=1)
  partner = models.ForeignKey('Partner', on_delete=models.CASCADE,related_name='cikkek')

  def __str__(self) -> str:
    return self.nev