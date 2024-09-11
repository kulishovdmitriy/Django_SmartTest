from django.urls import path

from smart_test.views import TestListView, TestDetailView, TestStartView, TestQuestionView, TestCreateView, \
    TestUpdateView

app_name = "tests"

urlpatterns = [

    path('', TestListView.as_view(), name='list'),

    path('<int:id>/', TestDetailView.as_view(), name='details'),

    path('<int:id>/start/', TestStartView.as_view(), name='start'),

    path('<int:id>/next/', TestQuestionView.as_view(), name='next'),

    path('create/', TestCreateView.as_view(), name='test_create'),

    path('<int:id>/edit/', TestUpdateView.as_view(), name='test_edit'),

]
