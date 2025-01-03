from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import View, generic
from rest_framework import permissions, viewsets

from polls.models import Choice, Question
from polls.serializers import ChoiceSerializer, QuestionSerializer


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "questions"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]


class DetailView(View):
    def get(self, request, question_id):
        question = get_object_or_404(self.get_queryset(), pk=question_id)
        return render(request, "polls/detail.html", {"question": question})

    def post(self, request, question_id):
        question = get_object_or_404(self.get_queryset(), pk=question_id)
        try:
            selected_choice = question.choice_set.get(pk=request.POST["choice"])
        except (KeyError, Choice.DoesNotExist):
            return render(
                request,
                "polls/detail.html",
                {
                    "question": question,
                    "error_message": "Please select a choice first.",
                },
            )
        else:
            selected_choice.votes = F("votes") + 1
            selected_choice.save()
            return HttpResponseRedirect(reverse("polls:detail", args=(question.id,)))

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all().order_by("-pub_date")
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]


class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [permissions.IsAuthenticated]
