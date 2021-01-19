from django.shortcuts import render, get_object_or_404
from . models import Product, Category


def store_page(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    product = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        product = category.products.filter(available=True)
        # product = product.filter(category=category)


    return render(request, 'store-page.html', dict(category=category, categories=categories,
                                                   product=product))


def detail_page(request, slug=None, detail_id=None):

    product = get_object_or_404(
        Product, slug=slug, id=detail_id, available=True)

    return render(request, 'store/detail.html', {"product": product})
