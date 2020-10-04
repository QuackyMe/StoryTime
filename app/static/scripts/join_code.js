var div = document.getElementById('course_code')

div.addEventListener("keypress", moveCursor);
div.addEventListener("click", clear);



console.log("Hi");

// function type(e){
//     e.target.value = String.fromCharCode(e.keyCode);
//     e.target.blur();
//     moveCursor(e.target, e.keyCode, e.target.id);


// }

function moveCursor(e) {
    console.log(e.keyCode);
    var counter = parseInt(e.target.id.slice(-1), e.target.id.length);

    if (e.target.id != 'input_5' && e.keyCode != 8) {
        document.getElementById('input_' + (counter + 1).toString()).focus();
    }
    if (e.keyCode == 8) {
        document.getElementById('input_' + (counter - 1).toString()).value = "";
        document.getElementById('input_' + (counter - 1).toString()).focus();
    }
}

function clear(e) {
    input = document.getElementsByTagName('input');
    if (e.target.id == "input_1") {
        for (var counter = 1; counter <= 5; counter++) {
            document.getElementById('input_' + counter.toString()).value = "";
        }
    }
}

