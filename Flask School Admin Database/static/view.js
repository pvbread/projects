
// option is paired with generate dropDown, and a lose conditional
// its tied to a none display jinja in 207 of the view.html
// option should have a clearer name
//let option = document.getElementById("option").textContent

// **** GENERATE SCHEDULE ON LOAD ******
let dataText = document.getElementById("data").textContent;
let schedule = document.getElementById("schedule");
// roster is the plain view of the roster instead of schedule
let roster = document.getElementById("roster");
let betterRoster = document.getElementById('better-roster');
// ****ENDBLOCK *******

//unsure max_class needs to be state here
let max_class = 0;

// **** GENERATE DROPDOWN ******
let allClasses = document.getElementById("all-classes").textContent;
//don't know that classSessions needs to be in the generate dropdown function, but it is in the block category

//this is only for the sessions, and so maybe it should ONNNNLYYYY
//be called then, because what happens, well, first it's text content, so that's not surviving
//and it's just tighter programming


// ****ENDBLOCK *******


// ****BUTTON FUNCTIONALITY********
let viewBtn = document.getElementById("viewBtn");
let addDropBtn = document.getElementById("addDropBtn");
let addBtn = document.getElementById("addBtn");
let dropBtn = document.getElementById("dropBtn");
let modifyBtn = document.getElementById("modifyBtn");
let confirmAdd = document.getElementById("confirm-add-button");
let confirmDrop = document.getElementById("confirm-drop");
let confirmModify = document.getElementById("confirm-modify-button");
let addTime = document.getElementById("add-time");
let dropTime = document.getElementById("drop-time");
let modifyTime = document.getElementById("modify-block");

// ****ENDBLOCK *******

// *********** JSON BUSINESS ************

let sessionJSON;

function getSessionJSON(){
    let urlCourse = document.getElementById('classfield_1').selectedOptions[0].value;
    let url = 'http://www.pedrovv.com/sessions/'


    fetch(url+urlCourse)
        .then(data => data.json())
        .then(success => sessionJSON = success)
        .catch(err => console.log('Something went wrong: ', err));
}

let rosterJSON;

function getRosterJSON(){


    url = 'http://www.pedrovv.com/roster/'

    fetch(url)
        .then(data => data.json())
        .then(success => rosterJSON = success)
        .catch(err => console.log('Something went wrong: ', err));


}




let classesJSON;
function fetchClassesJSON(){
    url = 'http://www.pedrovv.com/classes/'

    fetch(url)
        .then(data => data.json())
        .then(success => classesJSON = success)
        .catch(err => console.log('Something went wrong: ', err));

    return new Promise(resolve => {
        setTimeout(function() {
            resolve(classesJSON)
            console.log(classesJSON)
        }, 1000)
        
    })
}

async function getClassesJSON(){
    const test = await fetchClassesJSON()
    return classesJSON;
}

let studentsInClassJSON;
function fetchStudentsInClass(className){
    url = 'http://www.pedrovv.com/studentsIn/'

    fetch(url+className)
        .then(data => data.json())
        .then(success => studentsInClassJSON = success)
        .catch(err => console.log('Something went wrong: ', err));

    return new Promise(resolve => {
        setTimeout(function() {
            resolve(studentsInClassJSON)
            console.log(studentsInClassJSON)
        }, 1000)
        
    })
}

async function getStudentsInClass(className){
    const test = await fetchStudentsInClass(className);
    return studentsInClassJSON;
}




// ******** HELPER FUNCTIONS (GETTERS AND SETTERS) *************
function filterParenthesis (text, max_class) {
    text = text.replace('(', '');
    text = text.replace(')', '');
    for (let i = 0; i < (max_class+1)*3; i++){
        text = text.replace('[', '');
        text = text.replace(']', '');
    }
    for (let i = 0; i < max_class*8; i++){
        text = text.replace("'", '');
    }   
    return text
}

function getMaxClass(array) {

    let max_class = Number.parseInt(array.slice(-2)[0]);
    return max_class;

}

function getSessionCount(array) {
    let count = Number.parseInt(array.slice(-1)[0]);
    return count;
}

