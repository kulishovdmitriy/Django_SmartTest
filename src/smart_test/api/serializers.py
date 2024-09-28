from rest_framework import serializers

from smart_test.models import Test


class TestSerializer(serializers.ModelSerializer):
    """
        Serializer class for the Test model.

        This class provides serialization for the Test model,
        including fields for 'id', 'topic', 'title', 'description',
        'level', and 'image'.
    """

    class Meta:
        model = Test
        fields = (
            'id',
            'topic',
            'title',
            'description',
            'level',
            'image'
        )
