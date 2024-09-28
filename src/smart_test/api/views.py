from rest_framework import generics
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

from smart_test.api.serializers import TestSerializer
from smart_test.models import Test


class TestListView(generics.ListAPIView):
    """
        Class providing a read-only endpoint that lists Test objects.

        Attributes:
            queryset (QuerySet): QuerySet that retrieves all Test objects.
            serializer_class (Serializer): Serializer class used for the Test objects.
            throttle_classes (list): List of throttle classes applied to the view, including UserRateThrottle and AnonRateThrottle.
    """

    queryset = Test.objects.all()
    serializer_class = TestSerializer
    throttle_classes = [UserRateThrottle, AnonRateThrottle]


class TestListCreateView(generics.ListCreateAPIView):
    """
        A view that provides both list and create actions for the Test model.

        - **queryset**: Defines the list of objects that the view will operate on. In this case, it retrieves all Test objects from the database.
        - **serializer_class**: Specifies the serializer that will be used to convert Test objects to and from JSON. The TestSerializer will
        handle this conversion.
        - **throttle_classes**: Lists the throttling policies that will be applied to the view. UserRateThrottle limits the rate of requests for
        authenticated users, and AnonRateThrottle does the same for anonymous users.
    """

    queryset = Test.objects.all()
    serializer_class = TestSerializer
    throttle_classes = [UserRateThrottle, AnonRateThrottle]


class TestUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
        Class-based view for retrieving, updating, and deleting Test instances.

        This view handles HTTP GET, PUT, PATCH, and DELETE requests for the Test model, providing
        functionality to retrieve a specific instance, update its details, or delete it. It ensures
        rate limiting for both authenticated and anonymous users.

        Attributes:
            queryset: A QuerySet containing all Test instances.
            serializer_class: The serializer class used for validating and deserializing input, and
                              serializing output.
            throttle_classes: A list of throttling policies that are applied to the view. This includes
                              rate limiting for authenticated users (UserRateThrottle) and anonymous
                              users (AnonRateThrottle).
    """

    queryset = Test.objects.all()
    serializer_class = TestSerializer
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