function setText(bigRowIndex, rowType, day, text) {
    let row = document.getElementsByClassName(rowType)[bigRowIndex];
    day -= 1;
    console.log(row.children)
    row.children[day].textContent = text;
  }

//i can cut this after testing the other
function getScheduleText(array){
    let count = Number.parseInt(array.slice(-1)[0]);
    //console.log(`this is the count: ${count}`)
    //console.log(array)
    let holder = []
    let teachers = []
    let courses = []
    let counter = 0
    let teachers_index = (-1*count) - 2
    let courses_index = (-2*count) - 2

    for (let i = 0; i < count; i++) {
        holder.push([]);
        teachers.push(array.slice(teachers_index)[0]);
        teachers_index += 1;
        holder[i].push(array.slice(teachers_index)[0]);
    }

    for (let i = 0; i < count; i++) {
        courses.push(array.slice(courses_index)[0]);
        courses_index += 1;
        holder[i].push(array.slice(courses_index)[0]);
    }

    for (let session = 0; session < count; session++){
        for (let i = 0; i < 6; i++) {
            holder[session].push(array[i+counter]);
        }
        counter += 6;
    }
    console.log(teachers)
    console.log(courses)
   

    return [teachers, courses]
}

async function betterGetScheduleText(){
    
    let data = await getClassesJSON();
    //let teachers;
    //setTimeout(() => teachers = Object.keys(classesJSON), 100);
    let courses = await Object.keys(data);
    let teachers = []
    for (i = 0; i < courses.length; i++) {
        teachers.push(data[courses[i]]);
    }

    return [teachers, courses];
}

function getTimeString(start, array, count) {
    let modifier = 1 + count*6
    
    if (start == false) {
        modifier = 2 + modifier;
    }
    
    let time = array[modifier].toString();

    if (array[modifier+1] < 10 || array[modifier+1] == undefined) {
        time += ":0" + array[modifier+1].toString()
    } else {time += ":" + array[modifier+1].toString()}

    return time

}

function getClassfieldSelectedValue(){
    for (let i = 0; i < addDropMenu.length; i++) {
        if (addDropMenu[i].selected == true) {
            return addDropMenu[i].value
        }
    }
}

function setScheduleText(array, teachers_courses){
    
    let count = getSessionCount(listQuery);
    console.log(listQuery)
    console.log(teachers_courses);
    let row_count = new Map();
    let row_to_write = 0;
    let time = "";
    for (let i=0; i<count; i++){
    
        if (row_count[array[i*6]] != undefined) {
            row_count[array[i*6]] += 1;
            row_to_write = row_count[array[i*6]]-1;
            } else {
                row_count[array[i*6]] = 1;
                row_to_write = 0;
            }   
        
        time = getTimeString(true, array, i) + "-" + getTimeString(false, array, i);
        
        
        setText(row_to_write, "class-name", array[(i*6)], teachers_courses[1][i]);
        setText(row_to_write, "time", array[(i*6)], time);
        setText(row_to_write, "room", array[(i*6)], array[(i*6)+5]);
        setText(row_to_write, "teacher", array[(i*6)], teachers_courses[0][i]);
    }
    
}

// *******ENDBLOCK*************

// ********** GENERATOR FUNCTIONS (TABLES, DROPDOWNS) ****************

function generateRoster(roster){
    for (i = 0; i < roster.length; i++) {
        let item = document.createElement('ul');
        
        item.textContent = roster[i]
        betterRoster.appendChild(item);
    }
}

//this can be refactored
function generateClasses(){
    let keys = Object.keys(classesJSON);
    for (i = 0; i < keys.length; i++) {
        let item = document.createElement('ul');    
        item.textContent = keys[i] + ", Teacher: " + classesJSON[keys[i]];
        betterRoster.appendChild(item);
    }
}

function generateScheduleTable(table, max_class) {
    let tbody = document.createElement("TBODY");
    //maybe the x amount of rows gets a special function??
    for (let i = 0; i < max_class; i++) {
        rowCreator(tbody, table);
    }
}

