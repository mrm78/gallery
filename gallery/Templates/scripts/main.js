//Smooth Scroll
$(document).ready(function() {
    $(".scroll").on('click', function(event) {
        if (this.hash !== "") {
            event.preventDefault();
            let hash = this.hash;
            $('html, body').animate({
                scrollTop: $(hash).offset().top
            }, 800, function() {
                window.location.hash = hash;
            });
        }
    });
});

//Scroll Button
let button = document.getElementById("scroll-button");
let header = document.getElementById("header");
window.addEventListener("scroll", scroll);
window.addEventListener("resize", scroll);

function scroll() {
    if (window.innerWidth >= 1300) {
        if (document.body.scrollTop > header.getBoundingClientRect().top + window.scrollY || document.documentElement.scrollTop > +header.getBoundingClientRect().top + window.scrollY) {
            button.style.display = "block";
        } else {
            button.style.display = "none";
        }
    } else {
        button.style.display = "none";
    }
}

function goTop() {
   $("html,body").animate({
            scrollTop: 0},
        'slow');
}

//Search Box
function openSearch() {
    document.getElementById("searchOverlay").style.opacity = "1";
    document.getElementById("searchOverlay").style.visibility = "visible";

}

function closeSearch() {
    document.getElementById("searchOverlay").style.opacity = "0";
    document.getElementById("searchOverlay").style.visibility = "hidden";

}
