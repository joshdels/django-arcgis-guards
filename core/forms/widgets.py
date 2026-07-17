from django import forms


class CalciteInputWidget(forms.TextInput):
    template_name = "widgets/calcite/input.html"


class CalciteTextareaWidget(forms.Textarea):
    template_name = "widgets/calcite/textarea.html"


class CalciteSelectWidget(forms.Select):
    template_name = "widgets/calcite/select.html"


class CalciteNumberWidget(forms.NumberInput):
    template_name = "widgets/calcite/number.html"


class CalciteTelephoneWidget(forms.TextInput):
    template_name = "widgets/calcite/tel.html"


class CalciteCheckboxWidget(forms.CheckboxInput):
    template_name = "widgets/calcite/checkbox.html"


class CalciteDateWidget(forms.DateInput):
    template_name = "widgets/calcite/date.html"

    def __init__(self, attrs=None):
        attrs = attrs or {}
        attrs["type"] = "date"
        super().__init__(attrs)
