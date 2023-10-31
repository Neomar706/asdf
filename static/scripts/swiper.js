const swiperAll = document.querySelectorAll('.swiper')

const swiperControls = []
for(let i = 0; i < swiperAll.length; i++){
	swiperControls.push({
		swiperNext: document.getElementById(`swiper_next_${i}`),
		swiperPrev: document.getElementById(`swiper_prev_${i}`)
	})
}

for(let i = 0; i < swiperAll.length; i++){
	new Swiper(`.swiper`, {
		direction: 'horizontal',
		slidesPerView: 6,
		slidesPerGroup: 6,
		spaceBetween: 8,
		allowTouchMove: false,
	})
}

for(let i = 0; i < swiperAll.length; i++){
	const swiper =  swiperAll[i].swiper
	swiperControls[i].swiperNext.onclick = () => swiper.slideNext()
	swiperControls[i].swiperPrev.onclick = () => swiper.slidePrev()

	swiper.on('slideChange', e => {
		e.isBeginning
			? swiperControls[i].swiperPrev.classList.add('hidden')
			: swiperControls[i].swiperPrev.classList.remove('hidden')
		
		e.isEnd
			? swiperControls[i].swiperNext.classList.add('hidden')
			: swiperControls[i].swiperNext.classList.remove('hidden')
	})
}