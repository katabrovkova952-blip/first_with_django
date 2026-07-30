from rest_framework import serializers


class AssistantAskSerializer(serializers.Serializer):
    question = serializers.CharField(max_length=2000)
    book_id = serializers.IntegerField(required=False)