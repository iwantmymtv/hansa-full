from django.contrib import admin

from .models import (Bolt,Partner,Penztargep,Vasarlas,VasarlasTetel,Cikk)

@admin.register(Bolt)
class BoltAdmin(admin.ModelAdmin):
    pass

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    pass

@admin.register(Penztargep)
class PenztargepAdmin(admin.ModelAdmin):
    pass

@admin.register(Vasarlas)
class VasarlasAdmin(admin.ModelAdmin):
    pass

@admin.register(VasarlasTetel)
class VasarlasTetelAdmin(admin.ModelAdmin):
    pass

@admin.register(Cikk)
class CikkAdmin(admin.ModelAdmin):
    pass
