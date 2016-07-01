# -*- coding: utf-8 -*-

from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User

from .models import Cliente
from .models import Billetera
from .forms import EditarPerfilForm, ClaveBilleteraForm, CrearBilleteraForm, \
RecargaBilleteraForm, ElegirPlatosForm, TarjetaCreditoForm

from administrador.models import Menu, Plato


@login_required(login_url=reverse_lazy('login'))
def home(request):
    return render(request, 'cliente/home.html', {'user': request.user})


@login_required(login_url=reverse_lazy('login'))
def perfil(request):
    return render(request, 'cliente/perfil.html', {'user': request.user})


@login_required(login_url=reverse_lazy('login'))
def editar_perfil(request):
    inline_formset = inlineformset_factory(
        User, Cliente, fields=('telefono',), can_delete=False)

    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, instance=request.user)
        formset = inline_formset(request.POST, instance=request.user)

        if form.is_valid():
            created_user = form.save(commit=False)
            formset = inline_formset(
                request.POST, instance=created_user)

            if formset.is_valid():
                created_user.save()
                formset.save()
                messages.success(request, '✓ Se actualizaron los datos!')
                return redirect(reverse('perfil_cliente'))
    else:
        form = EditarPerfilForm(instance=request.user)
        formset = inline_formset(instance=request.user)
    return render(
        request,
        'cliente/editar_perfil.html',
        {'user': request.user, 'formset': formset, 'form': form})

@login_required(login_url=reverse_lazy('login'))
def crear_billetera(request):
    if request.method == 'POST':
        form = CrearBilleteraForm(request.POST)
        
        if form.is_valid():
            pin = form.cleaned_data['pin']
            billetera = Billetera.objects.create(
                usuario=request.user, pin=pin)
            messages.success(request, '✓ Se ha creado su billetera')

            return redirect(reverse('home_cliente'))
    else:
        form = CrearBilleteraForm()
    return render(request, 'cliente/crear_billetera.html', {'form': form})

@login_required(login_url=reverse_lazy('login'))
def consultar_saldo(request):
    if request.method == 'POST':
        form = ClaveBilleteraForm(request.POST)
        
        if form.is_valid():
            billetera = request.user.billetera
            
            if form.cleaned_data['pin'] == billetera.pin:
                return render(
                    request,
                    'cliente/consultar_saldo.html',
                    {'billetera': billetera})
            else:
                messages.error(
                    request, 'La contraseña es incorrecta, intente de nuevo.')
                form = ClaveBilleteraForm()
    else:
        form = ClaveBilleteraForm()
    return render(request, 'cliente/consultar_saldo_clave.html', {'form': form})


@login_required(login_url=reverse_lazy('login'))
def recargar_saldo(request):
    if request.method == 'POST':
        form = RecargaBilleteraForm(request.POST)

        if form.is_valid():
            monto = form.cleaned_data['monto']
            billetera = request.user.billetera
            billetera.recargar(monto)
            messages.success(request, '✓ Recarga exitosa: %s Bs.' % monto)
            return render(
                request, 'cliente/home.html', {'billetera': billetera})
            
    else:
        form = RecargaBilleteraForm()
    return render(request, 'cliente/recargar_saldo.html', {'form': form})


@login_required(login_url=reverse_lazy('login'))
def ver_plato(request):
    menu = Menu.objects.get(actual=True)

    return render(request, 'cliente/ver_menu.html', {'menu':menu})

@login_required(login_url=reverse_lazy('login'))
def detalle_plato(request, nombre):
    plato = Plato.objects.get(nombre=nombre)
    return render(request, 'cliente/detalles_plato.html', {'plato':plato})

@login_required(login_url=reverse_lazy('login'))
def elegir_platos(request):
    menu = Menu.objects.get(actual=True)
    queryset = menu.incluye.all()

    if request.method == 'POST':
        form = ElegirPlatosForm(queryset, request.POST)
        if form.is_valid():
            elegidos = []
            monto = 0
            platos = form.cleaned_data['platos']
            for i in platos:
                elegidos.append(i.nombre)
                monto = monto + i.precio 
            

            #messages.success(request, '✓ Se agregaron los platos "%s"' % elegidos)
            return render(request, 'cliente/pagar_pedido.html', {'monto': monto})
    else:
        form = ElegirPlatosForm(queryset)

    return render(
        request,
        'cliente/elegir_platos.html',
        {'form':form, 'user': request.user})

@login_required(login_url=reverse_lazy('login'))
def pagar_pedido(request):
    #platos = Plato.objects.get(nombre=nombre)
    return render(request, 'cliente/pagar_pedido.html')

@login_required(login_url=reverse_lazy('login'))
def tarjeta_credito(request, monto):
    if request.method == 'POST':
        form = TarjetaCreditoForm(request.POST)

        if form.is_valid():
            usuario = User.objects.get(username='admin')
            monto_p = float(monto)
            billetera = Billetera.objects.get(usuario = usuario)
            billetera.recargar(monto_p)
            messages.success(request, '✓ Consumo exitoso: %s Bs.' % monto)
            return render(
                request, 'cliente/home.html', {'billetera': billetera})
            
    else:
        form = TarjetaCreditoForm()
    return render(request, 'cliente/tarjeta_credito.html', {'form': form, 'monto':monto})


@login_required(login_url=reverse_lazy('login'))
def billetera(request, monto):
    if request.method == 'POST':
        form = ClaveBilleteraForm(request.POST)

        if form.is_valid():
            usuario = User.objects.get(username='admin')
            monto_p = float(monto)
            billetera = request.user.billetera
            billetera.consumir(monto_p)
            billetera_admin = Billetera.objects.get(usuario = usuario)
            billetera_admin.recargar(monto_p)
            messages.success(request, '✓ Consumo exitoso: %s Bs.' % monto)
            return render(
                request, 'cliente/home.html', {'billetera': billetera})
            
    else:
        form = ClaveBilleteraForm()
    return render(request, 'cliente/billetera.html', {'form': form, 'monto':monto})


