import random
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from shop.models import Penztargep,Partner,Bolt,Cikk

class Command(BaseCommand):
    help = 'Populate data'

    def create_partners(self):
      for _ in range(10):
        Partner.objects.create(nev=f"Partner_{get_random_string(8)}")

    def create_shops(self):
      for _ in range(20):
        p = Partner.objects.get(id=random.randint(1, Partner.objects.count()))
        Bolt.objects.create(
          nev=f"Bolt_{get_random_string(8)}",
          partner=p
          )

    def create_cash_register(self):
      b = Bolt.objects.get(id=random.randint(1, Bolt.objects.count()))
      for i in range(25):
        Penztargep.objects.create(bolt=b)

    def create_item(self):
      bulk_list = list()
      for _ in range(100):
        p = Partner.objects.get(id=random.randint(1, Partner.objects.count()))

        cikk = Cikk(
          nev=f"Cikk_{get_random_string(8)}",
          cikkszam=get_random_string(10),
          vonalkod=random.randint(50000, 8000000),
          mennyisegiegyseg = "db",
          nettoegysegar= random.randint(1000, 200000),
          verzio= random.randint(1, 5),
          partner=p
        )
        bulk_list.append(cikk)
      Cikk.objects.bulk_create(bulk_list)

    def handle(self, *args, **kwargs): 
      self.create_partners()
      self.create_shops()
      self.create_cash_register()
      self.create_item()

      