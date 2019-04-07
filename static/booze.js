"use strict";
const btn = document.getElementById("trigger");
const image = document.getElementById("image");
const counter = document.getElementById("counter");
btn.addEventListener("click",countdownTimer);

function countdownTimer(){
	// weg mit listener
	btn.removeEventListener("click",countdownTimer);
	let timeLeft = 5;
	btn.value = 'Noch ' + timeLeft + ' Sekunden';
	image.style.background = '';
	counter.classList.add('animated'); 
	counter.classList.add('intensifies'); 
	counter.innerHTML = timeLeft;
	const downloadTimer = setInterval(function(){
		timeLeft--;
	    console.log(`Noch ${timeLeft} Sekunden`);
	    btn.value = `Noch ${timeLeft} Sekunden`;
		counter.innerHTML = timeLeft;
		if (timeLeft <= 0){
			clearInterval(downloadTimer);
			counter.innerHTML = '';
			counter.classList.remove('animated'); 
			counter.classList.remove('intensifies'); 
			snap();
		}
	}, 1000);
}

function snap(){
    console.log("Taking a picture...");
    image.style.background ="url(/static/spinner.svg) center no-repeat";
    fetch('/api/v1/pictures',
       {method:"POST"}
    )
   .then(response => response.json() )
   .then(json => {
        image.style.background ="url(" + json.scaled + ") center no-repeat";
        btn.addEventListener("click",countdownTimer);
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
  })
  .catch(error => image.style.background="url(/static/broken.png) center no-repeat");

}
