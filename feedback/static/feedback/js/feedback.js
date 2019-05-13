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

var important_fields = document.getElementsByClassName('important-field');

for(var i = 0; i < important_fields.length; i++){
    important_fields[i].style.display = 'none';
}
