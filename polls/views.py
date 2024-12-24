from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View, generic

from polls.models import Choice, Question


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "questions"

    def get_queryset(self):
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(View):
    def get(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        return render(request, "polls/detail.html", {"question": question})

    def post(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
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
