from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from orderapp.models import Order, OrderItem

from orderapp.forms import OrderItemForm, OrderForm

from lootapp.models import PurchasedMaterial

from lootapp.models import Material


class OrderListView(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super(ListView, self).dispatch(*args, **kwargs)


class OrderCreateView(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('order:list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, OrderItemForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            formset = OrderFormSet()
        context_data['orderitems'] = formset
        return context_data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        if self.object.total_cost == 0:
            self.object.delete()

        return super().form_valid(form)

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super(CreateView, self).dispatch(*args, **kwargs)


class OrderUpdateView(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('order:list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, OrderItemForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST, instance=self.object)
        else:
            formset = OrderFormSet(instance=self.object)
            for form in formset.forms:
                if form.instance.pk:
                    form.initial['price'] = form.instance.material.price_rp

        context_data['orderitems'] = formset
        return context_data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        if self.object.total_cost == 0:
            self.object.delete()

        return super().form_valid(form)

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super(UpdateView, self).dispatch(*args, **kwargs)


class OrderDetailView(DetailView):
    model = Order

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super(DetailView, self).dispatch(*args, **kwargs)


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('order:list')

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super(DeleteView, self).dispatch(*args, **kwargs)


def order_sending_to_payment(request, pk):
    order = Order.objects.get(pk=pk)
    order.status = Order.STATUS_SEND_TO_PAYMENT
    order.save()
    return HttpResponseRedirect(reverse('order:payment', kwargs={'pk': pk}))


def order_payment(request, pk):
    order = Order.objects.get(pk=pk)
    if order.user.rp >= order.total_cost:
        order.user.subtract_rp(order.total_cost)
        order.status = Order.STATUS_PAID
        order.save()
        for item in OrderItem.objects.filter(order=order):
            purchased = PurchasedMaterial(material=item.material, user=order.user, quantity=item.quantity)
            purchased.save()
        order.status = Order.STATUS_DONE
        order.save()
    return HttpResponseRedirect(reverse('order:list'))


def get_material_price(request, pk):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        material_item = Material.objects.filter(pk=pk).first()
        if material_item:
            return JsonResponse({'price': material_item.price_rp})
        else:
            return JsonResponse({'price': 0})