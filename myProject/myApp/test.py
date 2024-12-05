from django.http import HttpResponse
from django.db.models.functions import Length
from models import Product

def check_code_length(request):
    
    objs = Product.objects.annotate(
        code_length=Length('code')
    ).filter(
        code_length__gt=10
    ).values(
        'pk', 'code', 'code_length'
    )

    for obj in objs:
        print(f'Object with ID {obj["pk"]} has a field with length {obj["problematic_field_length"]}: {obj["code"]}')