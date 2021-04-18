from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import ListView, CreateView, UpdateView, View, DeleteView, DetailView
from django.contrib.auth.views import LoginView, LogoutView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from . import models, forms
# Create your views here.

def get_all_amount():
    amount = 0
    for order in models.Order.objects.all():
        t = order.amount
        if t:
            amount += t
    return amount

def get_all_clear_amount():
    amount = 0
    for order in models.Order.objects.all():
        t = order.clear_amount
        if t:
            amount += t
    return amount

def index(request):
    if not request.user.is_authenticated:
        return redirect(reverse_lazy('login'))
    context = {
        'orders': models.Order.objects.all(),
        'clear_amount': get_all_clear_amount(),
        'amount': get_all_amount(),
    }
    return render(request, 'index.html', context=context)


class OrderDeleteView(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    redirect_field_name = 'login'
    model = models.Order
    template_name = 'order_delete.html'
    success_url = reverse_lazy('orders')


class OrderUpdateView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    redirect_field_name = 'login'
    template_name = 'order_detail.html'
    model = models.Order
    form_class = forms.OrderUpdateForm

    def form_valid(self, form):
        return super().form_valid(form)


class OrderCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    redirect_field_name = 'login'
    template_name = 'order_create.html'
    model = models.Order
    form_class = forms.OrderCreateForm


class OrderListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    redirect_field_name = 'login'
    filter_form_class = forms.OrdersFilterForm
    model = models.Order
    template_name = 'order_list.html'
    ordering = ['-create_date']
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.filter_form_class
        context['amount'] = self.get_all_amount()
        context['clear_amount'] = self.get_all_clear_amount()
        return context

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset, filter_form = self.do_filter(self.request, queryset)
        self.filter_form_class = filter_form
        return queryset

    def do_filter(self, request, queryset):
        filter_form = forms.OrdersFilterForm(request.GET)
        if filter_form.is_valid():
            if filter_form.cleaned_data['min_amount']:
                queryset = queryset.filter(
                    amount__gte=filter_form.cleaned_data['min_amount'])
            if filter_form.cleaned_data['max_amount']:
                queryset = queryset.filter(
                    amount__lte=filter_form.cleaned_data['max_amount'])
            if filter_form.cleaned_data['city']:
                queryset = queryset.filter(
                    client_city=filter_form.cleaned_data['city'])
            if filter_form.cleaned_data['order_type'] and filter_form.cleaned_data['order_type'] != '':
                queryset = queryset.filter(
                    order_type=filter_form.cleaned_data['order_type'])
            if filter_form.cleaned_data['order_status']:
                queryset = queryset.filter(
                    order_status=filter_form.cleaned_data['order_status'])
        return queryset, filter_form

    def get_all_amount(self):
        amount = 0
        for order in self.get_queryset():
            t = order.amount
            if t:
                amount += t
        return amount

    def get_all_clear_amount(self):
        amount = 0
        for order in self.get_queryset():
            t = order.clear_amount
            if t:
                amount += t
        return amount


class UserProfileView(UpdateView, LoginRequiredMixin):
    login_url = reverse_lazy('login')
    redirect_field_name = 'login'
    model = models.User
    form_class = forms.UserProfileForm
    template_name = 'profile_edit.html'
    success_url = reverse_lazy('index')


class UserLoginView(LoginView):
    authentication_form = forms.UserLoginForm
    template_name = 'login_form.html'
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("login")


class MasterListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    redirect_field_name = 'login'
    ordering = ['-is_master']
    model = models.TelegramProfile
    template_name = 'master_list.html'


class MasterUpdateView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    redirect_field_name = 'login'
    template_name = 'master_detail.html'
    model = models.TelegramProfile
    form_class = forms.TelegramProfileUpdateForm

    def form_valid(self, form):
        return super().form_valid(form)


class MasterDeleteView(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    redirect_field_name = 'login'
    model = models.TelegramProfile
    template_name = 'master_delete.html'
    success_url = reverse_lazy('masters')
