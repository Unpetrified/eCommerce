var carouselSlide = document.querySelector(".carousel-slide"),
    carouselImages = carouselSlide.children,
    cardWidth = carouselSlide.children[0],
    carouselContainer = document.querySelector(".carousel-container"),
    counter = 1, size = cardWidth.clientWidth,
    prevBtn = document.querySelectorAll("svg")[0],
    nextBtn = document.querySelectorAll("svg")[1];

carouselSlide.style.transform = "translateX(" +  -size*counter +"px)";
carouselContainer.style.width = size+"px";
console.log("out", size);

cardWidth.addEventListener("load", () => {
    size = cardWidth.clientWidth;
    console.log("in", size);
    carouselContainer.style.width = size+"px";
    carouselSlide.style.transform = "translateX(" +  -size*counter +"px)";
})

nextBtn.addEventListener("click", function() {
    if (counter >= carouselImages.length - 1) return;
    carouselSlide.setAttribute("class","carousel-slide transition");
    counter++;
    carouselSlide.style.transform = "translateX(" +  -size*counter +"px)"
})

prevBtn.addEventListener("click", function() {
    if (counter <= 0) return;
    carouselSlide.setAttribute("class","carousel-slide transition");
    counter--;
    carouselSlide.style.transform = "translateX(" +  -size*counter +"px)";
})

carouselSlide.addEventListener("transitionend", () =>{
    if (carouselImages[counter].getAttribute("id") == "last_clone") {
        counter = carouselImages.length - 2;
    }
    if (carouselImages[counter].getAttribute("id") == "first_clone") {
        counter = carouselImages.length - counter;
    }
    carouselSlide.setAttribute("class", "carousel-slide");
    carouselSlide.style.transform = "translateX(" +  -size*counter +"px)";
})

window.addEventListener("resize", () => {
    size = cardWidth.clientWidth;
    carouselSlide.style.transform = "translateX(" +  -size*counter +"px)";
    carouselContainer.style.width = size+"px";
})