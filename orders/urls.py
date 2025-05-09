from django.urls import path, include
from rest_framework.routers import DefaultRouter

from orders.views import OrderViewSet, OrderItemViewSet

app_name = "orders"

router = DefaultRouter()
router.register(r"^(?P<order_id>\d+)/items", OrderItemViewSet, basename="order-items")
router.register("", OrderViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