function rowCreator(tbody, table) {
    
    table.appendChild(tbody);
    
    let firstRow = tbody.insertRow();
    firstRow.className = "class-name"
    for (let i = 0; i < 7; i++) {
        firstRow.insertCell();
    }
    let secondRow=tbody.insertRow();
    secondRow.className = "time";
    for (let i = 0; i < 7; i++) {
        secondRow.insertCell();
    }
    let thirdRow=tbody.insertRow();
    thirdRow.className = "room";
    for (let i = 0; i < 7; i++) {
        thirdRow.insertCell();
    }
    
    let fourthRow = tbody.insertRow();
    fourthRow.className = "teacher"
    for (let i = 0; i < 7; i++) {
        fourthRow.insertCell();
    }
    
}

//make a hidden call for all classes available
function generateDropdowns() {
    // for class
    let filteredClasses = filterParenthesis(allClasses, 1);
    filteredClasses = filteredClasses.split(', ');
    let dropdown = document.getElementsByClassName("class-dropdown");
    for (let i = 0; i < dropdown.length; i++){
        select = document.createElement("select");
        select.setAttribute("name", "classfield");
        select.setAttribute("id", "classfield"+"_"+i);
        opt = document.createElement("option");
        optText = document.createTextNode("Classes");
        opt.setAttribute("value", "Classes");
        opt.appendChild(optText);
        select.appendChild(opt);
        for (let i = 0; i < filteredClasses.length; i++){
            opt = document.createElement("option");
            optText = document.createTextNode(filteredClasses[i]);
            
            opt.setAttribute("value", filteredClasses[i]);
            opt.appendChild(optText);
            select.appendChild(opt);
        }
    
        dropdown[i].appendChild(select);
    }

    //for hours

    //i need to target the second dropdown specifically fix
    //or can i abstract this??
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
    

    //room generation

    //session generation  // consider, what is this using from the general
    //function that needs to be here? can i move it out to break
    //dependencies?  
    /*
    classSessions = classSessions.replace('[', '');
    classSessions = classSessions.replace(']', '');
    classSessions = classSessions.split(', ');
    //console.log(classSessions);
    sessionSelect = document.createElement("select");
    sessionSelect.setAttribute("name", "sessionfield");
    for (let i = 0; i < classSessions.length; i++) {
        opt = document.createElement("option");
        optText = document.createTextNode(classSessions[i]);
        opt.setAttribute("value", i);
        opt.appendChild(optText);
        sessionSelect.appendChild(opt);
    }*/
    // is this text supposed the filler text? and the set
    // attribute text?
    /*
    selected = document.getElementById('classfield_1').selectedOptions[0].value;
    addText = document.createTextNode(selected);
    //come back here
    document.getElementById('add-class').appendChild(addText);
    document.getElementById('remove-time').setAttribute("value", addText)
    document.getElementById('remove-time').setAttribute("name", 'drop-confirm')
    newText = addText + " session to drop"
    newText = document.createTextNode(newText);
    document.getElementById('remove-time').appendChild(newText);
    document.getElementById('remove-time').appendChild(sessionSelect);*/
}


