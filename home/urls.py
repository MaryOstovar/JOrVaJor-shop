from django.urls import path
from home.views import HomeView, AboutView, ProductCreateView, MyProductsView, ProductDetailView, ProductDeleteView, \
    ProductEditView, ProductAddReplyView

app_name = 'home'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('category/<slug:category_slug>/', HomeView.as_view(), name='category_filter'),
    path('<int:pk>', MyProductsView.as_view(), name='my-products'),
    path('about/', AboutView.as_view(), name='about'),
    path('post/create/', ProductCreateView.as_view(), name='product-create'),
    path('post/detail/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('post/delete/<int:pk>/', ProductDeleteView.as_view(), name='product-delete'),
    path('post/edit/<int:pk>/', ProductEditView.as_view(), name='product-edit'),
    path('reply/<int:post_pk>/<int:comment_pk>/', ProductAddReplyView.as_view(), name='add_reply'),

]
