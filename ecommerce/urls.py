from django.contrib import admin
from django.urls import path
from store import views  # Import your app's views
from django.conf.urls.static import static
from django.conf import settings
from store.views import login_view, register_view, payments_page
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_required(views.home), name='home'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),

    # ✅ Payment flow routes
    path('payments/', views.payments_page, name='payments'),
    path('stk_push/', views.stk_push, name='stk_push'),
]

# ✅ Serve media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
