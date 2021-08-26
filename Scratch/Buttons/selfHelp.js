function buttonYes(btn) {
    buttonReset(btn)
    // var self_button = document.getElementById(btn);
    // self_button.style.background = '#00FF00'
    btn.style.background = '#00FF00'

    var parent = btn.parentElement;
    var c = parent.childNodes;
    var i;
    for (i = 0; i < c.length; i++) {
        if (c[i].className=="current_answer"){
                // console.log("found current_answer");
                // console.log(c[i]);
                c[i].style.backgroundColor = '#C0C0C0';
                c[i].innerHTML = "<p>Yes</p>";
            }
        // console.log("--")
    }
}

function buttonNo(btn) {
    buttonReset(btn)
    // var self_button = document.getElementById(btn);
    // self_button.style.background = '#FF0000'
    btn.style.background = '#FF0000'
    var parent = btn.parentElement;
    var c = parent.childNodes;
    var i;
    for (i = 0; i < c.length; i++) {
        if (c[i].className=="current_answer"){
                // console.log("found current_answer");
                // console.log(c[i]);
                c[i].style.backgroundColor = '#C0C0C0';
                c[i].innerHTML = "<p>No</p>";
            }
        // console.log("--")
    }
}

function buttonReset(btn) {
    var parent = btn.parentElement;
    // console.log("finding children");
    // console.log(parent.childNodes);
    var c = parent.childNodes;
    var i;
    for (i = 0; i < c.length; i++) {
        // console.log("I is",i);
        // console.log("printing c.id: ",c[i].id);
        // console.log("printing class name: ",c[i].className)
        if (c[i].className=="no_button"){
            // console.log("found no_button");
            // console.log(c[i]);
            c[i].style.backgroundColor = '#FF7575';
            }
        if (c[i].className=="yes_button"){
            // console.log("found yes_button");
            // console.log(c[i]);
            c[i].style.backgroundColor = '#B1FFB1';
            }
        if (c[i].className=="current_answer"){
                // console.log("found yes_button");
                // console.log(c[i]);
                c[i].style.backgroundColor = '#808080';
                c[i].innerHTML = "<p></p>"
            }
        // console.log("--")
        }
    }
