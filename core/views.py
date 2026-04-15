from django.shortcuts import redirect
from django.utils import translation
from django.conf import settings

def change_language(request):
    """
    Cambia el idioma del usuario y redirige a la página anterior.
    Soporta parámetros GET para facilitar el uso en el sidebar del admin.
    """
    lang_code = request.GET.get('language')
    if lang_code in [lang[0] for lang in settings.LANGUAGES]:
        translation.activate(lang_code)
        request.session[translation.LANGUAGE_SESSION_KEY] = lang_code
    
    next_path = request.GET.get('next', request.META.get('HTTP_REFERER', '/'))
    return redirect(next_path)
