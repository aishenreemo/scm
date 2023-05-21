const USER_TYPE = Object.freeze({
    Admin: 0,
    Viewer: 1,
});
const MENU_TYPE = Object.freeze({
    Data: 0,
    AddRecord: 1,
    ListRecords: 2,
    Delete: 3,
});

const ADMIN_USERNAME = "admin";
const ADMIN_PASSWORD = "123";
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
let addRecordForm = selectPane(".add > form");
let menuDivs = [""]

async function login() {
    let errorDiv = document.querySelector(".login > .error");

    if (!(await validateCredentials())) {
        errorDiv.innerText = "Invalid username or password.";

        return;
    }

    errorDiv.innerText = "";
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
    document.querySelector(".register").classList.add("invisible");
    addRecordForm.reset();
    mainPage.querySelector(".header > .options").style.display = "none";

    let panes = [ ".data", ".add", ".records", ".delete" ].map(selectPane);

    for (let i = 0; i < panes.length; i++) {
        let pane = panes[i];

        pane.classList.add("invisible");

        if (i == MENU_TYPE.Data) {
            pane.classList.remove("invisible");
        }
    }
}

async function validateCredentials() {
    let usernameDiv = document.querySelector(".login > .username");
    let passwordDiv = document.querySelector(".login > .password");

    let valid = false;

    let adminOnlyElements = document.querySelectorAll(".admin-only");
    if (usernameDiv.value == ADMIN_USERNAME && passwordDiv.value == ADMIN_PASSWORD) {
        userType = USER_TYPE.Admin;
        valid = true;

        for (let i = 0; i < adminOnlyElements.length; i++) {
            let element = adminOnlyElements[i];
            element.style.display = "inline";
        }
    } else if (usernameDiv.value == VIEWER_USERNAME && passwordDiv.value == VIEWER_PASSWORD) {
        userType = USER_TYPE.Viewer;
        valid = true;

        for (let i = 0; i < adminOnlyElements.length; i++) {
            let element = adminOnlyElements[i];
            element.style.display = "none";
        }
    } else {
        let response = await fetch("http://localhost:3000/login", { 
            method: "POST", 
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ email: usernameDiv.value, password: passwordDiv.value }),
        });
        let data = await response.json();

        if (response.status == 200) {
            userType = data.user.admin ? USER_TYPE.Admin : USER_TYPE.Viewer;

            for (let i = 0; i < adminOnlyElements.length; i++) {
                let element = adminOnlyElements[i];
                element.style.display = data.user.admin ? "inline" : "none";
            }
            usernameDiv.value = "";
            valid = true;
        } else if (response.status == 401) {
            document.querySelector(".forgot").classList.remove("invisible");
        } else {
            usernameDiv.value = "";
        }
    }

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
    let apiUrl = `http://localhost:3000/get/${this.dataset.id}`;
    let response = await fetch(apiUrl);
    let json = await response.json();

    studentInfoWindow.classList.remove("invisible");
    studentListWindow.classList.add("invisible");

    let data = selectPane(".data");

    let map = {
        ".name > input": `${json.name.last}, ${json.name.first} ${json.name.middle} ${json.name.suffix}`,
        ".grade > input": `${json.grade_level + 7}`,
        ".section > input": json.section,
        ".gender > input": json.gender == 0 ? "Male" : "Female",
        ".address > input": json.address,
        ".religion > input": json.religion,
        ".nationality > input": json.nationality,
        ".birth-date > input": json.birth?.date,
        ".birth-place > input": json.birth?.place,
        ".father > input": json.father?.name,
        ".father-contact-no > input": json.father?.contact,
        ".mother > input": json.mother?.name,
        ".mother-contact-no > input": json.mother?.contact,
        ".immunization-has-flu > input": json.immunization?.flu,
        ".immunization-has-hepatitis > input": json.immunization?.hepatitis,
        ".immunization-has-varicella > input": json.immunization?.varicella,
        ".immunization-has-meningococcal > input": json.immunization?.meningococcal,
        ".immunization-has-pneunomococcal > input": json.immunization?.pneunomococcal,
        ".immunization-has-hpv > input": json.immunization?.hpv,
        ".immunization-remarks > textarea": json.immunization?.remarks,
        ".brand-first-dose > input": json.vaccination?.first,
        ".brand-second-dose > input": json.vaccination?.second,
        ".brand-booster > input": json.vaccination?.booster,
        ".brand-remarks > textarea": json.vaccination?.remarks,
        ".brand-reason > textarea": json.vaccination?.reason,
        ".brand-household > input[value='1']": json.vaccination?.household,
        ".brand-household > input[value='0']": !json.vaccination?.household,
        ".brand-household-reason > textarea": json.vaccination?.household_reason,
        "textarea[name='allergies-list']": json.medical_history?.allergies,
        "input[name='medication-has-meds'][value='1']": json.medical_history?.medication?.has_meds,
        "input[name='medication-has-meds'][value='0']": !json.medical_history?.medication?.has_meds,
        "input[name='medication-name']": json.medical_history?.medication?.name,
        "input[name='medication-treat']": json.medical_history?.medication?.treat,
        "input[name='medication-dose']": json.medical_history?.medication?.dose,
        "input[name='condition-headache']": json.medical_history?.conditions?.headache,
        "input[name='condition-toothache']": json.medical_history?.conditions?.toothache,
        "input[name='condition-fever']": json.medical_history?.conditions?.fever,
        "input[name='condition-rhinitis']": json.medical_history?.conditions?.rhinitis,
        "input[name='condition-stomach-ache']": json.medical_history?.conditions?.stomach_ache,
        "textarea[name='condition-others']": json.medical_history?.conditions?.others,
        "textarea[name='treatment-current']": json.medical_history?.ongoing_treatment,
        "input[name='pe-cant-participate'][value='1']": !!json.medical_history?.sport_limitations,
        "input[name='pe-cant-participate'][value='0']": !json.medical_history?.sport_limitations,
        "textarea[name='pe-cant-reason']": json.medical_history?.sport_limitations,
        "input[name='visual-has-difficulties'][value='1']": json.medical_history?.visual_limitations?.glasses || json.medical_history?.visual_limitations?.contact_lenses,
        "input[name='visual-has-difficulties'][value='0']": !json.medical_history?.visual_limitations?.glasses && !json.medical_history?.visual_limitations?.contact_lenses,
        "input[name='visual-contact-lenses']": json.medical_history?.visual_limitations?.contact_lenses,
        "input[name='visual-glasses']": json.medical_history?.visual_limitations?.glasses,
        "input[name='hearing-has-difficulties'][value='1']": !!json.medical_history?.language_limitations,
        "input[name='hearing-has-difficulties'][value='0']": !json.medical_history?.language_limitations,
        "textarea[name='hearing-details']": json.medical_history?.language_limitations,
        "input[name='other-backaches']": json.medical_history?.other_limitations?.backaches,
        "input[name='other-chest-pain']": json.medical_history?.other_limitations?.chest_pain,
        "input[name='other-cough']": json.medical_history?.other_limitations?.cough,
        "input[name='other-cyclic-vomiting']": json.medical_history?.other_limitations?.cyclic_vomiting,
        "input[name='other-depression']": json.medical_history?.other_limitations?.depression,
        "input[name='other-difficulty-of-breathing']": json.medical_history?.other_limitations?.difficulty_of_breathing,
        "input[name='other-dizziness']": json.medical_history?.other_limitations?.dizziness,
        "input[name='other-epistaxis']": json.medical_history?.other_limitations?.epistaxis,
        "input[name='other-eczema']": json.medical_history?.other_limitations?.eczema,
        "input[name='other-fainting-spells']": json.medical_history?.other_limitations?.fainting_spells,
        "input[name='other-headaches']": json.medical_history?.other_limitations?.headaches,
        "input[name='other-insomias']": json.medical_history?.other_limitations?.insomias,
        "input[name='other-joint-pains']": json.medical_history?.other_limitations?.join_pains,
        "input[name='other-recurrent-abdominal-pain']": json.medical_history?.other_limitations?.recurrent_abdominal_pain,
        "input[name='other-seizure']": json.medical_history?.other_limitations?.seizure,
        "input[name='other-urinary-problems']": json.medical_history?.other_limitations?.urinary_problems,
        "input[name='other-weight-lost']": json.medical_history?.other_limitations?.weight_lost,
        "input[name='other-others']": json.medical_history?.other_limitations?.others,
        "textarea[name='drugs-taken']": json.medical_history?.drugs_taken,
        "textarea[name='other-info']": json.medical_history?.other_info,
    };

    data.dataset.id = json._id;

    for (let [key, value] of Object.entries(map)) {
        let element = data.querySelector(key);

        if (element.tagName == "INPUT" && element.getAttribute("type") == "checkbox") {
            element.checked = value;
            continue;
        }

        if (element.tagName == "INPUT" && element.getAttribute("type") == "radio") {
            element.checked = value;
            continue;
        }

        if (element.tagName == "INPUT") {
            element.value = value || "N/A";

            continue;
        } 

        if (element.tagName == "TEXTAREA") {
            element.innerText = value || "N/A";
        }
    }

    updateListRecords(json);
}

