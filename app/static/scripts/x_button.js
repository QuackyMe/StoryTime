var closebtns = document.querySelectorAll(".close");


for (var i = 0; i < closebtns.length; i++) {
    closebtns[i].addEventListener('click', close, false);
}

function close(e) {
    this.parentElement.remove();
}