from pyexpat.errors import messages
from re import search
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView
from .forms import ToDoForm, LoginForm
from .models import ToDo
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from django.shortcuts import render

def minha_view(request):
    return render(request, 'base.html', {'usuario': request.user.username})

@login_required
def list_view(request):
    if request.user.is_staff:  
        todos = ToDo.objects.all()  
    else:
        todos = ToDo.objects.filter(user = request.user)  
    
    return render(request, 'to_do_list.html', {'todos': todos})

    


class CreateToDo(CreateView):
    template_name = "to_do_create.html"
    model = ToDo
    form_class = ToDoForm

    def get_success_url(self):
        return reverse_lazy("to_do_list")
    def form_valid(self, form):
        # Associa o usuário logado ao campo 'user' (supondo que exista um campo user no modelo ToDo)
        form.instance.user = self.request.user
        return super().form_valid(form)
    

  
class UpdateToDo(LoginRequiredMixin, UpdateView):
    template_name = "to_do_uptade.html"
    model = ToDo
    fields = ['task_name', 'task_start', 'task_end']
        
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Verifique se o usuário logado é o dono do objeto
        if obj.user != self.request.user:
            # Caso contrário, você pode redirecionar ou lançar um erro
            raise PermissionDenied("Você não tem permissão para editar essa tarefa.")
        return obj

    def get_success_url(self):
        return reverse_lazy("to_do_list")
@login_required
def delete_view(request, pk):
    obj=get_object_or_404(ToDo, pk=pk)
    # Verifique se o usuário logado é o dono do ToDo
    if obj.user != request.user:
        # Levanta a exceção PermissionDenied caso o usuário não seja o proprietário
        raise PermissionDenied("Você não tem permissão para deletar essa tarefa.")
    if request.method=='POST':
        obj.is_active = False
        obj.save()
        return redirect('to_do_list')
    return render(request, 'to_do_delete.html', {'object': obj})
    
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
        
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  # Realiza o login
                return redirect('home')  # Redireciona para a página inicial ou outra página
            else:
                    # Usuário não encontrado ou senha incorreta
                form.add_error(None, 'Usuário ou senha inválidos.')

        else:
            form = LoginForm()

        return render(request, 'login.html', {'form': form})

 
class DetailToDo(DetailView):
    template_name = "to_do_detail.html"
    model = ToDo
   
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Verifique se o usuário logado é o dono do objeto
        if obj.user != self.request.user:
            # Caso contrário, você pode redirecionar ou lançar um erro
            raise PermissionDenied("Você não tem permissão para editar essa tarefa.")
        return obj