const dontClickButton = document.querySelector("#dont-click");
dontClickButton.addEventListener("click", yell);

function yell(){
    alert("STOP THAT!");
}