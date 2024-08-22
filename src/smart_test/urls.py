from django.urls import path

from smart_test.views import TestListView, TestDetailView, TestStartView, TestQuestionView

app_name = "tests"

urlpatterns = [
    path('', TestListView.as_view(), name='list'),
    path('<int:id>/', TestDetailView.as_view(), name='details'),
    path('<int:id>/start/', TestStartView.as_view(), name='start'),
    path('<int:id>/question/<int:order_number>', TestQuestionView.as_view(), name='question')
]