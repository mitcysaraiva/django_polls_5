from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from polls.models import Question
from django.views.generic import DetailView, ListView, TemplateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.core.exceptions import ValidationError

from django.contrib.auth import get_user_model
User = get_user_model()


from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse

from polls.models import Question, Choice

def ultimas_perguntas(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/perguntas.html', context)

def index(request):
    #return HttpResponse('Olá... seja bem vindo a enquete')
 return render(request, 'home.html')
def sobre(request):
    return HttpResponse('Este é um app de enquete!')

def exibe_questao(request, question_id):
    questao = Question.objects.get(id=question_id)
    return HttpResponse(questao.question_text)
    
#codigo wanderson
def exibe_questao(request, question_id):
    questao = Question.objects.get(id=question_id)
    
    if questao is not None:
        # questao.question_text
        return HttpResponse(questao.question_text)
    
    return HttpResponse('Não existe questão a exibir')


def ultimas_perguntas(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'perguntas_recentes.html', context)

from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

class QuestionCreateView(CreateView):
    model= Question
    fields= ('question_text', 'pub_date')
    success_url = reverse_lazy('index')

class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    template_name = 'polls/question_form.html'
    fields = ('question_text', 'pub_date', )
    success_url = reverse_lazy('polls_list')

    def get_context_data(self, **kwargs):
        context = super(QuestionCreateView, self).get_context_data(**kwargs)
        context['form_title'] = 'Criando uma pergunta'

        question_id = self.kwargs.get('pk')
        choices = Choice.objects.filter(question__pk=question_id) 
        context['question_choices'] = choices

        return context

class QuestionUpdateView(UpdateView):
        model = Question
        template_name = 'polls/question_form.html'
        fields = ('question_text', 'pub_date', )
        success_url = reverse_lazy('polls_list')
        
        def get_context_data(self, **kwargs):
            context = super(QuestionUpdateView, self).get_context_data(**kwargs)
            context['form_title'] = 'Editando a pergunta'

            question_id = self.kwargs.get('pk')
            choices = Choice.objects.filter(question__pk-question_id)
            context['question_choices'] = choices
            
            return context

class QuestionDeleteView(DeleteView):
    model = Question
    template_name = 'polls/question_confirm_delete_form.html'
    success_url = reverse_lazy('polls_all')
    success_message = 'Pergunta excluída com sucesso.'

    def form_valid(self, request, *args, **kwargs):
        form.instance.author = self.request.user
        messages.success(self.request, self.success_message)
        return super(QuestionDeleteView, self).form_valid(request, *args, **kwargs)

class QuestionDetailView(DetailView):
    model = Question
    template_name = 'polls/question_detail.html'
    context_object_name = 'question'

    def get_context_data(self, **kwargs):
        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        votes = Choice.objects.filter(question=context['question']).aggregate(total=Sum('votes')) or 0
        context['total_votes'] = votes.get('total')

        return context

class QuestionListView(ListView):
    model = Question
    template_name = 'polls/question_list.html'
    context_object_name = 'questions'
    paginate_by = 5 # quantidade de itens por página
    ordering = ['-pub_date'] 

class SobreTemplateView(TemplateView):
    template_name = 'polls/sobre.html'

class ChoiceCreateView(CreateView): 
    model = Choice
    template_name = 'polls/choice_form.html'
    fields=('choice_text',)
    success_message = 'Alternativa registrada com sucesso!'

    def dispatch(self, request, *args, **kwargs): 
        self.question = get_object_or_484(Question, pk=self.kwargs.get('pk')) 
        return super (ChoiceCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs): 
        question = get_object_or_484 (Question, pk=self.kwargs.get('pk'))

        context = super (ChoiceCreateView, self).get_context_data(**kwargs) 
        context['form_title'] = f'Alternativa para: {question.question_text}'

        return context

    def form_valid(self, form): 
        form.instance.question = self.question
        messages.success(self.request, self.success_message) 
        return super (ChoiceCreateView, self).form_valid(form)

    def get_success_url(self, *args, **kwargs): 
        question_id = self.kwargs.get('pk')
        return reverse_lazy('poll_edit', kwargs={'pk': question_id})


class ChoiceUpdateView(UpdateView):
    model = Choice
    template_name = 'polls/choice_form.html'
    fields = ('choice_text', )
    success_message = 'Alternativa atualizada com sucesso!'

    def get_context_data(self, **kwargs):
        # question = get_object_or_404 (Question, pk=self.object.question.id) 
        context = super (ChoiceUpdateView, self).get_context_data(**kwargs)
        context['form_title'] = 'Editando alternativa'
        return context

    def form_valid (self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super (ChoiceUpdateView, self).form_valid (request, *args, **kwargs)

    def get_success_url(self, *args, **kwargs):
        question_id = self.object.question.id
        return reverse_lazy('poll_edit', kwargs={'pk': question_id})

class ChoiceDeleteView(LoginRequiredMixin, DeleteView):
    model = Choice
    template_name = 'polls/choice_confirm_delete_form.html'
    success_message = 'Alternativa excluída com sucesso!'

    def form_valid(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message) 
        return super (ChoiceDeleteView, self).form_valid (request, *args, **kwargs)

    def get_success_url(self, *args, **kwargs): 
        question_id = self.object.question.id 
        return reverse_lazy('poll_edit', kwargs={'pk': question_id})
@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        try:
            selected_choice = question.choice_set.get(pk=request.POST["choice"])
        except (KeyError, Choice.DoesNotExist):
            messages.error(request, 'Selecione uma alternativa para votar')
        except (ValidationError) as error:
            messages.error(request, error.message)
        else:
            selected_choice.votes += 1
            selected_choice.save()
            messages.success(request, 'Seu voto foi registrado com sucesso')
            return redirect(reverse_lazy("poll_show", args=(question.id,)))
    
    context = {'question': question}
    return render(request, 'polls/question_detail.html', context)