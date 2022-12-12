ESCREVER = document.querySelector('#escrever')

ESCREVER.parentNode.addEventListener('click', function(e) {
    if (ESCREVER.checked ) {
        document.querySelector('.flask-pagedown').classList.remove('d-none') 
        document.querySelector('.flask-pagedown-preview').classList.add('d-none')
    }
    else {
        document.querySelector('.flask-pagedown').classList.add('d-none')
        document.querySelector('.flask-pagedown-preview').classList.remove('d-none')
    }
})

VISUALIZAR = document.querySelector('.flask-pagedown-preview')
VISUALIZAR.classList.add('p-2')
VISUALIZAR.classList.add('d-none')
VISUALIZAR.classList.add('text-break')

RESPONDER = document.querySelector('#responder')

if (RESPONDER) {
    RESPONDER.addEventListener('click', function(e) {
        document.querySelector('#form_responder').classList.remove('d-none')
        document.querySelector('#responder').classList.add('d-none')
    })
}

CANCELAR_RESPONDER = document.querySelector('#cancelar_responder')

if (CANCELAR_RESPONDER) {
    CANCELAR_RESPONDER.addEventListener('click', function(e) {
        document.querySelector('#form_responder').classList.add('d-none')
        document.querySelector('#responder').classList.remove('d-none')
    })
}

document.querySelectorAll('img').forEach(function(e){
    e.classList.add('img-fluid')
})