var questionButton = document.getElementById('btn_question');
var questionSection = document.getElementById('questions');
var firstQuestion = document.getElementById('firstQuestion');

var counter = 0;

questionSection.addEventListener('click', addChoice);
questionButton.addEventListener('click', addQuestion);

function addChoice(e) {
    if (e.target.id === 'btn_choice') {
        var newLabel = document.createElement('h4');
        newLabel.appendChild(document.createTextNode('Choice: '));

        var newInput = document.createElement('input');
        newInput.name = 'choice[]';

        newLabel.appendChild(newInput)
        e.target.parentElement.insertBefore(newLabel, e.target);
    }
}

function addQuestion(e) {
    if (e.target.id === 'btn_question') {
        var clone = firstQuestion.cloneNode(true);
        for (var i = 0; i < clone.children.length; i++) {
            for (var j = 0; j < clone.children[i].children.length; j++) {
                if (clone.children[i].children[j].tagName != 'SELECT')
                    clone.children[i].children[j].value = "";
            }
        }
        questionSection.insertBefore(clone, questionButton);
    }
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