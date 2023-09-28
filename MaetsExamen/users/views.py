from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Genero, LugarVisita, Equipamiento, Persona, Donation
from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm, GeneroForm, LugarVisitaForm, PersonaForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.conf import settings
from django.urls import reverse

import paypalrestsdk


def donate(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        amount = request.POST.get('amount')

        donation = Donation(name=name, email=email, amount=amount)
        donation.save()

        paypalrestsdk.configure({
            'mode': 'sandbox',  # Cambia a 'live' en producción
            'client_id': settings.PAYPAL_CLIENT_ID,
            'client_secret': settings.PAYPAL_CLIENT_SECRET
        })

        payment = paypalrestsdk.Payment({
            'intent': 'sale',
            'payer': {'payment_method': 'paypal'},
            'redirect_urls': {
                'return_url': request.build_absolute_uri(reverse('payment_done')),
                'cancel_url': request.build_absolute_uri(reverse('payment_cancelled'))
            },
            'transactions': [{
                'amount': {'total': str(amount), 'currency': 'USD'},
                'description': 'Donation'
            }]
        })

        if payment.create():
            request.session['payment_id'] = payment.id
            for link in payment.links:
                if link.method == 'REDIRECT':
                    redirect_url = str(link.href)
                    return redirect(redirect_url)
        else:
            messages.error(request, 'Error al procesar el pago: %s' % payment.error)

    return render(request, 'donation/donation.html')

def payment_done(request):
    payment_id = request.session.get('payment_id')
    payment = paypalrestsdk.Payment.find(payment_id)
    if payment.execute({'payer_id': request.GET.get('PayerID')}):
        messages.success(request, 'Pago exitoso. ¡Gracias por tu donación!')
    else:
        messages.error(request, 'Error al ejecutar el pago: %s' % payment.error)
    return redirect('donate')

def payment_cancelled(request):
    messages.info(request, 'El pago ha sido cancelado.')
    return redirect('donate')

def donation_list(request):
    donations = Donation.objects.all()
    return render(request, 'admin/donation_list.html', {'donations': donations})

def home(request):
    return render(request, 'core/index.html')


def donde_ir(request):
    return render(request, 'core/donde.html')


class TemporadasAPI(View):
    def get(self, request, lugar_id):


        lugar = LugarVisita.objects.get(id=lugar_id)
        data = {
            'valor_temporada_alta': lugar.valor_temporada_alta,
            'valor_temporada_baja': lugar.valor_temporada_baja,
        }

        return JsonResponse(data)

def listar_lugares(request):
    lugares = LugarVisita.objects.all()
    return render(request, 'core/formulario.html', {'lugares': lugares})

def detalles_lugar(request, pk):
    lugar = get_object_or_404(LugarVisita, pk=pk)
    return render(request, 'core/formulario.html', {'lugar': lugar})


class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to='/')

        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-home')


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})


def crud_generos(request):
    generos = Genero.objects.all()
    context = {'generos': generos}
    print("enviando los datos generos_list")
    return render(request, "genero/generos_list.html", context)


def generosAdd(request):
    print("estoy en controlador generosAdd...")
    context={}
    
    if request.method == "POST":
        print("controlador es un post...")
        form = GeneroForm(request.POST)
        if form.is_valid:
            print("estoy en agregar, is_valid")
            form.save()
            
            #limpiar el form
            
            
            form = GeneroForm()
            
            context = {'mensaje': "Ok, datos grabados...", "form":form}
            return render(request, "genero/generos_add.html",context)
    else:
        form = GeneroForm()
        context = {'form':form}
        return render(request, 'genero/generos_add.html', context)

def generos_del(request, pk):
    mensajes=[]
    errores=[]
    generos = Genero.objects.all()
    try:
        genero=Genero.objects.get(id_genero=pk)
        context={}
        if genero:
            genero.delete()
            mensajes.append("Bien, datos eliminados...")
            context = {'generos': generos, 'mensajes': mensajes, 'errores':errores}
            return render(request, 'genero/generos_list.html', context)
    except:
        print("Error, id no existe...")
        generos = Genero.objects.all()
        mensaje="error, id no existe"
        context={'mensaje':mensaje, 'generos':generos}
        return render(request, 'genero/generos_list.html', context)


def generos_edit(request, pk):
    try:
        genero=Genero.objects.get(id_genero=pk)
        context={}
        if genero:
            print("Edit, encontro el género...")
            if request.method == 'POST':
                print("edit es un post")
                form = GeneroForm(request.POST, intance=genero)
                form.save()
                mensaje="Bien, datos actualizados..."
                print(mensaje)
                context = {'generos': generos, 'form': form, 'mensaje':mensaje}
                return render(request, 'genero/generos_edit.html', context)
    except:
        print("Error, id no existe...")
        generos = Genero.objects.all()
        mensaje="error, id no existe"
        context={'mensaje':mensaje, 'generos':generos}
        return render(request, 'genero/generos_list.html', context)






