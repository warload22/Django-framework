from django.conf import settings
from django.db import models
from lootapp.models import Material
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete, pre_save
from django.db.models import Q


class Order(models.Model):

    STATUS_FORMING = 'FM'
    STATUS_SEND_TO_PAYMENT = 'STP'
    STATUS_PAID = 'PD'
    STATUS_DONE = 'DN'
    STATUS_CANCELED = 'CN'

    STATUSES = ((STATUS_FORMING, "Forming"),
                (STATUS_SEND_TO_PAYMENT, "Waiting for payment"),
                (STATUS_PAID, "Paid"),
                (STATUS_DONE, "Done"),
                (STATUS_CANCELED, "Canceled"))

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUSES, default=STATUS_FORMING, max_length=3)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def get_summary(self):
        _items = self.orderitems.select_related()
        return {
            'total_cost': sum(list(map(lambda x: x.cost, _items))),
            'total_quantity': sum(list(map(lambda x: x.quantity, _items)))
        }

    @property
    def total_cost(self):
        _items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.cost, _items)))

    @property
    def total_quantity(self):
        _items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.quantity, _items)))

    def delete(self):
        for item in self.orderitems.select_related():
            item.delete()
        self.is_active = False
        self.status = self.STATUS_CANCELED
        self.save()


class OrderItem(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderitems')
    material = models.ForeignKey(Material, on_delete=models.CASCADE, verbose_name='Material',
                                 limit_choices_to=Q(is_purchasable=True))
    quantity = models.PositiveIntegerField(default=0, verbose_name='Quantity', )

    @property
    def cost(self):
        return self.material.price_rp * self.quantity

    @staticmethod
    def get_item(pk):
        return OrderItem.objects.get(pk=pk)


@receiver(post_save, sender=OrderItem)
def item_post_save_adjustments(sender, update_fields, instance, **kwargs):
    if instance.quantity == 0:
        instance.delete()
    try:
        item = OrderItem.objects.get(Q(order=instance.order, material=instance.material), ~Q(pk=instance.pk))
        item.quantity += instance.quantity
        instance.delete()
        item.save()
    except (OrderItem.DoesNotExist, AssertionError):
        pass


@receiver(pre_save, sender=OrderItem)
def material_quantity_update_save(sender, update_fields, instance, **kwargs):
    if instance.pk:
        instance.material.quantity -= instance.quantity - instance.get_item(instance.pk).quantity
    else:
        instance.material.quantity -= instance.quantity
    instance.material.save()


@receiver(pre_delete, sender=OrderItem)
def material_quantity_update_delete(sender, instance, **kwargs):
    instance.material.quantity += instance.quantity
    instance.material.save()