function generateSessionDropdown() {
   
    // fix this
    /* should'nt get classsessions, should fetch text*/
    /*let classSessions = document.getElementById("class-sessions").textContent;
    classSessions = classSessions.replace('[', '');
    classSessions = classSessions.replace(']', '');
    classSessions = classSessions.split(', ');*/
    let classSessions = sessionJSON.sessions
    console.log("pita chips")
    //this code will go in the call
    //console.log("inside the function")
    //console.log(classSessions);

    //fix alright so what needs to happen is a conditional for remove, and a conditional for modify
    if (classSessions.length == 0) {
        window.alert("No class sessions to change for this class!");
        let modifyTime = document.getElementById('modify-block');
        modifyTime.style.display="none";

    }
    if (classSessions.length != 0) {
        /*
        let sessionSelect = document.createElement("select");
        sessionSelect.setAttribute("name", "sessionfield");
        for (let i = 0; i < classSessions.length; i++) {
            opt = document.createElement("option");
            optText = document.createTextNode(classSessions[i]);
            opt.setAttribute("value", i);
            //opt.setAttribute("id", "sessionfield_"+i);
            opt.appendChild(optText);
            sessionSelect.appendChild(opt);
        }
        let removeTime = document.getElementById('remove-time');
        let modifyTime = document.getElementById('modify-time');
        let sessionClone = sessionSelect.cloneNode()
        console.log(sessionSelect);
        console.log(sessionClone);
        removeTime.appendChild(sessionSelect);
        modifyTime.appendChild(sessionClone);

        */
        oneSessionGenerator('remove-time', classSessions);
        oneSessionGenerator('modify-time', classSessions);
        let removeTime = document.getElementById('remove-time');
        let modifyTime = document.getElementById('modify-time');
        let classToRemove = sessionStorage.getItem('classfield');
        let classToRemoveText = document.createTextNode(" " + classToRemove + " session to remove");
        removeTime.appendChild(classToRemoveText);
       
       

        if (sessionStorage.getItem("drop")==="true" && 
            sessionStorage.getItem("classfield") != "Classes"){
                dropTime.style.display = "block";
            } else {
                dropTime.style.display = "none";
        }

        if (sessionStorage.getItem("modify")==="true" && 
            sessionStorage.getItem("classfield") != "Classes"){
                modifyTime.style.display = "block";
            } else {
                modifyTime.style.display = "none";
        }
    } else if (sessionStorage.getItem("add") != "true" && sessionStorage.getItem("view") != "true" &&
        sessionStorage.getItem("addDrop") != "true" && (sessionStorage.getItem("modify") == "true"
        || sessionStorage.getItem("drop") == "true")) {

        errorClass = sessionStorage.getItem("classfield");
        window.alert(`There are no ${errorClass} class sessions to drop`);
    }

}

function oneSessionGenerator(session, classSessions){
    let sessionSelect = document.createElement("select");
    sessionSelect.setAttribute("name", "sessionfield");
    for (let i = 0; i < classSessions.length; i++) {
        opt = document.createElement("option");
        optText = document.createTextNode(classSessions[i]);
        opt.setAttribute("value", i);
        //opt.setAttribute("id", "sessionfield_"+i);
        opt.appendChild(optText);
        sessionSelect.appendChild(opt);
    }
    let timeNode = document.getElementById(session);
    timeNode.appendChild(sessionSelect);
  
}


// **********ENDBLOCK ***************

//******* INVOCATION TO GENERATE ********

generateDropdowns();
schedule.style.display = "none";



//Name of code block,**** GENERATE BASIC SCHEDULE ON LOAD ******
//info needed: dataText, schedule?,
//what does this code do
/*
    1. Sets schedule to visible
    2. parses text using filterParenthesis Function
    3. generatesScheduleTable with that function and with getMaxClass function
    4. uses a weirdly named getScheduleText (could use JSON instead?)
    5. sets schedule text with function
    6. this all happens regardless of whether the user views it or not
        they are immediate generations on the known queries
*/


async function scheduleControlFlow(){

    let option = document.getElementById("option").textContent

    if (option==='View Schedule of a Student' || option==='View Schedule of a Teacher'
    || option=== 'View Schedule of a Class' || option==='View master schedule (days)'){

        temp = dataText.split(', ');
        max_class = parseInt(temp.slice(-2)[0]);
        query = filterParenthesis(dataText, max_class);
        listQuery = query.split(', ');

        
        generateScheduleTable(schedule, getMaxClass(listQuery));
        let teachers_courses = await betterGetScheduleText();
        setScheduleText(listQuery, teachers_courses);
        schedule.style.display = "";
    }
}

