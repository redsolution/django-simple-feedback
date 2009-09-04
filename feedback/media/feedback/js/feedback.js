;
$(document).ready(function(){
    $('#feedback').submit(function(){
        var data = {};
        var feedback_url = $(this).attr('action');
        $(this).find(':input').each(function(){
            var key = $(this).attr('name');
            var value = $(this).attr('value');
            data[key] = value;
        });
        $.post(feedback_url, data, load_feedback);
        return false;
    });
});

function load_feedback(data, textStatus){
    $('#feedback').html(data).show();
}
