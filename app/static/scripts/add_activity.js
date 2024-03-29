var questionButton = document.getElementById('btn_question');
var questionSection = document.getElementById('questions');
var template = document.getElementById('template');
var form = document.querySelector('form');
var question_num = document.querySelector('#question_num');

form.addEventListener('submit', submit);
questionSection.addEventListener('click', addChoice);
questionSection.addEventListener('change', choiceButton);
questionButton.addEventListener('click', addQuestion);

var counter = 0;
var choice_counter = 0;
window.onload = addQuestion();

function choiceButton(e) {
    let parent = e.target.parentNode.parentNode;
    let c_button = parent.querySelector("#btn_choice");
    let type = parent.querySelector("#q_type");
    let choices = parent.querySelectorAll(".choice_item");

    if(type.value == "stt"){
        c_button.style.visibility = "hidden";
        choices.forEach(element => element.remove());
    }
    else{
        c_button.style.visibility = "visible";
    }
} 

function addChoice(e) {
    if (e.target.id === 'btn_choice') {
        var newLabel = document.createElement('h2');
        newLabel.appendChild(document.createTextNode('Choice: '));
        newLabel.className = 'choice_item choice_container';

        var newInput = document.createElement('input');
        newInput.name = `choice_${String(choice_counter)}`;

        var newButton = document.createElement('span');
        newButton.className = 'close';
        newButton.innerHTML = '&times;';

        newLabel.appendChild(newInput);
        newLabel.appendChild(newButton);
        e.target.parentElement.insertBefore(newLabel, e.target);
        newButton.addEventListener('click', deleteChoice);
    }
}

function deleteChoice(e) {
    e.target.parentNode.remove();
}

function addQuestion(e) {
    if (counter == 0 || e.target.id === 'btn_question') {
        counter++;
        question_num.value++;
        var clone = template.cloneNode(true);
        clone.classList.remove('hidden');
        clone.id = counter;
        clone.getElementsByTagName('h2')[0].textContent = `Question ${counter} :`;

        input = clone.getElementsByTagName('input');
        for (var i = 0; i < input.length; i++) {
            input[i].value = null;
        }
        questionSection.insertBefore(clone, questionButton);

        choice_counter++;
    }
}

function submit(e) {
    input = document.getElementsByName
}







// var form = document.getElementById('addForm');
// var itemList = document.getElementById('items');
// var filter = document.getElementById('filter')

// form.addEventListener('submit', addItem);
// itemList.addEventListener('click', removeItem);
// filter.addEventListener('keyup', filterItems);

// function addItem(e){
//     e.preventDefault();

//     var newItem = document.getElementById('item').value;
//     var li = document.createElement('li');
//     li.className = 'list-group-item';
//     li.appendChild(document.createTextNode(newItem));

//     var deleteBtn = document.createElement('button');
//     deleteBtn.className = "btn btn-danger btn-sm float-right delete";
//     deleteBtn.appendChild(document.createTextNode("X"));

//     li.appendChild(deleteBtn);
//     itemList.appendChild(li);
// }

// function removeItem(e){
//     if(e.target.classList.contains('delete')) {
//         if(confirm("Are you sure?")){
//             var li = e.target.parentElement;
//             itemList.removeChild(li);
//         }
//     }
// }

// function filterItems(e){
//     var text = e.target.value.toLowerCase();
//     var items = itemList.getElementsByTagName('li');
//     Array.from(items).forEach(function(item){
//         var itemName = item.firstChild.textContent.toLowerCase();
//         if(itemName.indexOf(text) != -1) {
//             item.style.display = 'block';
//         } else {
//             item.style.display = 'none';
//         }
//     })
// }