from django.urls import path

from smart_test.api.views import TestListView, TestListCreateView, TestUpdateDeleteView


app_name = 'api_smart_test'

urlpatterns = [
    path('tests', TestListView.as_view(), name='test_list'),

    path('tests/create', TestListCreateView.as_view(), name='test_create'),

    path('tests/update/<int:pk>', TestUpdateDeleteView.as_view(), name='test_detail'),
]
