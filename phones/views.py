from django.shortcuts import get_object_or_404, redirect, render

from .models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    template = 'catalog.html'
    sort = request.GET.get('sort')
    phones_qs = Phone.objects.all()

    if sort == 'name':
        phones_qs = phones_qs.order_by('name')
    elif sort == 'min_price':
        phones_qs = phones_qs.order_by('price')
    elif sort == 'max_price':
        phones_qs = phones_qs.order_by('-price')

    context = {
        'phones': phones_qs,
    }
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    phone = get_object_or_404(Phone, slug=slug)

    context = {
        'phone': phone,
    }
    return render(request, template, context)
