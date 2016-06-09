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
            'cliente1', 'Uno', 'Cliente', '1', 'cliente1@mail.com',
            '1111-1111111', 'M', '1991-1-1')

        self.agregar_cliente(
            'cliente2', 'Dos', 'Cliente', '2', 'cliente2@mail.com',
            '2222-2222222', 'F', '1992-2-2')

        self.agregar_cliente(
            'cliente3', 'Tres', 'Cliente', '3', 'cliente3@mail.com',
            '3333-3333333', 'M', '1993-3-3')

    def tearDown(self):
        self.browser.quit()

    def chequear_fila_en_tabla_clientes(self, texto_fila):
        tabla = self.browser.find_element_by_id('tabla_clientes')
        filas = tabla.find_elements_by_tag_name('td')
        self.assertIn(texto_fila, [fila.text for fila in filas])

    def concatenar(self, s1, s2):
        return '%s%s' % (s1, s2)

    def buscar_elemento_por_id(self, ident, error):
        try:
            elem = self.browser.find_element_by_id(ident)
            return elem
        except NoSuchElementException:
            return self.fail(error)

    def chequear_datos_cliente(self, link_cliente, home_admin_url, ver_clientes_url):
        user = User.objects.get(username=link_cliente.text)
        cliente = Cliente.objects.get(usuario=user)
        
        link_cliente.click()
        
        self.assertNotEqual(home_admin_url, self.browser.current_url)
        self.assertNotEqual(ver_clientes_url, self.browser.current_url)
        self.assertIn(user.username, self.browser.current_url)
        
        header_text = self.browser.find_element_by_tag_name('h1').text
        titulo_esperado = self.concatenar('Datos de ', user.username)
        self.assertEqual(titulo_esperado, header_text)

        nombre = self.browser.find_element_by_id('nombre')
        apellido = self.browser.find_element_by_id('apellido')
        cedula = self.browser.find_element_by_id('cedula')
        email = self.browser.find_element_by_id('email')
        telefono = self.browser.find_element_by_id('telefono')
        sexo = self.browser.find_element_by_id('sexo')
        fecha_nacimiento = self.browser.find_element_by_id(
            'fecha_nacimiento')
        fecha_registro = self.browser.find_element_by_id('fecha_registro')

        self.assertEqual(
            self.concatenar('Nombre: ', user.first_name), nombre.text)
        self.assertEqual(
            self.concatenar('Apellido: ', user.last_name), apellido.text)
        self.assertEqual(
            self.concatenar('Cédula: ', cliente.ci), cedula.text)
        self.assertEqual(
            self.concatenar('Correo electrónico: ', user.email), email.text)
        self.assertEqual(
            self.concatenar('Teléfono: ', cliente.telefono), telefono.text)
        self.assertEqual(
            self.concatenar('Sexo: ', cliente.sexo), sexo.text)
        self.assertEqual(
            self.concatenar(
                'Fecha de nacimiento: ',
                cliente.fecha_nacimiento.strftime('%d/%m/%Y')),
            fecha_nacimiento.text)
        self.assertEqual(
            self.concatenar(
                'Fecha de registro: ',
                user.date_joined.strftime('%d/%m/%Y')),
            fecha_registro.text)

        regresar = self.buscar_elemento_por_id(
            'boton_regresar',
            'No hay botón para regresar a la página anterior! (se buscó un '
            'elemento con id = "boton_regresar")')
        
        regresar.click()

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
        home_admin_url = self.concatenar(self.live_server_url, '/administrador/')

        self.assertEqual(home_admin_url, self.browser.current_url)

        # En la página principal ve una opción que dice "Ver clientes" y le da
        # click
        ver_clientes = self.buscar_elemento_por_id(
                'ver_clientes_button',
                'No hay un botón para ver clientes!\n'
                '(Se buscó un elemento con id = ver_clientes_button)')

        ver_clientes.click()

        # La página ahora redirecciona a admin a otra página que muestra un título
        # que dice "Clientes registrados:"
        self.assertNotEqual(home_admin_url, self.browser.current_url)
        ver_clientes_url = self.browser.current_url
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertEqual('Clientes registrados:', header_text)

        # Abajo del título se muestra una lista con dos columnas una para los
        # nombres de usuario con título 'Nombre de usuario' y otra para la fecha
        # de registro con título 'Fecha de registro'
        lista_clientes = self.buscar_elemento_por_id(
            'tabla_clientes',
            'No hay lista de clientes!\n'
            '(Se buscó un elemento con id = "tabla_clientes")')

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

        # Decide ver los detalles de todos los clientes del sistema y le da
        # click a los nombres de usuario de cada uno, al hacerlo se redirije a
        # un URL que incluye el nombre de usuario del cliente y que muestra
        # una página con los datos del cliente. Luego de ver los datos de un
        # admin le da al botón que dice 'Regresar a la lista de clientes' que
        # lo lleva de regreso a la página anterior

        link_cliente1 = self.buscar_elemento_por_id(
            'cliente1',
            'No hay link para cliente1!\n'
            '(Se buscó un elemento con id = "cliente1")')
        self.chequear_datos_cliente(
            link_cliente1, home_admin_url, ver_clientes_url)

        link_cliente2 = self.buscar_elemento_por_id(
            'cliente2',
            'No hay link para cliente2!\n'
            '(Se buscó un elemento con id = "cliente2")')
        self.chequear_datos_cliente(
            link_cliente2, home_admin_url, ver_clientes_url)

        link_cliente3 = self.buscar_elemento_por_id(
            'cliente3',
            'No hay link para cliente3!\n'
            '(Se buscó un elemento con id = "cliente3")')
        self.chequear_datos_cliente(
            link_cliente3, home_admin_url, ver_clientes_url)

        # El admin regresa a la página principal dándole click a "Restaurante"
        # en la barra de navegación
        home = self.buscar_elemento_por_id(
            'boton_home',
            'No hay botón para regresar a la página principal!'
            ' (se buscó un elemento con id="botón_home")')
        home.click()
