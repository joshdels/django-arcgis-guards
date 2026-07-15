from django import forms

from .widgets import (
    CalciteDateWidget,
    CalciteInputWidget,
    CalciteNumberWidget,
    CalciteSelectWidget,
    CalciteTextareaWidget,
)


class CalciteModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            attrs = field.widget.attrs.copy()

            # Mark invalid fields for Calcite
            if name in self.errors:
                attrs["status"] = "invalid"

            # ModelChoiceField (ForeignKey)
            if isinstance(field, forms.ModelChoiceField):
                field.widget = CalciteSelectWidget(
                    attrs=attrs,
                    choices=field.widget.choices,
                )

            # ChoiceField
            elif isinstance(field, forms.ChoiceField):
                field.widget = CalciteSelectWidget(
                    attrs=attrs,
                    choices=field.widget.choices,
                )

            # DateField
            elif isinstance(field, forms.DateField):
                field.widget = CalciteDateWidget(attrs=attrs)

            # IntegerField, DecimalField, FloatField
            elif isinstance(
                field,
                (
                    forms.IntegerField,
                    forms.DecimalField,
                    forms.FloatField,
                ),
            ):
                field.widget = CalciteNumberWidget(attrs=attrs)

            # Textarea
            elif isinstance(field.widget, forms.Textarea):
                field.widget = CalciteTextareaWidget(attrs=attrs)

            # Everything else (CharField, EmailField, URLField, etc.)
            else:
                field.widget = CalciteInputWidget(attrs=attrs)
