document.addEventListener('alpine:init', () => {
    Alpine.store('global', {
        sidebar: {
            show: true,
            showWatch: false,
            toggle(){
                if(!window.location.pathname.includes('watch')) this.show = !this.show
                else this.showWatch = !this.showWatch
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