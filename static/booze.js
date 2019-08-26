"use strict";
const btn = document.getElementById("trigger");
const image = document.getElementById("image");
const counter = document.getElementById("counter");
const socket = io();
const colors = [
    "#8f807",
    "#a153a0",
    "#00aaab",
    "#0070bb",
    "#ffd100",
    "#f6931c",
    "#ec1b24",
    "#8bc63f",
    "#0cb04a",
];
let currentColor = 0;
btn.addEventListener("click",snap);
function enterFullscreen(element) {
    if(element.requestFullscreen) {
      element.requestFullscreen();
    } else if(element.mozRequestFullScreen) {
      element.mozRequestFullScreen();
    } else if(element.msRequestFullscreen) {
      element.msRequestFullscreen();
    } else if(element.webkitRequestFullscreen) {
      element.webkitRequestFullscreen();
    }
}

function snap() {
    socket.emit('trigger', {});
    enterFullscreen(document.documentElement);
}
socket.on('working', (data) =>{
    console.log(data);
    btn.removeEventListener("click",snap);
	image.style.background = '';
	counter.classList.add('animated'); 
	counter.classList.add('intensifies'); 
});
socket.on('timer', (data) => {
    console.log(data);
    image.style.backgroundImage = "none";
    btn.value = 'Noch ' + data.time + ' Sekunden';
    counter.style.color = colors[currentColor];
    counter.innerHTML = data.time;
    currentColor += 1;
    if (colors.length == currentColor)
        currentColor = 0;
});
socket.on('result', (data) => {
    console.log(data);
    image.style.background ="url(" + data.src + ") center no-repeat";
    btn.addEventListener("click", snap);
    btn.value = 'Click!';
    setTimeout(function(){
        image.classList.add('animated');
        image.classList.add('intensifies');
        setTimeout(function(){
            image.style.background = '';
            image.style["background-image"] = "url('/static/polaroid.svg')";
            image.classList.remove('animated');
            image.classList.remove('intensifies');
        },2000)
    },5000)
});
socket.on('error', (data) => {
    console.log(data);
    btn.addEventListener("click", snap);
    btn.value = data;
}
);
socket.on('processing', (data) => {
    console.log(data);
    counter.innerHTML = '';
    counter.classList.remove('animated'); 
    counter.classList.remove('intensifies'); 
    image.style.background ="url(/static/spinner.svg) center no-repeat";
});
socket.on('random', (data) => {
    console.log(data);
});
