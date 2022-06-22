from rest_framework import serializers
from .models import (Bolt,Partner,Penztargep,Vasarlas,VasarlasTetel,Cikk)

class PartnerSerializer(serializers.ModelSerializer):
  class Meta:
    model = Partner
    fields = ['id', 'nev']

class PartnerDetailSerializer(serializers.ModelSerializer):
  class Meta:
    model = Partner
    fields = ['id', 'nev','boltok','vasarlasok','vasarlas_tetelek','cikkek']

class BoltSerializer(serializers.ModelSerializer):
  class Meta:
    model = Bolt
    fields = ['id','nev','partner']

class PenztargepSerializer(serializers.ModelSerializer):
  class Meta:
    model = Penztargep
    fields = ['id','uuid','bolt']

class BoltDetailSerializer(serializers.ModelSerializer):
  partner = PartnerSerializer(read_only=True)
  class Meta:
    model = Bolt
    fields = ['id','nev','partner','penztargepek']

class VasarlasTetelSerializer(serializers.ModelSerializer):
  class Meta:
    model = VasarlasTetel
    fields = '__all__'

class VasarlasDetailSerializer(serializers.ModelSerializer):
  partner = PartnerSerializer(read_only=True)
  bolt = BoltSerializer(read_only=True)
  penztargep = PenztargepSerializer(read_only=True)
  vasarlas_tetelek = VasarlasTetelSerializer(read_only=True,many=True)
  class Meta:
    model = Vasarlas
    fields = ['id','esemenydatumido','vasarlasosszeg', 'bolt','penztargep','partner','vasarlas_tetelek']

class VasarlasSerializer(serializers.ModelSerializer):
  class Meta:
    model = Vasarlas
    fields = ['id','esemenydatumido','vasarlasosszeg', 'bolt','penztargep','partner']


class CikkDetailSerializer(serializers.ModelSerializer):
  class Meta:
    model = Cikk
    fields = ['id','cikkszam','vonalkod', 'mennyisegiegyseg','nettoegysegar','verzio','partner','vasarlas_tetelek']

class CikkSerializer(serializers.ModelSerializer):
  class Meta:
    model = Cikk
    fields = '__all__'
