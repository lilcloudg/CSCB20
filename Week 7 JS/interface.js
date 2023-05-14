const nameField = document.querySelector("#name-input");
const messageField = document.querySelector("#text-input");
const submitButton = document.querySelector("#message-submit");
const messagesField = document.querySelector("#message-output");
const jsonField = document.querySelector("#json-output");
submitButton.addEventListener("click", submitMessage);
window.addEventListener("DOMContentLoaded",loadPage);


/*
Get a message from the name/message fields, add it to the
messages list and to local storage
*/
function submitMessage(){
    addNewMessage(nameField.value, messageField.value);
    updateList();
}

/*
get the messages for each user and display them on the screen
*/
function updateList(){
    msgList = "<ul>"
    usersArray = getUsers();
    for(nextUser of usersArray){
        msgList += "<li>" + nextUser;
        msgList += " says: " +getMessage(nextUser)+ "</li>";
    }
    msgList += "</ul>"
    messagesField.innerHTML = msgList;
    jsonField.innerHTML = getRawJSON();
}

/*
When the page is loaded, signal the "database" to activate and
refresh the page
*/
function loadPage(){
    loadData();    
    updateList();  
}

