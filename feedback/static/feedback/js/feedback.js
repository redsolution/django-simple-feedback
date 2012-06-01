;
feedback = {
    submit: function(form){
        var data = {};

        var feedback_url = $(form).attr('action');
        var form_array = $(form).serializeArray();
        for (i=0;i<form_array.length;i++){
            var key = form_array[i].name;
            var value = form_array[i].value;
            data[key] = value;
        }

        $.post(feedback_url, data, function(data, textStatus){
            $(form).replaceWith(data).show();
        });
        return false;
    }
};
