document.addEventListener("DOMContentLoaded", function () {
    let angleX = 0;
    let angleY = 0;
    const textElement = document.querySelector("p");
    
    function rotateText() {
        angleX += 1;
        angleY += 1;
        textElement.style.transform = `rotateX(${angleX}deg) rotateY(${angleY}deg)`;
        textElement.style.display = "inline-block";
        textElement.style.perspective = "500px";
        requestAnimationFrame(rotateText);
    }
    
    rotateText();
});