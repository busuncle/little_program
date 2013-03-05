// a graceful implementation for a status-checker using closure avoiding global variable
var click_it = (function(){
    var clicked = false;
    return function(){
        if(clicked){
            return;
        }
        clicked = true;
        alert("click this!");
    }
}());


// call it, it will alert only once
click_it();
click_it();
click_it();
