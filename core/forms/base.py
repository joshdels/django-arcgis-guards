from django import forms

from .widgets import (
    CalciteDateWidget,
    CalciteInputWidget,
    CalciteNumberWidget,
    CalciteSelectWidget,
    CalciteTextareaWidget,
    CalciteCheckboxWidget,
)


class CalciteModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            attrs = field.widget.attrs.copy()

            if field.widget.attrs.get("status"):
                attrs["status"] = field.widget.attrs["status"]

            self.apply_calcite_widget(field, attrs)

    def apply_calcite_widget(self, field, attrs):

        if isinstance(field, forms.BooleanField):
            field.widget = CalciteCheckboxWidget(attrs=attrs)

        elif isinstance(field, forms.ModelChoiceField):
            field.widget = CalciteSelectWidget(
                attrs=attrs,
                choices=field.choices,
            )

        elif isinstance(field, forms.ChoiceField):
            field.widget = CalciteSelectWidget(
                attrs=attrs,
                choices=field.choices,
            )

        elif isinstance(field, forms.DateField):
            field.widget = CalciteDateWidget(attrs=attrs)

        elif isinstance(
            field,
            (
                forms.IntegerField,
                forms.DecimalField,
                forms.FloatField,
            ),
        ):
            field.widget = CalciteNumberWidget(attrs=attrs)

        elif isinstance(field.widget, forms.Textarea):
            field.widget = CalciteTextareaWidget(attrs=attrs)

        else:
            field.widget = CalciteInputWidget(attrs=attrs)
