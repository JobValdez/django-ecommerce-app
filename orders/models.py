from django.db import models
from django.contrib.auth import get_user_model
from users.models import Address
from products.models import Product
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _



User = get_user_model()


class Order(models.Model):
    PENDING = "P"
    COMPLETED = "C"
    
    STATUS_CHOICES = ((PENDING, _("Pending")), (COMPLETED, _("Completed")))
    
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=PENDING)
    shipping_address = models.ForeignKey(Address, related_name="shipping_orders", on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(Address, related_name="billing_orders", on_delete=models.SET_NULL, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-created_at"]
        
    def __str__(self):
        return self.buyer.get_full_name()
    
    

    @cached_property
    def total_price(self):
        """
        Total cost of all the items in an order
        """
        return round(sum([order_item.cost for order_item in self.order_items.all()]), 2)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_orders")
    quantity = models.PositiveIntegerField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-created_at"]
        
    def __str__(self):
        return self.order.buyer.get_full_name()
    
    @cached_property
    def cost(self):
        """
        Total Cost of the order item
        """
        return round(self.product.price * self.quantity, 2)