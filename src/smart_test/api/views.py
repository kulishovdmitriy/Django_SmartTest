from rest_framework import generics
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

from smart_test.api.serializers import TestSerializer
from smart_test.models import Test


class TestListView(generics.ListAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    throttle_classes = [UserRateThrottle, AnonRateThrottle]


class TestListCreateView(generics.ListCreateAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    throttle_classes = [UserRateThrottle, AnonRateThrottle]


class TestUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
