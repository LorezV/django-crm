from . import models
from django import forms
from django.contrib.auth.forms import AuthenticationForm


class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = '__all__'
        exclude = ['closing_date', 'master']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['working_date'].widget.attrs['type'] = 'datetime-local'


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = '__all__'
        exclude = ['closing_date', 'amount',
                   'master_comment', 'order_status', 'master', 'master_request']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['first_name', 'last_name', 'email']

    def as_div(self):
        return self._html_output(
            normal_row=u'<div>%(label)s <div%(html_class_attr)s>%(field)s %(help_text)s %(errors)s</div></div>',
            error_row=u'<div class="error">%s</div>',
            row_ender='</div>',
            help_text_html=u'<div class="hefp-text">%s</div>',
            errors_on_separate_row=False,)


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = models.User
        fields = ['username', 'password']


class OrdersFilterForm(forms.Form):
    status_choice = list(models.Order.StatusChoice)
    status_choice.append(('', 'Все'))
    type_choice = list(models.Order.TypeChoice)
    type_choice.append(('', 'Любой'))

    city = forms.CharField(max_length=128, label='Город', required=False)
    order_type = forms.ChoiceField(
        required=False,
        choices=type_choice,
        label='Тип',
        initial=''
    )
    order_status = forms.ChoiceField(
        required=False,
        choices=status_choice,
        label='Статус',
        initial=''
    )

    min_amount = forms.IntegerField(label='От', required=False)
    max_amount = forms.IntegerField(label='До', required=False)


class TelegramProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = models.TelegramProfile
        fields = '__all__'
        exclude = ['telegram_chat_id', 'telegram_username']