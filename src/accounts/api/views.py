from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from accounts.models import User
from accounts.api.serializers import RegistrationSerializer, AccountSerializer


class RegistrationView(generics.CreateAPIView):
    """
    class RegistrationView(generics.CreateAPIView):
    A view that handles the registration of new users.

    queryset: The complete collection of User instances.
    serializer_class: The serializer class used for validation and deserialization of input data.

    def create(self, request, *args, **kwargs):
    Handles the creation of a new user instance.

    Parameters:
    request : HTTP request object containing user registration data.
    *args : Additional positional arguments.
    **kwargs : Additional keyword arguments.

    Returns:
    Response object with serialized user data and HTTP 201 status code if creation is successful.
    """

    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AccountView(generics.ListAPIView):
    """

    This view provides a read-only endpoint for listing user accounts.

    Attributes:
        queryset: The queryset containing all User instances to be serialized.
        serializer_class: The serializer class to be used for serializing the User instances.
    """

    queryset = User.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [AllowAny]
