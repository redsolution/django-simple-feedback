
function insertAndExecute(form, text) {

    /** Update form and execute form js */

    form.innerHTML = text;
    var scripts = Array.prototype.slice.call(form.getElementsByTagName("script"));
    for (var i = 0; i < scripts.length; i++) {
        var scriptNode = document.createElement("script");
        if (scripts[i].src != "") {
            scriptNode.src = scripts[i].src;
        }
        else {
            scriptNode.innerHTML = scripts[i].innerHTML;
        }
        document.getElementsByTagName("head")[0].appendChild(scriptNode);
    }
}

document.querySelectorAll('.feedback-form').forEach(function(form){
    form.addEventListener('submit', async function(event){

        /** Ajax submit for all feedback forms */

        event.preventDefault()
        let response = await fetch(form.getAttribute('action'), {
            method: 'POST',
            body: new FormData(form)
        })
        if(response.ok) {
            insertAndExecute(form, await response.text())
        } else {
            console.log(response.status)
        }
    })
})