from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, UpdateView, CreateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from adminapp.forms import PlayerEditAdminForm, CategoryEditForm, ChampionEditForm, SkinEditForm
from authapp.models import Player
from mainapp.models import Champion, Skin
from authapp.forms import PlayerRegisterForm
from mainapp.models import CollectionCategory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class AccessMixin:

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    if request.method == 'POST':
        user_form = PlayerRegisterForm(request.POST, request.FILES)

        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('admin:user_list'))
    else:
        user_form = PlayerRegisterForm()

    context = {
        'title': 'create user',
        'form': user_form
    }
    return render(request, 'adminapp/user_edit.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def user_list(request, page=1):

    paginator = Paginator(Player.objects.all().order_by('-is_active', 'nickname'), 9)
    try:
        users_paginator = paginator.page(page)
    except PageNotAnInteger:
        users_paginator = paginator.page(1)
    except EmptyPage:
        users_paginator = paginator.page(paginator.num_pages)

    context = {
        'title': 'users',
        'users': users_paginator
    }
    return render(request, 'adminapp/user_list.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def user_edit(request, pk=None):
    current_user = Player.objects.get(pk=pk)
    if request.method == 'POST':
        user_form = PlayerEditAdminForm(request.POST, request.FILES, instance=current_user)

        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('admin:user_list'))
    else:
        user_form = PlayerEditAdminForm(instance=current_user)
    context = {
        'title': 'edit user',
        'form': user_form,
        'user': current_user
    }
    return render(request, 'adminapp/user_edit.html', context=context)


class UserDetailView(AccessMixin, DetailView):
    model = Player
    template_name = 'adminapp/user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Player.objects.get(pk=self.kwargs['pk']).nickname

        return context


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk=None):
    current_user = get_object_or_404(Player, pk=pk)

    if request.method == 'POST':
        if current_user.is_active:
            current_user.is_active = False
        else:
            current_user.is_active = True
        current_user.save()
        return HttpResponseRedirect(reverse('admin:user_list'))
    context = {
        'title': 'ban user',
        'user': current_user
    }
    return render(request, 'adminapp/user_ban.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def category_create(request):
    if request.method == 'POST':
        category_form = CategoryEditForm(request.POST, request.FILES)

        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('admin:category_list'))
    else:
        category_form = CategoryEditForm()

    context = {
        'title': 'create category',
        'form': category_form
    }
    return render(request, 'adminapp/category_edit.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def category_list(request):
    context = {
        'title': 'categories',
        'categories': CollectionCategory.objects.all()
    }
    return render(request, 'adminapp/category_list.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def category_edit(request, pk=None):
    category = CollectionCategory.objects.get(pk=pk)
    if request.method == 'POST':
        category_form = CategoryEditForm(request.POST, request.FILES, instance=category)

        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('admin:category_list'))
    else:
        category_form = CategoryEditForm(instance=category)
    context = {
        'title': 'edit category',
        'form': category_form,
        'category': category
    }
    return render(request, 'adminapp/category_edit.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def category_delete(request, pk=None):
    category = get_object_or_404(CollectionCategory, pk=pk)

    if request.method == 'POST':
        category.delete()
        return HttpResponseRedirect(reverse('admin:category_list'))
    context = {
        'title': 'delete category',
        'category': category
    }
    return render(request, 'adminapp/category_delete.html', context=context)


class ChampionCreateView(AccessMixin, CreateView):
    model = Champion
    template_name = 'adminapp/champion_edit.html'
    success_url = reverse_lazy('admin:champion_list')
    form_class = ChampionEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'create champion'
        context['category'] = 'champions'

        return context


class ChampionListView(AccessMixin, ListView):
    model = Champion
    template_name = 'adminapp/champion_list.html'
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'champions'
        context['category'] = 'champions'

        return context

    def get_queryset(self):
        return Champion.objects.all().order_by('name')


class ChampionUpdateView(AccessMixin, UpdateView):
    model = Champion
    template_name = 'adminapp/champion_edit.html'
    success_url = reverse_lazy('admin:champion_list')
    form_class = ChampionEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'edit champion'
        context['category'] = 'champions'

        return context


class ChampionDeleteView(AccessMixin, DeleteView):
    model = Champion
    template_name = 'adminapp/champion_delete.html'
    success_url = reverse_lazy('admin:champion_list')
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Champion.objects.get(pk=self.kwargs['pk']).name
        context['category'] = 'champions'

        return context


class ChampionDetailView(AccessMixin, DetailView):
    model = Champion
    template_name = 'adminapp/champion.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Champion.objects.get(pk=self.kwargs['pk']).name
        context['category'] = 'champions'

        return context


class SkinCreateView(AccessMixin, CreateView):
    model = Skin
    template_name = 'adminapp/skin_edit.html'
    success_url = reverse_lazy('admin:skin_list')
    form_class = SkinEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'create skin'
        context['category'] = 'skins'

        return context


class SkinListView(AccessMixin, ListView):
    model = Skin
    template_name = 'adminapp/skin_list.html'
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'skins'
        context['category'] = 'skins'

        return context

    def get_queryset(self):
        return Skin.objects.all().order_by('champion__name', 'name')


class SkinUpdateView(AccessMixin, UpdateView):
    model = Skin
    template_name = 'adminapp/skin_edit.html'
    success_url = reverse_lazy('admin:skin_list')
    form_class = SkinEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'edit skin'
        context['category'] = 'skins'

        return context


class SkinDeleteView(AccessMixin, DeleteView):
    model = Skin
    template_name = 'adminapp/skin_delete.html'
    success_url = reverse_lazy('admin:skin_list')
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Skin.objects.get(pk=self.kwargs['pk']).name
        context['category'] = 'skins'

        return context


class SkinDetailView(AccessMixin, DetailView):
    model = Skin
    template_name = 'adminapp/skin.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Skin.objects.get(pk=self.kwargs['pk']).name
        context['category'] = 'skins'

        return context