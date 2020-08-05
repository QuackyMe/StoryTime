var div = document.getElementById('course_code')

div.addEventListener("keyup", moveCursor);
div.addEventListener("click", clear);

console.log("Hi");

function moveCursor(e) {
    keycode = e.keyCode;
    var counter = parseInt(e.target.id.slice(-1), 10);
    if(e.target.id != 'input_5' && keycode != 8){
        document.getElementById('input_' + (counter+1).toString()).focus();
    }
    if(keycode == 8){
        document.getElementById('input_' + (counter-1).toString()).value="";
        document.getElementById('input_' + (counter-1).toString()).focus();
    }
}

function clear(e) {
    input = document.getElementsByTagName('input');
    if(e.target.id== "input_1"){
        for(var counter = 1; counter <= 5; counter++){
            document.getElementById('input_' + counter.toString()).value="";
        }
    }
}