const channelPage = document.getElementById('main-channel-page')
const fixedTabs = document.getElementById('fixed-tabs')
const movilTabs = document.getElementById('movil-tabs')

channelPage.onscroll = function(e){
    setTimeout(() => {
        if(e.target.scrollTop >= 350) {
            fixedTabs.classList.remove('hidden')
            movilTabs.classList.add('hidden')
        } else {
            fixedTabs.classList.add('hidden')
            movilTabs.classList.remove('hidden')
        }
    }, 500)
}