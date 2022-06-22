from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from shop import api

urlpatterns = [
    path('boltok/', api.BoltList.as_view()),
    path('boltok/export/', api.BoltExportView.as_view()),
    path('boltok/<int:pk>/', api.BoltDetail.as_view()),

    path('penztargepek/', api.PenztargepList.as_view()),
    path('penztargepek/export/', api.PenztargepExportView.as_view()),
    path('penztargepek/<int:pk>/', api.PenztargepDetail.as_view()),

    path('partnerek/', api.PartnerList.as_view()),
    path('partnerek/export/', api.PartnerExportView.as_view()),
    path('partnerek/<int:pk>/', api.PartnerDetail.as_view()),

    path('vasarlasok/', api.VasarlasList.as_view()),
    path('vasarlasok/export/', api.VasarlasExportView.as_view()),
    path('vasarlasok/<int:pk>/', api.VasarlasDetail.as_view()),

    path('vasarlas_tetelek/', api.VasarlasTetelList.as_view()),
    path('vasarlas_tetelek/export/', api.VasarlasTetelExportView.as_view()),
    path('vasarlas_tetelek/<int:pk>/', api.VasarlasTetelDetail.as_view()),

    path('cikkek/', api.CikkList.as_view()),
    path('cikkek/export/', api.CikkExportView.as_view()),
    path('cikkek/<int:pk>/', api.CikkDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)