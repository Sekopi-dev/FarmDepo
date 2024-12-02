from .models import Catergory


def categories(request):
    categories = Catergory.objects.all()  # Fetch all categories
    return {'categories': categories}




