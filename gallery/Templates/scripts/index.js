//Products Slider
let productsSwiper = new Swiper('.products-swiper-container', {
    slidesPerView: 2,
    spaceBetween: 30,
    pagination: {
        el: '.products-swiper-pagination',
        clickable: true,
    },
    navigation: {
        nextEl: '.products-swiper-button-next',
        prevEl: '.products-swiper-button-prev',
    },
    autoplay: {
        delay: 5000,
    },
    breakpoints: {
        0: {
            slidesPerView: 1,
        },
        576: {
            slidesPerView: 2,
        },
        768: {
            slidesPerView: 2,
        },
        992: {
            slidesPerView: 3,
        },
        1200: {
            slidesPerView: 4,
        },
    }
});

//Blog Slider
let blogSwiper = new Swiper('.blog-swiper-container', {
    slidesPerView: 2,
    spaceBetween: 30,
    pagination: {
        el: '.blog-swiper-pagination',
        clickable: true,
    },
    navigation: {
        nextEl: '.blog-swiper-button-next',
        prevEl: '.blog-swiper-button-prev',
    },
    autoplay: {
        delay: 5000,
    },
    breakpoints: {
        0: {
            slidesPerView: 1,
        },
        576: {
            slidesPerView: 2,
        },
        768: {
            slidesPerView: 2,
        },
        992: {
            slidesPerView: 3,
        },
        1200: {
            slidesPerView: 4,
        },
    }
});