scheduleControlFlow();
/*
if (option==='View Schedule of a Student' || option==='View Schedule of a Teacher'
    || option=== 'View Schedule of a Class' || option==='View master schedule (days)'){
    schedule.style.display = "";
    getClassesJSON();
    temp = dataText.split(', ');
    
    max_class = parseInt(temp.slice(-2)[0]);
    query = filterParenthesis(dataText, max_class);
    listQuery = query.split(', ');
    generateScheduleTable(schedule, getMaxClass(listQuery));

    // provisional test
    let teachers_courses = getScheduleText(listQuery);
    //let teachers_courses = betterGetScheduleText();
    //console.log(teachers_courses);
    //let's try phasing out teachers_courses
    setScheduleText(listQuery, teachers_courses);
    //setTimeout(() => setScheduleText(listQuery, teachers_courses), 1000);
    
    //console.log('**********');
    //what is this else for?
    } else {
        dataText = dataText.replace('[', '');
        dataText = dataText.replace(']', '');
        temp = dataText.split(', ');
        console.log(temp);
        for (let i=0; i<temp.length; i++){
            item = document.createElement("li");
            item.textContent = temp[i];
            //let text = document.createTextNode(data[i])
            roster.appendChild(item);
        }
}
*/
// ******END CODE BLOCK*************


// ******UNCONFIRMED IMPLEMENTATION LOGIC FOR BUTTONS***********

// review / fix this see if it can get cut
/*if (sessionStorage.getItem('classfield')==="None"||
    sessionStorage.getItem('classfield')==="Classes") {
    dropTime.style.display = "none";
    } else {
        dropTime.style.display = "block";
    }*/


/* *******what is this about?*********
document.getElementById('remove-time').setAttribute("value", dropText)
document.getElementById('remove-time').setAttribute("name", 'drop-confirm')
newText = dropText + " session to drop"
newText = document.createTextNode(dropText);
document.getElementById('remove-time').appendChild(dropText);
document.getElementById('remove-time').appendChild(sessionSelect);*/

let addDropMenu = document.getElementById('classfield_1').options;
let testSelected = document.getElementById('classfield_1').selectedOptions[0].value;

dropText = document.createTextNode(testSelected);

for (let i = 0; i < addDropMenu.length; i++) {
    if (addDropMenu[i].value === sessionStorage.getItem('classfield')) {
        addDropMenu[i].selected = true;
        break;
    }
}



// ******** BUTTON LOGIC **********

//viewBtn.onclick = viewLogic;
addDropBtn.onclick = addDropLogic;

viewBtn.onclick = function(){
    sessionStorage.setItem("view", true);
    sessionStorage.setItem("add", false);
    sessionStorage.setItem("drop", false);
    sessionStorage.setItem("modify", false);
    sessionStorage.setItem("createSessions", false);
    
    let viewQueries = document.getElementById("queries");
    let viewSelected = viewQueries.selectedOptions[0].value;
    
    //sessionStorage.setItem("viewSelected", viewSelected);
    if (viewSelected == "View All Students"){
        sessionStorage.setItem("viewRoster", true);
        sessionStorage.setItem("viewValue", viewSelected);
    } else if (viewSelected == "View All Teachers"){
        sessionStorage.setItem("viewRoster", true);
        sessionStorage.setItem("viewValue", viewSelected);
    } else if (viewSelected == "View All Classes"){
        sessionStorage.setItem("viewRoster", true);
        sessionStorage.setItem("viewValue", viewSelected);
    } else if (viewSelected == "View All Students in a Class"){
        sessionStorage.setItem("viewRoster", true);
        sessionStorage.setItem("viewValue", viewSelected);
    } else {
        sessionStorage.setItem("viewRoster", false)
    }
}
if (sessionStorage.getItem('viewValue') == "View All Students"){

    document.getElementById("queries").value = sessionStorage.getItem('viewValue');
    getRosterJSON();
    setTimeout(() => generateRoster(rosterJSON.students), 1000);
    
} else if (sessionStorage.getItem('viewValue') == "View All Teachers"){

    document.getElementById("queries").value = sessionStorage.getItem('viewValue');
    getRosterJSON();
    setTimeout(() => generateRoster(rosterJSON.teachers), 1000);
    
} else if (sessionStorage.getItem('viewValue') == "View All Classes"){

    document.getElementById("queries").value = sessionStorage.getItem('viewValue');
    getClassesJSON();
    setTimeout(() => generateClasses(), 1000);
    
} else if (sessionStorage.getItem('viewValue') == "View All Students in a Class"){

    document.getElementById("queries").value = sessionStorage.getItem('viewValue');
    let searchField = document.getElementById('viewField').value;
    getStudentsInClass(searchField);
    setTimeout(() => generateRoster(studentsInClassJSON), 1000);
    
} 