function updateListRecords(json) {
    let records = selectPane(".records > .flex");
    while (records.firstChild) records.firstChild.remove();

    for (let i = 0; i < (json.records?.length || 0); i++) {
        let record = json.records[i];
        let div = document.createElement("div");

        div.classList.add("record");
        div.innerHTML = `
            <div><label>IN:</label><input type="time" value="${record.in}" readonly></div>
            <div><label>OUT:</label><input type="time" value="${record.out}" readonly></div>
            <div><label>DATE:</label><input type="date" value="${record.date}" readonly></div>
            <div class="block">
            <label>REASON/CAUSE:</label>
            <textarea rows="4" readonly>${record.reason}</textarea>
            </div>
            <div class="block">
            <label>TREATMENT:</label>
            <textarea rows="4" readonly>${record.treatment}</textarea>
            </div>
            `;

        let button = document.createElement("button");

        button.addEventListener("click", deleteRecordFunc(i));
        button.setAttribute("type", "button");
        button.innerText = "DELETE";

        div.appendChild(button);
        records.appendChild(div);
    }

}

function deleteRecordFunc(i) {
    return async () => {
        if (userType == USER_TYPE.Viewer) return;

        let id = selectPane(".data").dataset.id;
        let body = { i, id };

        await fetch("http://localhost:3000/delete_record", { 
            method: "POST", 
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            body: JSON.stringify(body),
        });

        let apiUrl = `http://localhost:3000/get/${id}`;
        let response = await fetch(apiUrl);
        let json = await response.json();
        updateListRecords(json);
        showMenu(MENU_TYPE.Data);
    }
}

