import csv
from django.http import StreamingHttpResponse

class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        
        return value
class ConvertToCSVMixin():
    def get(self,request):
        res = super().get(request)

        if self.request.GET.get('limit') or self.request.GET.get('offset'):
            data = res.data["results"]
        else:
            data = res.data

        pseudo_buffer = Echo()
        writer = csv.DictWriter(f=pseudo_buffer,delimiter=";",fieldnames=data[0].keys())
        
        response = StreamingHttpResponse(
                ( writer.writerow(row) for row in data),
                content_type="text/csv",
                headers={'Content-Disposition': f'attachment; filename="{self.output_name}.csv"'},
        )
        return response