def index(request):
    equipamientos = Equipamiento.objects.all()
    context = {
        'equipamientos': equipamientos
    }
    return render(request, 'equipamiento/index.html', context)

def create(request):
    print(request.POST)
    equipamiento = request.GET['equipamiento']
    precio = request.GET['precio']
    cantidad = request.GET['cantidad']
    equipamiento_details = Equipamiento(equipamiento=equipamiento, precio=precio, cantidad=cantidad)
    equipamiento_details.save()
    return redirect('/')


def add_equipment(request):
    return render(request, 'equipamiento/add_equipment.html')



def delete(request, id):
    equipamiento = Equipamiento.objects.get(pk=id)
    equipamiento.delete()
    return redirect('/')

def edit(request, id):
    equipamientos = Equipamiento.objects.get(pk=id)
    context = {
        'equipamiento': equipamientos
    }
    return render(request, 'equipamiento/edit.html', context)


def update(request, id):
    equipamientos = Equipamiento.objects.get(pk=id)
    equipamientos.equipamiento = request.GET['equipamiento']
    equipamientos.precio = request.GET['precio']
    equipamientos.cantidad = request.GET['cantidad']
    equipamientos.save()
    return redirect('/')

def guardar_formulario(request):
    if request.method == 'POST':
        rut = request.POST.get('rut')
        primer_nombre = request.POST.get('pnombre')
        primer_apellido = request.POST.get('papellido')
        segundo_apellido = request.POST.get('sapellido')
        lugar_visita_id = request.POST.get('lvisita')

        persona = Persona(rut=rut, primer_nombre=primer_nombre, primer_apellido=primer_apellido, segundo_apellido=segundo_apellido, lugar_visita_id=lugar_visita_id)
        persona.save()

        return redirect('/') 
    return render(request, 'formulario.html')



def superuser_check(user):
    return user.is_superuser

@user_passes_test(superuser_check)
@login_required
def LugarVisitaAdminView(request):
    lugares = LugarVisita.objects.all()
    return render(request, 'admin/lugarvisita_admin.html', {'lugares': lugares})

@user_passes_test(superuser_check)
@login_required
def LugarVisitaCreateView(request):
    if request.method == 'POST':
        form = LugarVisitaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lugarvisita_admin')
    else:
        form = LugarVisitaForm()
    return render(request, 'admin/lugarvisita_form.html', {'form': form})

@user_passes_test(superuser_check)
@login_required
def LugarVisitaUpdateView(request, pk):
    lugar = get_object_or_404(LugarVisita, pk=pk)
    if request.method == 'POST':
        form = LugarVisitaForm(request.POST, instance=lugar)
        if form.is_valid():
            form.save()
            return redirect('lugarvisita_admin')
    else:
        form = LugarVisitaForm(instance=lugar)
    return render(request, 'admin/lugarvisita_form.html', {'form': form})

@user_passes_test(superuser_check)
@login_required
def LugarVisitaDeleteView(request, pk):
    lugar = get_object_or_404(LugarVisita, pk=pk)
    if request.method == 'POST':
        lugar.delete()
        return redirect('lugarvisita_admin')
    return render(request, 'admin/lugarvisita_confirm_delete.html', {'lugar': lugar})

@user_passes_test(superuser_check)
@login_required
def crud(request):
    return render(request, 'admin/crud.html')

@user_passes_test(superuser_check)
@login_required
def persona_admin(request):
    personas = Persona.objects.all()
    return render(request, 'admin/persona_admin.html', {'personas': personas})

@user_passes_test(superuser_check)
@login_required
def persona_add(request):
    if request.method == 'POST':
        form = PersonaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('persona_admin')
    else:
        form = PersonaForm()
    return render(request, 'admin/persona_form.html', {'form': form})

@user_passes_test(superuser_check)
@login_required
def persona_edit(request, pk):
    persona = get_object_or_404(Persona, pk=pk)
    if request.method == 'POST':
        form = PersonaForm(request.POST, instance=persona)
        if form.is_valid():
            form.save()
            return redirect('persona_admin')
    else:
        form = PersonaForm(instance=persona)
    return render(request, 'admin/persona_form.html', {'form': form})

@user_passes_test(superuser_check)
@login_required
def persona_delete(request, pk):
    persona = get_object_or_404(Persona, pk=pk)
    if request.method == 'POST':
        persona.delete()
        return redirect('persona_admin')
    return render(request, 'admin/persona_confirm_delete.html', {'persona': persona})

@user_passes_test(superuser_check)
@login_required
def crud(request):
    return render(request, 'admin/crud.html')