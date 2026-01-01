# apps/interactions/urls.py
from .views import (
    ScheduleInspectionView, MyInspectionsListView, ManageInspectionView, # Existing
    SendMessageView, InboxListView, MarkMessageReadView, AnnouncementListView # New
)
from django.urls import path, include

urlpatterns = [
    # ... existing inspection paths ...
    path("schedule/", ScheduleInspectionView.as_view(), name="schedule-inspection"),
    path("my-inspections/", MyInspectionsListView.as_view(), name="my-inspections"),
    path("manage/<uuid:id>/", ManageInspectionView.as_view(), name="manage-inspection"),

    # MESSAGING ROUTES
    path("messages/send/", SendMessageView.as_view(), name="send-message"),
    path("messages/inbox/", InboxListView.as_view(), name="inbox"),
    path("messages/read/<uuid:id>/", MarkMessageReadView.as_view(), name="mark-read"),
    
    # ANNOUNCEMENTS
    path("announcements/", AnnouncementListView.as_view(), name="announcements"),
]