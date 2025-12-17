from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.views.generic import CreateView, View
from django.contrib.auth.views import LoginView as AuthLoginView
from django.urls import reverse, reverse_lazy
from .forms import EditarPerfilForm, RegistroForm, CustomPasswordChangeForm
from .models import Usuario
from apps.posts.models import Post 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView, FormView
from django.contrib.auth.decorators import login_required

# ============== VISTAS DE AUTENTICACIÓN ==============

class RegistrarUsuario(CreateView):
    model = Usuario
    form_class = RegistroForm
    template_name = 'usuarios/registrar.html'
    success_url = reverse_lazy('index')

class LoginView(AuthLoginView):
    template_name = 'usuarios/login.html'
    
    def form_valid(self, form):
        messages.success(self.request, f'¡Bienvenido {form.get_user().username}!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Usuario o contraseña incorrectos.')
        return super().form_invalid(form)

class CerrarSesionView(View):
    def get(self, request):
        logout(request)
        messages.success(request, '¡Has cerrado sesión exitosamente!')
        return redirect('index')

# ============== VISTAS DE PERFIL - VERSIÓN CLASE ==============

class PerfilUsuario(LoginRequiredMixin, View):
    template_name = 'usuarios/perfil.html'
    
    def get(self, request, *args, **kwargs):
        usuario = request.user
        form = EditarPerfilForm(instance=usuario)
        
        # Contar publicaciones
        try:
            posts_count = Post.objects.filter(autor=request.user).count()
        except:
            posts_count = 0
        
        context = {
            'usuario': usuario,  # ¡IMPORTANTE! Usa 'usuario' no 'user'
            'form': form,  # Añade el formulario al contexto
            'posts_count': posts_count,
            'comentarios_count': 0,  # Ajusta según tu modelo de comentarios
        }
        return render(request, self.template_name, context)


# ============== VISTAS DE EDICIÓN ==============

class EditarPerfil(LoginRequiredMixin, UpdateView):
    form_class = EditarPerfilForm
    template_name = 'usuarios/editar_perfil.html'
    success_url = reverse_lazy('usuarios:perfil')
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, '¡Perfil actualizado correctamente!')
        return response  # No redirijas a otra página, usa success_url

class CambiarPassword(LoginRequiredMixin, FormView):
    form_class = CustomPasswordChangeForm
    template_name = 'usuarios/cambiar_password.html'
    success_url = reverse_lazy('usuarios:perfil')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)
        messages.success(self.request, '¡Contraseña actualizada exitosamente!')
        return super().form_valid(form)