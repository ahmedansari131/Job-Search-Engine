from django.urls import path
from .views import Testing, JobSearchView

urlpatterns = [
    path("test/", Testing.as_view(), name="testing"),
    path("search-job/", JobSearchView.as_view(), name="search_jobs"),
]
