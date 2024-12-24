from rest_framework import serializers

from polls.models import Choice, Question


class ChoiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Choice
        fields = ["url", "id", "choice_text", "votes"]


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True, source="choice_set")

    class Meta:
        model = Question
        fields = ["url", "question_text", "pub_date", "choices"]
