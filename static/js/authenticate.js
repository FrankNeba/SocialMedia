

const visibility1 = document.getElementById('password-visibility1')
const password1 = document.getElementById('password')
const visibilityText1 = document.getElementById('visibility-text1')

visibility1.addEventListener('click', (e) => {
    e.preventDefault()
    if (password1.type == 'text'){
        password1.type = 'password'
        visibilityText1.textContent = 'show'
    }
    else {
        password1.type ='text'
        visibilityText1.textContent = 'hide'
    }
})

const visibility2 = document.getElementById('password-visibility')
const password2 = document.getElementById('passwordConfirm')
const visibilityText2 = document.getElementById('visibility-text')

visibility2.addEventListener('click', (e) => {
    e.preventDefault()
    if (password2.type == 'text'){
        password2.type = 'password'
        visibilityText2.textContent = 'show'
    }
    else {
        password2.type ='text'
        visibilityText2.textContent = 'hide'
    }
})



