from django.contrib.auth.models import User
from django.core.urlresolvers import resolve, reverse
from django.http import HttpRequest
from django.test import TestCase
from django.template.loader import render_to_string

from cliente.models import Cliente

from .forms import CrearMenuForm
from .models import Administrador, Ingrediente, Menu, Plato
from .views import crear_menu, detalles_cliente, home, ver_clientes

class PruebasHomeAdmin(TestCase):
    def agregar_cliente(
        self, username, nombre, apellido, ci, email, telefono, sexo,
        fecha_nacimiento
    ):
        user = User.objects.create(
            username=username, password='pw', email=email,
            first_name=nombre, last_name=apellido
        )
        cliente = Cliente.objects.create(
            usuario=user, ci=ci, fecha_nacimiento=fecha_nacimiento,
            sexo=sexo, telefono=telefono,
        )
        user.save()
        cliente.save()
        return user

    def setUp(self):
       user = User.objects.create(username='admin', password='administrador')
       admin = Administrador.objects.create(usuario=user)

    def test_pagina_principal_devuelve_html_correcto(self):
        request = HttpRequest()
        response = home(request)
        expected_html = render_to_string('administrador/home.html', request=request)
        self.assertEqual(response.content.decode(), expected_html)

    def test_home_url_llama_a_vista_home_administrador(self):
        found = resolve(reverse('home_administrador'))
        self.assertEqual(found.func, home)

    def test_ver_clientes_url_llama_a_vista_ver_clientes(self):
        found = resolve(reverse('ver_clientes'))
        self.assertEqual(found.func, ver_clientes)

    def test_pagina_ver_clientes_devuelve_html_correcto(self):
        request = HttpRequest()
        response = ver_clientes(request)
        expected_html = render_to_string(
            'administrador/ver_clientes.html', request=request)
        self.assertEqual(response.content.decode(), expected_html)

    def test_pagina_ver_clientes_muestra_info_clientes_registrados(self):
        cliente1 = self.agregar_cliente(
            'cliente1', 'Uno', 'Cliente', '1', 'cliente1@mail.com',
            '1111-1111111', 'M', '1991-1-1')

        cliente2 = self.agregar_cliente(
            'cliente2', 'Dos', 'Cliente', '2', 'cliente2@mail.com',
            '2222-2222222', 'M', '1992-2-2')

        request = HttpRequest()
        response = ver_clientes(request)

        self.assertIn(cliente1.username, response.content.decode())
        self.assertIn(
            cliente1.date_joined.strftime('%d/%m/%Y'),
            response.content.decode())
        
        self.assertIn(cliente2.username, response.content.decode())
        self.assertIn(
            cliente2.date_joined.strftime('%d/%m/%Y'),
            response.content.decode())

    def test_cliente_x_url_llama_a_vista_detalle_cliente(self):
        found = resolve(reverse('detalles_cliente', args=("cliente",)))
        self.assertEqual(found.func, detalles_cliente)

    def test_pagina_detalle_cliente_devuelve_html_correcto(self):
        request = HttpRequest()
        response = detalles_cliente(request, None)
        expected_html = render_to_string(
            'administrador/detalles_cliente.html', request=request)
        self.assertEqual(response.content.decode(), expected_html)

    def test_pagina_crear_menu_devuelve_html_correcto(self):
        request = HttpRequest()
        response = crear_menu(request)
        form = CrearMenuForm()
        expected_html = render_to_string(
            'administrador/crear_menu.html', {'form': form}, request=request)
        self.assertEqual(response.content.decode(), expected_html)

    def test_crear_menu_url_llama_a_vista_crear_menu(self):
        found = resolve(reverse('crear_menu'))
        self.assertEqual(found.func, crear_menu)

    def test_pagina_crear_menu_puede_guardar_una_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['nombre'] = 'Menu 1'

        response = crear_menu(request)

        self.assertEqual(Menu.objects.count(), 1)
        nuevo_menu = Menu.objects.first()
        self.assertEqual(nuevo_menu.nombre, 'Menu 1')

    def test_crear_menu_redireccion_despues_del_POST(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['nombre'] = 'Menu 1'

        response = crear_menu(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], reverse('home_administrador'))


