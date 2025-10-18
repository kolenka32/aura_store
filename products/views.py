from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, DetailView
from django.template.response import TemplateResponse
from django.db.models import Q

from products.models import Category, Product, Size



class IndexView(TemplateView):
    template_name = 'products/base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'AURA STORE'
        context['categories'] = Category.objects.all()
        category_slug = kwargs.get('category_slug')

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        return TemplateResponse(request, self.template_name, context)


class CatalogView(TemplateView):
    template = 'products/catalog.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = kwargs.get('category_slug')
        categories = Category.objects.all()
        products = Product.objects.all().order_by('-created_at')
        current_category = None

        if category_slug:
            current_category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=current_category)

        query = self.request.GET.get('q')
        if query:
            products = products.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )

        context.update({
            'categories': categories,
            'products': products,
            'current_category': category_slug,
            'sizes': Size.objects.all(),
            'search_query': query or '',
            'title': 'AURA STORE',
        })

        if self.request.GET.get('show_search') == 'true':
            context['show_search'] = True
        elif self.request.GET.get('reset_search') == 'true':
            context['reset_search'] = True
        return context


    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        if request.headers.get('HX-Request'):
            if context.get('show_search'):
                print(context.get('show_search'))
                return TemplateResponse(request, 'products/search_input.html', context)
            elif context.get('reset_search'):
                return TemplateResponse(request, 'products/search_button.html', {})

            return TemplateResponse(request, self.template, context)
        return TemplateResponse(request, self.template, context)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    slug_field = 'slug'    # поле модели для поиска
    slug_url_kwarg = 'slug'  # имя параметра в URL

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context['title'] = 'AURA STORE'
        context['categories'] = Category.objects.all()
        context['product_name'] = product.name

        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(**kwargs)

        return TemplateResponse(request, self.template_name, context)