function selectPane(pane) {
    return studentInfoWindow.querySelector(pane);
}

function showMenu(menuType) {
    let panes = [ ".data", ".add", ".records", ".delete" ].map(selectPane);

    for (let i = 0; i < panes.length; i++) {
        panes[i].classList.add("invisible");
    }

    let pane = panes[menuType];
    pane.classList.remove("invisible");
}

function backFromInfo() {
    let panes = [ ".data", ".add", ".records", ".delete" ].map(selectPane);

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

async function printStudentData() {
    let id = selectPane(".data").dataset.id;
    let apiUrl = `http://localhost:3000/get/${id}`;
    let response = await fetch(apiUrl);
    let json = await response.json();

    window.electronAPI.print(json);
}

async function deleteAll() {
    if (userType == USER_TYPE.Viewer) return;

    await fetch("http://localhost:3000/delete_all", { method: "POST" });
}

async function deleteStudent() {
    if (userType == USER_TYPE.Viewer) return;

    let data = selectPane(".data");
    let body = { id: data.dataset.id };

    await fetch("http://localhost:3000/delete", { 
        method: "POST", 
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        body: JSON.stringify(body),
    });

    sectionList.classList.add("invisible");
    studentList.classList.add("invisible");
    searchList.classList.add("invisible");
    backFromInfo();
}

addRecordForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    if (userType == USER_TYPE.Viewer) return;

    let data = Object.fromEntries(new FormData(addRecordForm));
    let id = selectPane(".data").dataset.id;

    let body = { data, id };

    await fetch("http://localhost:3000/add_record", { 
        method: "POST", 
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        body: JSON.stringify(body),
    });

    addRecordForm.reset();

    let apiUrl = `http://localhost:3000/get/${id}`;
    let response = await fetch(apiUrl);
    let json = await response.json();
    updateListRecords(json);
    showMenu(MENU_TYPE.Data);
});

document.querySelector(".create").addEventListener("click", () => {
    const register = document.querySelector(".register");
    register.classList.remove("invisible");
    register.dataset.admin = false;
})

document.querySelector(".create-admin").addEventListener("click", () => {
    const register = document.querySelector(".register");
    register.classList.remove("invisible");
    register.dataset.admin = true;
})

document.querySelector(".register-btn").addEventListener("click", async () => {
    const register = document.querySelector(".register");
    const email = register.querySelector(".username").value;
    const password = register.querySelector(".password").value;
    const admin = register.dataset.admin;

    try {
        const response = await fetch("http://localhost:3000/register", {
            method: "POST",
            credentials: "include",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email,
                password,
                admin,
            })
        });

        const data = await response.json();

        if (response.status == 201) return logout();

        register.querySelector(".error").innerText = data.message;
    } catch (err) {
        console.error(err);
    }
})
