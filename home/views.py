from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.views import View
from home.forms import ProductCreateForm, SearchForm, CommentCreateForm, CommentReplyForm
from django.contrib import messages
from home.models import Product, Category, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class HomeView(View):
    form_class = SearchForm

    def get(self, request, category_slug=None):
        form = self.form_class()
        default_page = 1
        page = request.GET.get('page', default_page)

        categories = Category.objects.all()
        products = Product.objects.all()

        if category_slug:
            category = Category.objects.get(slug=category_slug)
            products = products.filter(category=category)

        if request.GET.get('search'):
            products = Product.objects.filter(name__contains=request.GET['search'])

        # Paginate items
        items_per_page = 8
        paginator = Paginator(products, items_per_page)
        try:
            items_page = paginator.page(page)
        except PageNotAnInteger:
            items_page = paginator.page(default_page)
        except EmptyPage:
            items_page = paginator.page(paginator.num_pages)

        return render(request, 'home/home.html', {'form': form, 'products': products,
                                                  'categories': categories, 'items_page': items_page})


class MyProductsView(LoginRequiredMixin, View):
    def get(self, request, pk):
        products = Product.objects.filter(user=request.user)
        return render(request, 'home/my-products.html', {'products': products})


class AboutView(View):
    def get(self, request):
        return render(request, 'home/about.html')


class ProductCreateView(LoginRequiredMixin, View):
    form_class = ProductCreateForm

    def get(self, request):
        return render(request, 'home/product-create.html', {'form': self.form_class()})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            new_product = form.save(commit=False)
            cd = form.cleaned_data
            new_product.slug = slugify(cd['name'])
            new_product.user = request.user
            new_product.save()
            form.save_m2m()
            messages.success(request, 'post create successfully', 'success')
            return redirect('home:home')
        messages.error(request, 'your data wrong', 'danger')
        return redirect('product-create')


class ProductDetailView(View):
    form_class = CommentCreateForm
    reply_form_class = CommentReplyForm

    def setup(self, request, *args, **kwargs):
        self.product_instance = get_object_or_404(Product, pk=kwargs['pk'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        comment_form = self.form_class()
        product = self.product_instance
        comments = product.pcomments.filter(is_reply=False)
        return render(request, 'home/detail.html', {'product': product, 'comments': comments, 'form': comment_form,
                                                    'reply_form': self.reply_form_class()})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.product = self.product_instance
            new_comment.save()
            return redirect('product-detail', self.product_instance.pk)
        return redirect('product-detail', self.product_instance.pk)


class ProductAddReplyView(LoginRequiredMixin, View):
    from_class = CommentReplyForm

    def post(self, request, post_pk, comment_pk):
        product = Product.objects.get(pk=post_pk)
        comment = Comment.objects.get(pk=comment_pk)
        form = self.from_class(request.POST)
        if form.is_valid():
            reply_comment = form.save(commit=False)
            reply_comment.product = product
            reply_comment.reply = comment
            reply_comment.user = request.user
            reply_comment.is_reply = True
            reply_comment.save()
            messages.success(request, 'you reply successfully', 'success')
        return redirect('product-detail', product.pk)


class ProductDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        product = Product.objects.filter(pk=pk).first()
        if request.user == product.user:
            product.delete()
            messages.success(request, 'product delete successfully', 'success')
            return redirect('home:my-products', request.user.pk)
        messages.error(request, 'your not allowed', 'danger')
        return redirect('home:home')


class ProductEditView(LoginRequiredMixin, View):
    from_class = ProductCreateForm

    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        form = self.from_class(instance=product)
        return render(request, 'home/product-create.html', {'form': form})

    def post(self, request, pk):
        product = Product.objects.get(pk=pk)
        form = self.from_class(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save(commit=False)
            form.slug = slugify(form.cleaned_data['name'])

            form.save()
            messages.success(request, 'product edit successfully', 'success')
            return redirect('home:home')
        messages.error(request, 'you data is wrong', 'danger')
        return redirect('home:home')
