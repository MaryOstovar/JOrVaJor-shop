from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from django.views import View
from home.forms import PostCreateForm, SearchForm
from django.contrib import messages
from home.models import Product


class HomeView(View):
    form_class = SearchForm

    def get(self, request):
        form = self.form_class()
        try:
            products = Product.objects.all()
        except Product.DoesNotExist:
            raise 'error occurred'
        if request.GET.get('search'):
            products = Product.objects.filter(name__contains=request.GET['search'])
        return render(request, 'home/home.html', {'form': form, 'products': products})


class MyPostsView(LoginRequiredMixin, View):
    def get(self, request, pk):
        products = Product.objects.filter(user=request.user)
        return render(request, 'home/my_posts.html', {'products': products})


class AboutView(View):
    def get(self, request):
        return render(request, 'home/about.html')


class PostCreateView(LoginRequiredMixin, View):
    form_class = PostCreateForm

    def get(self, request):
        return render(request, 'home/post_create.html', {'form': self.form_class()})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            cd = form.cleaned_data
            new_post.slug = slugify(cd['name'])
            new_post.user = request.user
            new_post.save()
            messages.success(request, 'post create successfully', 'success')
            return redirect('home:home')
        messages.error(request, 'your data wrong', 'danger')
        return redirect('home:post_create')


class PostDetailView(View):
    def get(self, request, pk):
        product = Product.objects.filter(pk=pk).first()
        return render(request, 'home/detail.html', {'product': product})


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        product = Product.objects.filter(pk=pk).first()
        if request.user == product.user:
            product.delete()
            messages.success(request, 'product delete successfully', 'success')
            return redirect('home:my_post', request.user.pk)
        messages.error(request, 'your not allowed', 'danger')
        return redirect('home:home')


class PostEditView(LoginRequiredMixin, View):
    from_class = PostCreateForm

    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        form = self.from_class(instance=product)
        return render(request, 'home/post_create.html', {'form': form})

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
