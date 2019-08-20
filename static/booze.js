"use strict";
const btn = document.getElementById("trigger");
const image = document.getElementById("image");
const counter = document.getElementById("counter");
const socket = io();
btn.addEventListener("click",snap);


function socket_test() {
    socket.emit('random', {});
}
function snap() {
    socket.emit('trigger', {});
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
	btn.value = 'Noch ' + data.time + ' Sekunden';
	counter.innerHTML = data.time;
});
socket.on('result', (data) => {
    console.log(data);
    image.style.background ="url(" + data.scaled + ") center no-repeat";
    btn.addEventListener("click", snap);
    btn.value = 'Click!';
    setTimeout(function(){
        image.classList.add('animated');
        image.classList.add('intensifies');
        setTimeout(function(){
            image.style.background = '';
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
