from django.forms import modelformset_factory

from apps.operations.models import Assignment
from core.forms.base import CalciteModelForm


class AssignmentForm(CalciteModelForm):
    class Meta:
        model = Assignment
        fields = [
            "deployment",
            "guard",
            "start_date",
            "end_date",
        ]


class DeploymentAssignmentForm(CalciteModelForm):
    class Meta:
        model = Assignment
        fields = [
            "guard",
            "start_date",
            "end_date",
        ]


class AssignmentUpdateForm(CalciteModelForm):
    class Meta:
        model = Assignment
        fields = [
            "deployment",
            "guard",
            "start_date",
            "end_date",
            "status",
        ]


AssignmentFormSet = modelformset_factory(
    Assignment,
    form=AssignmentForm,
    extra=1,
    can_delete=False,
)


DeploymentAssignmentFormSet = modelformset_factory(
    Assignment,
    form=DeploymentAssignmentForm,
    extra=1,
    can_delete=False,
)