async function studentsInClassFlow(){
    if (sessionStorage.getItem('viewValue') == "View All Students in a Class"){
        document.getElementById("queries").value = sessionStorage.getItem('viewValue');
        let searchField = document.getElementById('viewField').value;
        let getStudents = await getStudentsInClass(searchField);
        generateRoster(getStudents);

    }
}

studentsInClassFlow();

if (sessionStorage.getItem("viewRoster") == "true") {
    betterRoster.style.display = "";
} else {
    betterRoster.style.display = "none";
}

function addDropLogic(){
    sessionStorage.setItem("addDrop", true);
}





// ******** ADD LOGIC **********



addBtn.onclick = addLogic;
function addLogic (){ 
    sessionStorage.setItem("test", "this is working");
    let classfield = document.getElementById("classfield_1");
    let selected = classfield.selectedOptions;
    sessionStorage.setItem("add", true);
    sessionStorage.setItem("drop", false);
    sessionStorage.setItem("modify", false);
    sessionStorage.setItem("view", false);

    // fix naming for this to be more genereal (the drop ref)
    sessionStorage.setItem("classfield", selected[0].value);
    addText = document.createTextNode(selected[0].value);
    document.getElementById('add-class').appendChild(addText); 
    if (dropTime.style.display === "block") {
        dropTime.style.display === "none";
        }
    }

if (sessionStorage.getItem("add")==="true" && 
    sessionStorage.getItem("classfield") != "Classes"){
        addTime.style.display = "block";
        } else {
            addTime.style.display = "none";
    }
let addClass = document.getElementById('add-class');
let addClassText = document.createTextNode(sessionStorage.getItem("classfield"));
addClass.appendChild(addClassText);

confirmAdd.onclick = function(){ 
    sessionStorage.setItem("classfield", "Classes");
    sessionStorage.setItem("add", false);
    }


//this doesn't work unless i delay a bit
//sessionStorage.setItem('sessionJSON', JSON.stringify(sessionJSON));

// so the idea, would be to make a string of promises?

//window.alert(sessionJSON);
/*
let myPromiseToYou = Promise.resolve(awaitValidJSON());
myPromiseToYou.then(test => console.log(`My promise to you: ${test}`));
//setTimeout(() => window.alert(sessionJSON.sessions), 3000);

function awaitValidJSON() {
    
    for(i = 0; i<3; i++){      
        setTimeout(() => console.log(sessionJSON), 1000);
        //window.alert(`it's ready! ${i}`);
    }
    
}*/



dropBtn.onclick = function(){ 

    sessionStorage.setItem("createSessions", true);
    sessionStorage.setItem("add", false);
    sessionStorage.setItem("modify", false);
    sessionStorage.setItem("drop", true);
    sessionStorage.setItem("view", false);
    //test line
    //
    
    let classfield = document.getElementById("classfield_1");
    let selected = classfield.selectedOptions;
    if (selected[0].value != "Classes"){
        sessionStorage.setItem("classfield", selected[0].value);
    }  
}
console.log('******')


confirmDrop.onclick = function(){ 
    sessionStorage.setItem("classfield", "Classes");
    sessionStorage.setItem("drop", false);
    }

// ******** MODIFY LOGIC **********

// will need a session style dropdown too

modifyBtn.onclick = modifyLogic;
function modifyLogic (){
    let classfield = document.getElementById("classfield_2");
    let selected = classfield.selectedOptions;
    sessionStorage.setItem("createSessions", true);
    sessionStorage.setItem("add", false);
    sessionStorage.setItem("drop", false);
    sessionStorage.setItem("modify", true);
    sessionStorage.setItem("view", false); 

    

    // fix naming for this to be more genereal (the drop ref)
    sessionStorage.setItem("classfield", selected[0].value);
    modifyText = document.createTextNode(selected[0].value);
    document.getElementById('modify-class').appendChild(modifyText); 
    if (dropTime.style.display === "block") {
        dropTime.style.display === "none";
    }

}

