(function ($) {
    "use strict";
    $(document).ready(function () {
        $(document).on('click', '.regenerate-api-key', function (e) {
            e.preventDefault();
            const prefix = $(this).data('prefix') || '';
            console.log("Generating with prefix: " + prefix);

            const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_';
            let result = prefix;
            const randomValues = new Uint32Array(32);
            window.crypto.getRandomValues(randomValues);
            for (let i = 0; i < 32; i++) {
                result += chars.charAt(randomValues[i] % chars.length);
            }

            const $parent = $(this).parent();
            let $input = $parent.find('input');

            if ($input.length === 0) {
                $input = $(this).siblings('input');
            }

            if ($input.length > 0) {
                $input.val(result).trigger('change');
            } else {
                console.error("No se encontró el campo de input");
            }
        });
    });
})(django.jQuery || jQuery);
