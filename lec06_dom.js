//let's add a listener to the button, so when it's clicked, we call yell
const dontClickButton = document.querySelector("#dont-click");
dontClickButton.addEventListener("click", yell);

function yell(){
    alert("STOP THAT!");
}

//another listener, but this time we're going to actually update
//the DOM
const countClickButton = document.querySelector("#count-button");
countClickButton.addEventListener("click", increment);

let clickCount = 0;
const countTargetParagraph = document.querySelector("#count-target");
function increment(){
    clickCount += 1;
    countTargetParagraph.innerHTML = clickCount;
    
}

//a more complex example... add an event listener to the button
//when that button is pressed, we'll check the value of the field
//if it's Brian, "log in", if not tell the user to go away
const nameSubmit = document.querySelector("#name-submit");
nameSubmit.addEventListener("click", checkName);
const nameField = document.querySelector("#name-input");
const nameOutput = document.querySelector("#name-response");
const brianParagraphs = document.querySelectorAll(".brian");
function checkName(){
    let userName = nameField.value;
    if(userName === "Brian"){
        nameOutput.innerHTML = "Welcome Brian";
        for(p of brianParagraphs){
            p.style.backgroundColor="green";
        }
    }else{
        nameOutput.innerHTML = "You are not welcome here";
        nameOutput.style.backgroundColor = "red";
    }
    
}
