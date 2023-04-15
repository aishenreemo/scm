const USER_TYPE = Object.freeze({
    Admin: 0,
    Viewer: 1,
});
const MENU_TYPE = Object.freeze({
    Data: 0,
    Record: 1,
    Delete: 2,
});

const ADMIN_USERNAME = "";
const ADMIN_PASSWORD = "";
const VIEWER_USERNAME = "viewer";
const VIEWER_PASSWORD = "123";

let memory = {};

let userType = USER_TYPE.Viewer;

let loginPage = document.querySelector(".login-page");
let mainPage = document.querySelector(".main-page");
let studentListWindow = document.querySelector(".student-list-window");
let studentInfoWindow = document.querySelector(".student-info-window");
let sectionList = studentListWindow.querySelector(".section-list");
let studentList = studentListWindow.querySelector(".student-list");
let searchList = studentListWindow.querySelector(".search-list");
let menuDivs = [""]

function login() {
    let errorDiv = document.querySelector(".login > .error");

    if (!validateCredentials()) {
        errorDiv.innerText = "Invalid username or password.";

        return;
    }

    loginPage.classList.add("invisible");
    mainPage.classList.remove("invisible");
    studentInfoWindow.classList.add("invisible");
    studentListWindow.classList.remove("invisible");
    studentList.classList.add("invisible");
    sectionList.classList.add("invisible");
    searchList.classList.add("invisible");
}

function logout() {
    loginPage.classList.remove("invisible");
    mainPage.classList.add("invisible");
    mainPage.querySelector(".header > .options").style.display = "none";

    let panes = [ ".data", ".record", ".delete" ].map(selectPane);

    for (let i = 0; i < panes.length; i++) {
        let pane = panes[i];

        pane.classList.add("invisible");

        if (i == MENU_TYPE.Data) {
            pane.classList.remove("invisible");
        }
    }
}

function validateCredentials() {
    let usernameDiv = document.querySelector(".login > .username");
    let passwordDiv = document.querySelector(".login > .password");

    let valid = false;

    if (usernameDiv.value == ADMIN_USERNAME && passwordDiv.value == ADMIN_PASSWORD) {
        userType = USER_TYPE.Admin;
        valid = true;
    } else if (usernameDiv.value == VIEWER_USERNAME && passwordDiv.value == VIEWER_PASSWORD) {
        userType = USER_TYPE.Viewer;
        valid = true;
    }

    usernameDiv.value = "";
    passwordDiv.value = "";

    return valid;
}

async function showSectionList(gradeLevel) {
    let apiUrl = `http://localhost:3000/sections/${gradeLevel}`;
    let response = await fetch(apiUrl);
    let json = await response.json();
    let rect = sectionList.querySelector(".rect");

    studentList.classList.add("invisible");
    searchList.classList.add("invisible");
    sectionList.classList.remove("invisible");

    while (rect.firstChild) rect.firstChild.remove();

    for (let i = 0; i < json.length; i++) {
        let button = document.createElement("button");
        button.dataset.section = json[i];
        button.dataset.gradeLevel = gradeLevel;
        button.innerText = json[i].toUpperCase();
        button.classList.add("unselectable");
        button.addEventListener("click", sectionOnClick);

        rect.appendChild(button);
    }
}

async function sectionOnClick() {
    let apiUrl = `http://localhost:3000/students/${this.dataset.gradeLevel}/${this.dataset.section}`;
    let response = await fetch(apiUrl);
    let json = await response.json();

    let boys = studentList.querySelector(".boys > .rect");
    let girls = studentList.querySelector(".girls > .rect");

    while (boys.firstChild) boys.firstChild.remove();
    while (girls.firstChild) girls.firstChild.remove();

    sectionList.classList.add("invisible");
    searchList.classList.add("invisible");
    studentList.classList.remove("invisible");

    for (let i = 0; i < json.length; i++) {
        let name = json[i].name
        let rect = json[i].gender == 0 ? boys : girls;
        let button = document.createElement("button");
        button.dataset.name = `${name.last}, ${name.first} ${name.middle}`;
        button.dataset.id = json[i]._id;
        button.innerText = button.dataset.name;
        button.classList.add("unselectable");
        button.addEventListener("click", studentOnClick);

        rect.appendChild(button);
    }
}

async function studentOnClick() {
    let apiUrl = `http://localhost:3000/student/${this.dataset.id}`;
    let response = await fetch(apiUrl);
    let json = await response.json();

    studentInfoWindow.classList.remove("invisible");
    studentListWindow.classList.add("invisible");

    let data = selectPane(".data");
    let map = {
        ".student > .name": `${json.name.last}, ${json.name.first} ${json.name.middle} ${json.name.suffix}`,
        ".student > .grade": `${json.grade_level + 7}`,
        ".student > .section": json.section,
        ".student > .gender": json.gender == 0 ? "Male" : "Female",
    };

    for (let [key, value] of Object.entries(map)) {
        let input = data.querySelector(`${key} > input`);
        input.value = value || "N/A";
    }
}

function selectPane(pane) {
    return studentInfoWindow.querySelector(pane);
}

function showMenu(menuType) {
    let panes = [ ".data", ".record", ".delete" ].map(selectPane);

    for (let i = 0; i < panes.length; i++) panes[i].classList.add("invisible");

    let pane = panes[menuType];
    pane.classList.remove("invisible");
}

function backFromInfo() {
    let panes = [ ".data", ".record", ".delete" ].map(selectPane);

    for (let i = 0; i < panes.length; i++) {
        let pane = panes[i];

        pane.classList.add("invisible");

        if (i == MENU_TYPE.Data) {
            pane.classList.remove("invisible");
        }
    }

    studentInfoWindow.classList.add("invisible");
    studentListWindow.classList.remove("invisible");
}

async function search() {
    let searchValue = mainPage.querySelector(".search > input").value;
    let apiUrl = `http://localhost:3000/search/${searchValue}`;
    let response = await fetch(apiUrl);
    let json = await response.json();
    let rect = searchList.querySelector(".rect");

    studentInfoWindow.classList.add("invisible");
    studentListWindow.classList.remove("invisible");
    sectionList.classList.add("invisible");
    studentList.classList.add("invisible");
    searchList.classList.remove("invisible");

    while (rect.firstChild) rect.firstChild.remove();

    for (let i = 0; i < json.length; i++) {
        let name = json[i].name
        let button = document.createElement("button");

        button.dataset.name = `${name.last}, ${name.first} ${name.middle}`;
        button.dataset.id = json[i]._id;
        button.innerText = button.dataset.name;
        button.classList.add("unselectable");
        button.addEventListener("click", studentOnClick);

        rect.appendChild(button);
    }
}

function toggleMenu() {
    let options = mainPage.querySelector(".header > .options");

    if (options.style.display == "flex") {
        options.style.display = "none";
    } else {
        options.style.display = "flex";
    }
}

function printStudentData() {
    window.electronAPI.print("test");
}
