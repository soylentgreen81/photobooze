"use strict";
document.getElementById("trigger").addEventListener("click",snap);

function snap(){
    let image = document.getElementById("image");
    console.log("Taking a picture...");
    image.src ="/static/spinner.svg";
    fetch('/api/v1/pictures',
       {method:"POST"}
    )
      .then(response=> response.json() )
      .then(json=> image.src = json.scaled)
      .catch(error => image.src='/static/broken.png');

}
