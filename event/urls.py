from django.urls import path

from event.views import (
    index,
    EventCreateView,
    EventUpdateView,
    EventDeleteView,
    RunnerDetailView,
    RunnerCreateView,
    RunnerUpdateView,
    RunnerDeleteView,
    RegistrationListView,
    RegistrationCreateView,
)

app_name = 'event'

urlpatterns = [
    path("", index, name="index"),
    path("events/create", EventCreateView.as_view(), name="event_create"),
    path("events/<int:pk>/update", EventUpdateView.as_view(), name="event_update"),
    path("events/<int:pk>/delete", EventDeleteView.as_view(), name="event_delete"),
    path("runners/<int:pk>/detail", RunnerDetailView.as_view(), name="runner_detail"),
    path("runners/create", RunnerCreateView.as_view(), name="runner_create"),
    path("runners/<int:pk>/update", RunnerUpdateView.as_view(), name="runner_update"),
    path("runners/<int:pk>/delete", RunnerDeleteView.as_view(), name="runner_delete"),
    path('registrations/', RegistrationListView.as_view(), name='registration_list'),
    path('registrations/create/<int:event_id>/', RegistrationCreateView.as_view(), name='registration_create'),
]
