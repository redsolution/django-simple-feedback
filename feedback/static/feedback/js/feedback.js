;
feedback = {
    submit: function($form){
        var data = {};
        var form_array = $form.serializeArray();
        for (i = 0; i < form_array.length; i++){
            data[form_array[i].name] = form_array[i].value;
        }
        $.post($form.attr('action'), data, function(data, textStatus){
            $form.replaceWith(data).show();
        });
        return false;
    }
};

$(document).on('submit', '.feedback-form', function(e){
    e.preventDefault();
    feedback.submit($(this));
})