class IngredienteModelTest(TestCase):
    def test_guardar_y_ver_ingrediente(self):
        ingrediente = Ingrediente(
            nombre='Ingrediente 1', descripcion='Descripción del ingrediente')
        ingrediente.save()

        ingrediente2 = Ingrediente(
            nombre='Ingrediente 2', descripcion='Descripción del ingrediente 2')
        ingrediente2.save()

        saved_ingr = Ingrediente.objects.all()
        self.assertEqual(saved_ingr.count(), 2)

        primer_ingr = saved_ingr[0]
        self.assertEqual(primer_ingr.nombre, 'Ingrediente 1')
        self.assertEqual(primer_ingr.descripcion, 'Descripción del ingrediente')

        segundo_ingr = saved_ingr[1]
        self.assertEqual(segundo_ingr.nombre, 'Ingrediente 2')
        self.assertEqual(segundo_ingr.descripcion, 'Descripción del ingrediente 2')


class PlatoModelTest(TestCase):
    def test_guardar_y_ver_plato(self):
        i1 = Ingrediente(nombre='i1', descripcion='d1')
        i1.save()

        i2 = Ingrediente(nombre='i2', descripcion='d2')
        i2.save()

        plato1 = Plato(
            nombre='Plato 1', descripcion = 'Descripción del plato1', precio = 1)
        plato1.save()
        plato1.contiene.add('i1', 'i2')

        plato2 = Plato(
            nombre='Plato 2', descripcion = 'Descripción del plato2', precio = 2)
        plato2.save()
        plato2.contiene.add('i2')

        platos = Plato.objects.all()
        self.assertEqual(platos.count(), 2)

        first_plato = platos[0]
        second_plato = platos[1]

        self.assertEqual(first_plato.nombre, 'Plato 1')
        self.assertEqual(first_plato.descripcion, 'Descripción del plato1')
        self.assertEqual(first_plato.precio, 1)
        self.assertEqual(first_plato.contiene.count(), 2)
        self.assertEqual(first_plato.contiene.all()[0].nombre, 'i1')
        self.assertEqual(first_plato.contiene.all()[0].descripcion, 'd1')
        self.assertEqual(first_plato.contiene.all()[1].nombre, 'i2')
        self.assertEqual(first_plato.contiene.all()[1].descripcion, 'd2')

        self.assertEqual(second_plato.nombre, 'Plato 2')
        self.assertEqual(second_plato.descripcion, 'Descripción del plato2')
        self.assertEqual(second_plato.precio, 2)
        self.assertEqual(second_plato.contiene.count(), 1)
        self.assertEqual(second_plato.contiene.all()[0].nombre, 'i2')
        self.assertEqual(second_plato.contiene.all()[0].descripcion, 'd2')


class MenuModelTest(TestCase):
    def test_guardar_y_ver_menu(self):
        i1 = Ingrediente(nombre='i1', descripcion='d1')
        i1.save()

        i2 = Ingrediente(nombre='i2', descripcion='d2')
        i2.save()

        plato1 = Plato(
            nombre='p1', descripcion = 'dp1', precio = 1)
        plato1.save()
        plato1.contiene.add('i1', 'i2')

        plato2 = Plato(
            nombre='p2', descripcion = 'dp2', precio = 2)
        plato2.save()
        plato2.contiene.add('i2')

        menu = Menu.objects.create(nombre = 'Menu 1', actual = True)

        menu.incluye.add('p1', 'p2')

        menus = Menu.objects.all()
        self.assertEqual(menus.count(), 1)

        self.assertEqual(menus[0].incluye.all()[0].nombre, 'p1')
        self.assertEqual(menus[0].incluye.all()[0].descripcion, 'dp1')

        self.assertEqual(menus[0].incluye.all()[1].nombre, 'p2')
        self.assertEqual(menus[0].incluye.all()[1].descripcion, 'dp2')

    def test_un_solo_menu_actual(self):
        Menu.objects.create(nombre='m1', actual=True)
        menu2 = Menu.objects.create(nombre='m2', actual=True)

        menu1 = Menu.objects.get(nombre='m1')

        self.assertFalse(menu1.actual)
        self.assertTrue(menu2.actual)

        menu3 = Menu.objects.create(nombre='m3', actual=True)
        menu1 = Menu.objects.get(nombre='m1')
        menu2 = Menu.objects.get(nombre='m2')

        self.assertFalse(menu1.actual)
        self.assertFalse(menu2.actual)
        self.assertTrue(menu3.actual)
