const _resizableContainer = document.querySelector('#resizable-container')

document.addEventListener('alpine:init', () => {
    Alpine.store('global', {
        sidebar: {
            show: true,
            showWatch: false,
            toggle(){
                if(window.location.pathname.includes('watch')){
                    this.showWatch = !this.showWatch
                    return
                }
                if(window.innerWidth > 1200){
                    this.show = !this.show
                    if(this.show) _resizableContainer.style.marginLeft = '15rem'
                    else _resizableContainer.style.marginLeft = '5rem'
                    return
                }
                if(!this.show) this.show = true 
                this.showWatch = !this.showWatch
            }
        },
        keywords: {
            start: true,
            end: false,
            toLeft(){
                const box = document.getElementById("keywords")
                box.scroll({
                    left: box.scrollLeft - 250,
                    behavior: "smooth",
                })
                this.start = box.scrollLeft === 0
                this.end = box.scrollWidth - box.scrollLeft === box.clientWidth
            },
            toRight(){
                const box = document.getElementById("keywords")
                box.scroll({
                    left: box.scrollLeft + 250,
                    behavior: "smooth",
                })
                this.start = box.scrollLeft === 0
                this.end = box.scrollWidth - box.scrollLeft === box.clientWidth
            }
        },
        contentWShort: "max-width: calc(100vw - 17.5rem)",
        contentWFull:  "max-width: calc(100vw - 7.5rem)",
        showModal: false
    })
})