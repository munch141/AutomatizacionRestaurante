from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from administrador.models import Administrador

class PruebasAdministrador(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

        user = User.objects.create(username='admin')
        user.set_password('pw')
        user.save()
        admin = Administrador.objects.create(usuario=user)

    def tearDown(self):
        self.browser.quit()

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
        self.fail('Hay que terminar la prueba!')

        # En la página principal ve una opción que dice "Ver clientes" y le da
        # click


        # La página ahora muestra un título que dice "Clientes registrados:"


        # Abajo del título se muestra una lista con los nombres de usuario de
        # todos los clientes registrados y la fecha de su registro


        # Decide ver los detalles de un cliente llamado "cliente1" y le da click
        # a su nombre de usuario


        # La página muestra los detalles del cliente y un botón que dice
        # "Regresar a la lista de clientes"


        # El admin le da click al botón y la página muestra la lista con todos
        # los clientes


        # El admin regresa a la página principal dándole click a "Restaurante"
        # en la barra de navegación

