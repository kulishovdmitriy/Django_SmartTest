from rest_framework import serializers

from smart_test.models import Test


class TestSerializer(serializers.ModelSerializer):

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