if (sessionStorage.getItem("modify")=="true") {

    document.getElementById('classfield_2').value = sessionStorage.getItem("classfield");
}

if (sessionStorage.getItem("modify")==="true" && 
    sessionStorage.getItem("classfield") != "Classes"){
        modifyTime.style.display = "block";
        } else {
            modifyTime.style.display = "none";
    }
let modifyClass = document.getElementById('modify-class');
let modifyClassText = document.createTextNode(sessionStorage.getItem("classfield"));
modifyClass.appendChild(modifyClassText);

confirmModify.onclick = function(){ 
    sessionStorage.setItem("classfield", "Classes");
    sessionStorage.setItem("modify", false);
    }   

if (sessionStorage.getItem('createSessions') == 'true' && 
    sessionStorage.getItem("classfield") != "Classes") {
    //awaitValidJSON();
    getSessionJSON();
    setTimeout(() => generateSessionDropdown(), 500);
    //generateSessionDropdown();
   
}




// generateSessionDropdown() sets sessionfield
//this might be throwing an error
/*
if (document.getElementById("sessionfield_0").textContent==""){
        sessionStorage.setItem("null", true);     
    } else {
            sessionStorage.setItem("null", false);
        }
*/

//changing this to fix
/*if (sessionStorage.getItem("drop")==="true" && 
    sessionStorage.getItem("classfield") != "Classes" &&
    sessionStorage.getItem("null")!="true"){
        
        dropTime.style.display = "block";
        } else {
            dropTime.style.display = "none";
    }*/


// ***********








/*selected = document.getElementById('classfield_1').selectedOptions[0].value;
addText = document.createTextNode(selected);
//come back here
document.getElementById('add-class').appendChild(addText);
document.getElementById('remove-time').setAttribute("value", addText)
document.getElementById('remove-time').setAttribute("name", 'drop-confirm')
newText = addText + " session to drop"
newText = document.createTextNode(newText);
document.getElementById('remove-time').appendChild(newText);
document.getElementById('remove-time').appendChild(sessionSelect);*/







/*

domtoimage.toPng(table)
    .then (function (dataUrl) {
        let img = new Image();
        img.src = dataUrl;
        document.appendChild(img);
    })
    .catch(function (error) {
        console.error('oops, something went wrong!', error);
    });

domtoimage.toJpeg(table, { quality: 0.95 })
    .then(function (dataUrl) {
        let link = document.createElement('a');
        link.download = 'my-image-name.jpeg';
        link.href = dataUrl;
        link.click();
    });*/



/*

function rowCreatorWithLeftBumper(class_name, tbody, table) {
    let firstRow = tbody.insertRow();
    firstRow.className = "time"
    let course = firstRow.insertCell()
    course.className = "course";
    course.rowSpan = "3";
    let courseName = document.createTextNode(class_name);
    table.appendChild(tbody);
    course.appendChild(courseName);
    for (let i = 0; i < 7; i++) {
        firstRow.insertCell();
    }
    let secondRow=tbody.insertRow();
    secondRow.className = "room";
    for (let i = 0; i < 7; i++) {
        secondRow.insertCell();
    }
    let thirdRow=tbody.insertRow();
    thirdRow.className = "teacher";
    for (let i = 0; i < 7; i++) {
        thirdRow.insertCell();
    }
}

function setTextWithBumper(bigRowIndex, rowType, day, text) {
    let row = document.getElementsByClassName(rowType)[bigRowIndex]
    if (rowType != "time") {day -= 1}
    row.children[day].textContent = text;
  }



function removeAllChildNodes(parent) {
    while (parent.firstChild) {
        parent.removeChild(parent.firstChild);
        }
}

function makeVisible(element){
    
    if (element.style.display==="none"){
        if (element === addTime){
            if (dropTime.style.display==="block"){             
                dropTime.style.display="none"
            }
            element.style.display="block";
        }

        if (element === dropTime){
            if (addTime.style.display==="block"){
                addTime.style.display="none"
            }
            element.style.display="block";
        }

    } else {
        element.style.display="none";
    }
    
}*/
