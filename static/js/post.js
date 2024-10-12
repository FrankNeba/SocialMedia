const show = document.getElementById('show')
const hide = document.getElementById('hide')
const menu = document.getElementById('menu')

show.addEventListener('click', () => {
    console.log('clicked')
    menu.classList.toggle('hidden')
    menu.classList.toggle('flex')
    hide.classList.toggle('hidden')
})
hide.addEventListener('click', () => {
    menu.classList.toggle('hidden')
    menu.classList.toggle('flex')
    hide.classList.toggle('hidden')
})

const text = document.getElementById('post-text')
const more = document.getElementById('see-more')

more.addEventListener('click', () => {
    text.classList.toggle('text-truncate')
    text.classList.toggle('flex-wrap')
    text.classList.toggle('overflow-hidden')
    if(more.textContent == 'see more'){
        more.textContent = 'see less'
    }
    else {
        more.textContent = 'see more'
    }
})