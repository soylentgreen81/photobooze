"use strict";
document.getElementById("trigger").addEventListener("click",snap);

function snap(){
    console.log("Taking a picture...");
    document.getElementById("image").src ="/static/spinner.svg";
    fetch('/pictures',{method:"POST"})
    .then(function(response) {
        return response.json();
    })
    .then(function(data) {
         console.log(data.pictureurl);
         document.getElementById("image").src = data.pictureurl;
    });

}
