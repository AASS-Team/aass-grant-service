from django.urls import path

from . import views

urlpatterns = [
    path("", views.GrantsList.as_view()),
    path("<uuid:id>", views.GrantDetail.as_view()),
]
