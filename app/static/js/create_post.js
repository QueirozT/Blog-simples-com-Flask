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

LIMPAR = document.querySelector('#flask-pagedown-pagedown')
LIMPAR.value = null 

RESPONDER = document.querySelector('#responder')

RESPONDER.addEventListener('click', function(e) {
    document.querySelector('#form_responder').classList.remove('d-none')
    document.querySelector('#responder').classList.add('d-none')
})

CANCELAR_RESPONDER = document.querySelector('#cancelar_responder')

CANCELAR_RESPONDER.addEventListener('click', function(e) {
    document.querySelector('#form_responder').classList.add('d-none')
    document.querySelector('#responder').classList.remove('d-none')
})