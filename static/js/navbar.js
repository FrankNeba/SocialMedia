const data = document.currentScript.dataset
const page = data.page
const links = document.querySelectorAll('.link')

links.forEach(link => {
    if(link.getAttribute('data-url-name') === page){
        link.classList.add('text-primary')
        link.classList.add('underline')
        link.classList.add('decoration-4')
        link.classList.add('underline-offset-8')
    }
})