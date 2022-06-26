

from collections import OrderedDict

from django.http import Http404
from django.db.models import Q

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import (Bolt,Partner,Penztargep,Vasarlas,VasarlasTetel,Cikk)
from .mixins import ConvertToCSVMixin

from .serializers import (
    BoltSerializer,
    BoltDetailSerializer,
    PartnerSerializer,
    PartnerDetailSerializer,
    PenztargepSerializer,
    VasarlasSerializer,
    VasarlasDetailSerializer,
    VasarlasTetelSerializer,
    CikkSerializer,
    CikkDetailSerializer
)

class BoltList(APIView):
    filters = Q()
    orderby = '-id'
    order_options = ['-id','id','nev','-nev']
    count = 0

    def get(self, request, format=None):

        partner_filter = self.request.GET.get('partner',None)
        search = self.request.GET.get('search',None)
        order = self.request.GET.get('ordering', None)

        limit = self.request.GET.get('limit', None)
        offset = self.request.GET.get('offset', 0)

        if partner_filter:
            self.filters &= Q(partner=partner_filter)

        if search:
            self.filters &= (
                Q(partner__nev__icontains=search) | 
                Q(nev__icontains=search) | 
                Q(partner__id__icontains=search)
            )


        if order and order in self.order_options:
            self.orderby = order

        boltok_qs = Bolt.objects.filter(self.filters).order_by(self.orderby)

        if limit:
            self.count = boltok_qs.count()
            boltok_qs = boltok_qs[int(offset):int(offset)+int(limit)]
            res = Response(OrderedDict([
                ('count', self.count),
                ('next', None),
                ('previous',None),
                ('results', BoltSerializer(boltok_qs, many=True).data)
            ]))
        else:
            serializer = BoltSerializer(boltok_qs, many=True)
            res =  Response(serializer.data)

        return res

    def get_next_link(self,request):
        pass
    
    def get_previous_link(self,request):
        pass

    def post(self, request, format=None):
        serializer = BoltSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class BoltExportView(ConvertToCSVMixin,BoltList):
    output_name = "boltok"

class BoltDetail(APIView):
    def get_object(self, pk):
        try:
            return Bolt.objects.get(pk=pk)
        except Bolt.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        bolt = self.get_object(pk)
        serializer = BoltDetailSerializer(bolt)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        bolt = self.get_object(pk)
        serializer = BoltSerializer(bolt, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        bolt = self.get_object(pk)
        bolt.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#pentzargep
class PenztargepList(generics.ListCreateAPIView):
    queryset = Penztargep.objects.all()
    serializer_class = PenztargepSerializer

class PenztargepExportView(ConvertToCSVMixin,PenztargepList):
    output_name = "penztargepek"

class PenztargepDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Penztargep.objects.all()
    serializer_class = PenztargepSerializer

#partner
class PartnerList(generics.ListCreateAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer

class PartnerExportView(ConvertToCSVMixin,PartnerList):
    output_name = "partnerek"

class PartnerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Partner.objects.all()

    def get_serializer_class(self):
        if self.request.method == "PUT":
            return PartnerSerializer
        
        return PartnerDetailSerializer

#vasarlas
class VasarlasList(generics.ListCreateAPIView):
    queryset = Vasarlas.objects.all()
    serializer_class = VasarlasSerializer
    filterset_fields = [ 'vasarlasosszeg','bolt','partner','penztargep']
    search_fields = ['vasarlasosszeg', 'bolt']
    ordering_fields = ['vasarlasosszeg', 'esemenydatumido']

class VasarlasExportView(ConvertToCSVMixin,VasarlasList):
    output_name = "vasarlasok"

class VasarlasDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vasarlas.objects.all()

    def get_serializer_class(self):
        if self.request.method == "PUT":
            return VasarlasSerializer
        
        return VasarlasDetailSerializer

#partnervasarlas_tetel
class VasarlasTetelList(generics.ListCreateAPIView):
    queryset = VasarlasTetel.objects.all()
    serializer_class = VasarlasTetelSerializer
    filterset_fields = [ 'vasarlas','partnercikk','partner']
    search_fields = ['id','vasarlas', 'partner','partnercikk__nev']
    ordering_fields = ['mennyiseg', 'brutto']

class VasarlasTetelExportView(ConvertToCSVMixin,VasarlasTetelList):
    output_name = "vasarlas_tetelek"

class VasarlasTetelDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = VasarlasTetel.objects.all()
    serializer_class = VasarlasTetelSerializer

class CikkList(generics.ListCreateAPIView):
    queryset = Cikk.objects.all()
    serializer_class = CikkSerializer
    filterset_fields = ['nettoegysegar','verzio','partner','mennyisegiegyseg']
    search_fields = ['nev','nettoegysegar','verzio','partner__nev','mennyisegiegyseg']
    ordering_fields = '__all__'

class CikkExportView(ConvertToCSVMixin,CikkList):
    output_name = "cikkek"

class CikkDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cikk.objects.all()

    def get_serializer_class(self):
        if self.request.method == "PUT":
            return CikkSerializer
        
        return CikkDetailSerializer