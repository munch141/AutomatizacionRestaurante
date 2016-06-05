from django.core.urlresolvers import reverse
from django.shortcuts import redirect


def login_check(func):
    def wrapper(request, *args, **kwargs):
        if args:
            request = args[0]

        if request.user.is_authenticated():
            try:
                request.user.cliente
                return redirect(reverse('home_cliente'))
            except:
                try:
                    request.user.proveedor
                    return redirect(reverse('home_proveedor'))
                except:
                    return cuentas.views.logout(request)

        else:
            return func(request)

    return wrapper
