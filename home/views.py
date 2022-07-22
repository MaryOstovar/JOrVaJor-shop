from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.utils.text import slugify
from django.views import View
from home.forms import PostCreateForm
from django.contrib import messages
from home.models import Product


class HomeView(View):
    def get(self, request):
        try:
            products = Product.objects.all()
        except Product.DoesNotExist:
            raise 'error occurred'
        return render(request, 'home/home.html', {'products': products})


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
