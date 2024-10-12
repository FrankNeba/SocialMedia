const warning = document.getElementById('warning')
const options = document.getElementById('options')
const submit = document.getElementById('submit')
const cancel = document.getElementById('cancel')

submit.addEventListener('click', (e) => {
    e.preventDefault()
    console.log('hello')
        warning.classList.toggle('hidden')
    submit.classList.toggle('hidden')
    options.classList.toggle('hidden')
    
    
})

cancel.addEventListener('click', (e)=>{
    e.preventDefault()
    warning.classList.toggle('hidden')
    submit.classList.toggle('hidden')
    options.classList.toggle('hidden')
})

