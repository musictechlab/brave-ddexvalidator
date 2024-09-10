from django.urls import path

from . import views

urlpatterns = [
    path("", views.upload_and_validate_xml, name="upload_xml"),
]
