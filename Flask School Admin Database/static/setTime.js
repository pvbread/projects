let startHours = document.getElementsByClassName("start-hour");
let endHours = document.getElementsByClassName("end-hour");
console.log(startHours);
console.log('this is me right now');
for (item = 0; item < startHours.length; item++) {
    for (let i = 9; i < 22; i++){
        opt = document.createElement("option");
        optText = document.createTextNode(i);
        opt.setAttribute("value", i);
        opt.appendChild(optText);
        startHours[item].appendChild(opt);
    }

    for (let i = 9; i < 22; i++){

        opt = document.createElement("option");
        optText = document.createTextNode(i);
        opt.setAttribute("value", i);
        opt.appendChild(optText);
        endHours[item].appendChild(opt);
    }
}