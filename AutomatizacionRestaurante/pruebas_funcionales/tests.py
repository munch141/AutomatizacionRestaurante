from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from administrador.models import Administrador
from cuentas.models import Cliente

class PruebasAdministrador(LiveServerTestCase):
    
    def agregar_cliente(
        self,
        username,
        nombre,
        apellido,
        ci,
        email,
        telefono,
        sexo,
        fecha_nacimiento
    ):
        user = User.objects.create(
                username=username,
                password='pw',
                email=email,
                first_name=nombre,
                last_name=apellido
            )
        cliente = Cliente.objects.create(
            usuario=user,
            ci=ci,
            fecha_nacimiento=fecha_nacimiento,
            sexo=sexo,
            telefono=telefono,
        )
        user.save()
        cliente.save()
        return user

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(2)

        user = User.objects.create(username='admin')
        user.set_password('pw')
        user.save()
        Administrador.objects.create(usuario=user)

        self.agregar_cliente(
            'cliente1',
            'Uno',
            'Cliente',
            '1',
            'cliente1@mail.com',
            '1111-1111111',
            'M',
            '1991-1-1')

        self.agregar_cliente(
            'cliente2',
            'Dos',
            'Cliente',
            '2',
            'cliente2@mail.com',
            '2222-2222222',
            'F',
            '1992-2-2')

        self.agregar_cliente(
            'cliente3',
            'Tres',
            'Cliente',
            '3',
            'cliente3@mail.com',
            '3333-3333333',
            'M',
            '1993-3-3')

    def tearDown(self):
        self.browser.quit()

    def chequear_fila_en_tabla_clientes(self, texto_fila):
        tabla = self.browser.find_element_by_id('tabla_clientes')
        filas = tabla.find_elements_by_tag_name('td')
        self.assertIn(texto_fila, [fila.text for fila in filas])

    def test_administrador_puede_ver_clientes_registrados(self):
        # El administrador entra a la página de inicio
        self.browser.get(self.live_server_url)

        # El admin ingresa el nombre de usuario "admin" con su contraseña
        username_input = self.browser.find_element_by_id('username_field')
        username_input.send_keys('admin')

        password_input = self.browser.find_element_by_id('password_field')
        password_input.send_keys('pw')

        password_input.send_keys(Keys.ENTER)

        # El admin es llevado a un nuevo URL donde está su paǵina principal
        home_admin_url = '%s%s' % (self.live_server_url, '/administrador/')

        self.assertEqual(home_admin_url, self.browser.current_url)

        # En la página principal ve una opción que dice "Ver clientes" y le da
        # click
        try:
            ver_clientes = self.browser.find_element_by_id('ver_clientes_button').click()
        except NoSuchElementException:
            self.fail('No hay un botón para ver clientes!\n'
                      '(Se buscó un elemento con id = ver_clientes_button)')

        # La página ahora redirecciona a admin a otra página que muestra un título
        # que dice "Clientes registrados:"
        self.assertNotEqual(home_admin_url, self.browser.current_url)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertEqual('Clientes registrados:', header_text)

        # Abajo del título se muestra una lista con dos columnas una para los
        # nombres de usuario con título 'Nombre de usuario' y otra para la fecha
        # de registro con título 'Fecha de registro'
        try:
            lista_clientes = self.browser.find_element_by_id('tabla_clientes')
        except NoSuchElementException:
            self.fail('No hay lista de clientes!\n'
                      '(Se buscó un elemento con id = tabla_clientes)')

        filas = lista_clientes.find_elements_by_tag_name('th')
        self.assertIn('Nombre de usuario', [fila.text for fila in filas])
        self.assertIn('Fecha de registro', [fila.text for fila in filas])

        # En la lista se ven los nombres de usuario de los clientes registrados
        # en el sistema
        cliente1 = User.objects.get(username='cliente1')
        cliente2 = User.objects.get(username='cliente2')
        cliente3 = User.objects.get(username='cliente3')

        self.chequear_fila_en_tabla_clientes(cliente1.username)
        self.chequear_fila_en_tabla_clientes(
            cliente1.date_joined.strftime('%d/%m/%Y'))

        self.chequear_fila_en_tabla_clientes(cliente2.username)
        self.chequear_fila_en_tabla_clientes(
            cliente2.date_joined.strftime('%d/%m/%Y'))

        self.chequear_fila_en_tabla_clientes(cliente3.username)
        self.chequear_fila_en_tabla_clientes(
            cliente3.date_joined.strftime('%d/%m/%Y'))

        # Decide ver los detalles de un cliente llamado "cliente1" y le da click
        # a su nombre de usuario
        self.fail('Hay que terminar la prueba!')
        


        # La página muestra los detalles del cliente y un botón que dice
        # "Regresar a la lista de clientes"


        # El admin le da click al botón y la página muestra la lista con todos
        # los clientes


        # El admin regresa a la página principal dándole click a "Restaurante"
        # en la barra de navegación

