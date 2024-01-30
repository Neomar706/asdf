const btnSidebar = document.querySelector('.w-10.h-10')
const resizableContainer = document.querySelector('#resizable-container')
const modalSidebar = document.querySelector('#modal-sidebar')
const permanentSidebar = document.querySelector('#permanent-sidebar')

const lte1200 = () => {
    resizableContainer.style.marginLeft = '0'
    modalSidebar.style.display = 'block'
    permanentSidebar.style.display = 'none'
}

const gt1200 = () => {
    resizableContainer.style.marginLeft = '15rem'
    modalSidebar.style.display = 'none'
    permanentSidebar.style.display = 'block'
}

window.onload = () => {
    window.innerWidth <= 1200 && !window.location.pathname.includes('watch') && lte1200()
    window.onresize = () => {
        if(window.innerWidth <= 1200 && !window.location.pathname.includes('watch')) lte1200()
        else if(window.innerWidth > 1200 && !window.location.pathname.includes('watch')) gt1200()
    }
}
