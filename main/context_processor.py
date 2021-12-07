from .models import *
def get_categories(request):
    categories = Category.objects.filter(parent__isnull=True)
    return {'categories': categories}