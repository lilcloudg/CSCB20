const messages = {};

/*
Add a new message to the "database"
*/
function addNewMessage(newName, newText){
    messages[newName] = newText;
    storeData();
}

/*
Get an array of all users who have left messages
*/
function getUsers(){
    userArray = [];
    for (nextUser in messages){
        userArray.push(nextUser);
    }
    return userArray;
}

/*
Get the message for a given user
*/
function getMessage(userName){
    return messages[userName];
}

/*
Get a JSON version of the current "database"
*/
function getRawJSON(){
    return JSON.stringify(messages);
}

/*
Get the current stored JSON file (if any) and load it into messages
*/
function loadData(){
    let fileSystemJSON = window.localStorage.getItem("messagesJSON");
    if(fileSystemJSON === null){
        setJSON("{}");
    }else{
        setJSON(fileSystemJSON);
    }
}

/*
store the data in messages to local stroage as a JSON
*/
function storeData(){
    currentJSON = JSON.stringify(messages);
    window.localStorage.setItem("messagesJSON",currentJSON);
}

/*
Load the "database" with data from a JSON
*/
function setJSON(JSONString){
    incomingJSON = JSON.parse(JSONString);
    for(nextName in incomingJSON){
        messages[nextName] = incomingJSON[nextName];
    }
}

