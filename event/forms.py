from django import forms
from django.contrib.auth.forms import UserCreationForm

from event.models import Runner, Event, Registration, Distance


class RunnerCreationForm(UserCreationForm):
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Date of birth",
    )

    class Meta(UserCreationForm.Meta):
        model = Runner
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "date_of_birth",
            "city",
            "gender",
            "phone_number",
        )
        widgets = {
            "distances": forms.CheckboxSelectMultiple(),
        }


class RunnerUpdateForm(forms.ModelForm):

    new_password = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
        label="New password",
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
        label="Confirm password",
    )

    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Date of birth",
    )

    class Meta:
        model = Runner
        fields = [
            "username",
            "first_name",
            "last_name",
            "date_of_birth",
            "city",
            "gender",
            "phone_number",
        ]

    def clean(self) -> dict[str]:
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password:
            if new_password != confirm_password:
                raise forms.ValidationError("Passwords do not match!")

        return cleaned_data

    def save(self, commit: bool = True) -> dict[str]:
        runner = super().save(commit=False)
        new_password = self.cleaned_data.get("new_password")
        if new_password:
            runner.set_password(new_password)
        if commit:
            runner.save()
        return runner


class RegistrationCreationForm(forms.ModelForm):
    def __init__(self, *args: tuple, **kwargs: dict) -> None:
        event_id = kwargs.pop("event_id", None)
        super().__init__(*args, **kwargs)

        if event_id:
            try:
                event = Event.objects.get(id=event_id)
                self.fields["distances"].queryset = Distance.objects.filter(
                    id__in=event.distances.values_list("id", flat=True)
                )
            except Event.DoesNotExist:
                self.fields["distances"].queryset = Distance.objects.none()

    class Meta:
        model = Registration
        fields = ["distances"]
        widgets = {
            "distances": forms.CheckboxSelectMultiple(),
        }


class EventCreationForm(forms.ModelForm):
    start_datetime = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
        label="Start date and time",
    )

    location = forms.CharField(
        label="City, street, starting point",
    )
    distances = forms.ModelMultipleChoiceField(
        queryset=Distance.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Distances",
    )

    class Meta:
        model = Event
        fields = [
            "name",
            "start_datetime",
            "location",
            "distances",
            "description",
            "event_type",
            "organiser",
            "is_active",
        ]


class EventSearchForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Name"}),
    )
    location = forms.CharField(
        max_length=100,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Location"}),
    )


class RegistrationForm(forms.ModelForm):
    distances = forms.ModelChoiceField(
        queryset=Distance.objects.all(), widget=forms.RadioSelect
    )

    def __init__(self, *args: tuple, **kwargs: dict) -> None:
        event_id = kwargs.pop("event_id", None)
        super().__init__(*args, **kwargs)
        if event_id:
            event = Event.objects.get(id=event_id)
            self.fields["distances"].queryset = event.distances.all()

    class Meta:
        model = Registration
        fields = [
            "distances",
        ]
