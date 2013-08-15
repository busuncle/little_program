// throw errors
(function recursion_function(n){
    try {
        if(n == 0){
            console.log("end the program");
            return;
        }
        throw new Error("this is error " + n);
    } catch(e) {
        console.log(e.name + ": " + e.message);
        recursion_function(n-1);
    }
})(3);
phantom.exit();

