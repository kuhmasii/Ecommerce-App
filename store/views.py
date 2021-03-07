from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from . models import Product, Category
from django.conf import settings
from cart.forms import CartForm


def store_page(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    product = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        product = category.products.filter(available=True)
        # product = product.filter(category=category)

    # using paginator
    paginator = Paginator(product, 12)
    page = request.GET.get("page")

    try:
        product = paginator.page(page)
    except PageNotAnInteger:
        # if the page is not an integer that means probably the beginning of the page
        product = paginator.page(1)
    except EmptyPage:
        # if possible the page is out of index, bring out the last page.
        product = paginator.page(page.num_pages)

    return render(request, 'store-page.html', dict(category=category, categories=categories,
                                                   product=product, page=page))


def detail_page(request, slug=None, detail_id=None):

    product = get_object_or_404(
        Product, slug=slug, id=detail_id, available=True)
    form = CartForm()
    return render(request, 'store/detail.html', {"product": product, 'form': form})
