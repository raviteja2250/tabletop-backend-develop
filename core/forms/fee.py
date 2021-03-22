"""
    forms/fee.py: Customize the form for fees in admin
"""

from django import forms

from core.models import GSTFee


class FeeFormSet(forms.models.BaseInlineFormSet):
    """ Form for normal fees """

    def get_queryset(self):
        qs = super().get_queryset()
        qs = list(qs)
        return [element for element in qs if not element.is_gst]


class GSTFeeFormSet(forms.models.BaseInlineFormSet):
    """ Formset for GST fees """

    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs.update({'brand': self.instance})
        return kwargs

    def get_queryset(self):
        qs = super().get_queryset()
        qs = list(qs)
        return [element for element in qs if element.is_gst]


class GSTFeeForm(forms.ModelForm):
    """ Form for GST fee """
    is_actived = forms.BooleanField(
        label='Is Actived',
        required=False
    )

    class Meta:
        model = GSTFee
        fields = ('value',)

    def __init__(self, *args, **kwargs):
        self.brand = kwargs.pop('brand')
        super().__init__(*args, **kwargs)

        # Check if the GST of this brand existed or not
        instance = GSTFee.objects.filter(is_gst=True, brand=self.brand).first()
        if instance:
            self.instance = instance
            self.initial['is_actived'] = True
        else:
            self.initial['is_actived'] = False

    def save(self, commit=True):
        is_actived = self.cleaned_data['is_actived']
        if is_actived:
            return super().save(True)

        if self.instance and self.instance.pk:
            self.instance.delete()

        return self.instance
