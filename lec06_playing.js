//this is a comment

/*
This
is
a
multi
line
comment
*/

//we can use this to "print" to the console
//(eventually, this will mostly be used for debugging)
console.log("Hello World");

//constants (immutable)
const x = 7;
//x = x + 3; <-- this would cause an error

//variables (mutable)
let y = 7;
y = y + 3;
console.log("the value of x is: " + x);
console.log("the value of y is: " + y);

//JavaScript is dynamically typed
let word = "Hello"; //strings
let num = 3.4; //ints/floats
let bool = false; //boolean
let empty = null; //null values
let dunno = undefined; //placeholder values

//JavaScript will happily let you reassign types, and
//will try to help guess at what you want it to do
let test = 3;
test = test + 5;
console.log("the value of test is: " + test);
test = "hello";
test = test + 5;
console.log("the value of test is: " + test);
test = 5;
test = test + "hello";
console.log("the value of test is: " + test);

//////ARRAYS/////
const stuff = [1, 2, 3, 4];
///ASIDE: const vs let
// why did we do const stuff and not let stuff
// const isn't actually defining a constant value
// it's saying we can't re-assign that label
// so stuff will still be mutable, we just
// can't re-assign stuff now

console.log(stuff);
//arrays are mutable
stuff[0] = 99;
console.log(stuff);
//arrays can hold data of different types
stuff[1] = "Hello";
console.log(stuff);
//even other arrays
stuff[2] = ['A', 'B', 'C'];
console.log(stuff);
console.log(stuff[2][1]);
//and we can do slicing
bigger = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
console.log(bigger.slice(2,7));
//what about appending to an arrray?
stuff.push("ADDED");
console.log(stuff);


/////Selection////
let testValue = 21;

if(testValue < 0){
    console.log("Value is negative");
}else if(testValue > 100){
    console.log("Value is big");
}else if(testValue < 10){
    console.log("Value is small");
}else{
    console.log("Value is normal");
}

////Functions////

function myCoolFunction(oneParam, anotherParam){
    console.log("I'm inside a function, and you sent me a total of: " + oneParam + anotherParam);
    console.log("Were you expecting addition?");
    console.log("maybe you'd prefer a total of: "+ (oneParam + anotherParam));
    return oneParam + anotherParam * 3;
}

let result = myCoolFunction(10, 20);
console.log("result was: "+ result);

////LOOPS///

let count = 0;
while(count < 5){
    console.log(count);
    count += 1;
}

for(let i=0; i<5;i++){
    console.log(i);
}

const myArray = ["Apple", "Bear", "Carrot", "Dog"];

for(item of myArray){
    console.log(item);
}

//////Objects////
const brian = {
    name:"Brian",
    office:"IC342",
    awesomeness:99
};

console.log(brian);
brian["awesomeness"] += 1;
brian.awesomeness += 1;
console.log(brian);

for(attribute in brian){
    console.log(attribute + "->" + brian[attribute]);
}



/////The curse of = vs == vs ===

//== converts types before comparison... which can be nice
console.log('1' == 1);
//but sometimes it can also be confusing

console.log([] == "");
console.log([] == 0);
console.log(0 == "0");
console.log([] == "0");
console.log("----");
//so using === (triple equals) is safer under most conditions
//it compares without conversion
console.log('1' === 1);
console.log([] === "");
console.log([] === 0);
console.log(0 === "0");
console.log([] === "0");
