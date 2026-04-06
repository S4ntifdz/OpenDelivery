from unfold.widgets import UnfoldAdminTextInputWidget
from django.utils.safestring import mark_safe

class RegenerableInputWidget(UnfoldAdminTextInputWidget):
    """
    Widget que hereda de Unfold para mantener el estilo (Dark mode, bordes, etc.)
    y añade un botón de autogeneración al final.
    """
    def __init__(self, prefix="key_", button_text="✨ Autogenerar", *args, **kwargs):
        self.prefix = prefix
        self.button_text = button_text
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        # El render original de Unfold ya trae todas las clases de CSS necesarias
        html = super().render(name, value, attrs, renderer)
        
        # Botón con estilo Unfold
        button_html = (
            f'<button type="button" class="regenerate-api-key bg-primary-600 text-white px-3 py-2 rounded-md ml-2 '
            f'text-sm font-semibold hover:bg-primary-700 transition-colors shrink-0 flex items-center gap-2" '
            f'data-prefix="{self.prefix}" '
            f'style="cursor: pointer; height: 42px;">'
            f'{self.button_text}'
            f'</button>'
        )
        # Envolvemos en un div flex para que queden alineados
        return mark_safe(f'<div class="flex items-center w-full max-w-2xl">{html}{button_html}</div>')