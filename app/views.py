from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import ListView, CreateView, UpdateView, View, DeleteView, DetailView
from django.contrib.auth.views import LoginView, LogoutView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from . import models, forms
import humanize
# Create your views here.

def get_sum_temp_cash():
    queryset = models.Order.objects.filter(order_status='R').exclude(cashed=True).exclude(master=None)
    t = 0
    for order in queryset:
        t += order.get_clear_amount
    return t

def get_sum_cash():
    queryset = models.Order.objects.filter(order_status='R').filter(cashed=True).exclude(master=None)
    t = 0
    for order in queryset:
        t += order.get_cashed_value
    return t


def index(request):
    if not request.user.is_authenticated:
        return redirect(reverse_lazy('login'))
    
    if request.method == 'GET':
        context = {
            'uncashed_orders': models.Order.objects.filter(order_status='R').filter(cashed=False).exclude(master=None).order_by('-closing_date'),
            'cashed_orders': models.Order.objects.filter(order_status='R').filter(cashed=True).exclude(master=None).order_by('-closing_date'),
            'temp_cash': get_sum_temp_cash(),
            'cash': get_sum_cash(),
        }
        return render(request, 'index.html', context=context)
    
    if request.method == 'POST':
        for id in request.POST.getlist('do_cash'):
            order = models.Order.objects.filter(id=id).first()
            if order:
                order.cashed = True
                order.save()
        return redirect('/')


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
    
    def get_all_amount(self):
        amount = 0
        queryset = self.get_queryset()
        for order in queryset.exclude(order_status='C'):
            t = order.get_amount
            if t:
                amount += t
        return amount

    def get_all_clear_amount(self):
        amount = 0
        queryset = self.get_queryset()
        for order in queryset.exclude(order_status='C'):
            t = order.get_cashed_value
            if t:
                amount += t
        return amount

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
