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
  partner_nev = serializers.CharField(source="partner.nev",read_only=True)
  class Meta:
    model = Bolt
    fields = ['id','nev','partner','partner_nev']

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
  partner_nev = serializers.CharField(source="partner.nev")
  bolt_nev = serializers.CharField(source="bolt.nev")
  penztargep = serializers.CharField(source="penztargep.uuid")

  class Meta:
    model = Vasarlas
    fields = ['id','esemenydatumido','vasarlasosszeg', 'bolt','bolt_nev','penztargep','partner','partner_nev']


class CikkDetailSerializer(serializers.ModelSerializer):
  class Meta:
    model = Cikk
    fields = ['id','cikkszam','vonalkod', 'mennyisegiegyseg','nettoegysegar','verzio','partner','vasarlas_tetelek']

class CikkSerializer(serializers.ModelSerializer):
  partner = serializers.CharField(source="partner.nev")
  class Meta:
    model = Cikk
    fields = ['id','cikkszam','vonalkod', 'mennyisegiegyseg','nettoegysegar','verzio','partner']
