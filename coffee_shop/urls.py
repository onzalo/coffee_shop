from django.urls import path

from transactions.api import api

urlpatterns = [
    path("api/", api.urls),
]
