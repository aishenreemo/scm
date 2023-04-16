const form = document.querySelector(".form.page");
const thankYou = document.querySelector(".thank-you.page");
const dataContentPrivacy = document.querySelector(".data-content-privacy.page");
const studentHealthRecord = document.querySelector(".student-health-record.page");

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    let data = Object.fromEntries(new FormData(form));
    let serialized = {
        name: {
            last: data["name-last"],
            first: data["name-first"],
            middle: data["name-middle"],
            suffix: data["name-suffix"],
        },
        birth: {
            date: data["birth-date"],
            place: data["birth-place"]
        },
        father: {
            name: data["father-name"],
            contact: data["father-contact"],
        },
        mother: {
            name: data["mother-name"],
            contact: data["mother-contact"],
        },
        section: data["grade-section"],
        address: data["address"],
        religion: data["religion"],
        nationality: data["nationality"],
        contact: data["contact"],
        grade_level: parseInt(data["grade-level"]),
        gender: parseInt(data["gender"]),
    };

    let error = form.querySelector(".error");
    console.log(serialized);

    try {
        let options = {
            method: "POST",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            body: JSON.stringify(serialized, null, 4)
        };

        let response = await fetch("http://localhost:3000/add/", options);
        let json = await response.json();

        if (!json.ok) throw new Error(json.msg);
    } catch (err) {
        console.log(err);
        error.innerHTML = `${err.message}`;
        return;
    }

    showThankYou();
})

function showStudentHealthRecordPage() {
    form.classList.add("invisible");
    dataContentPrivacy.classList.add("invisible");
    studentHealthRecord.classList.remove("invisible");
    thankYou.classList.add("invisible");
}

function showDataContentPrivacyPage() {
    form.classList.add("invisible");
    studentHealthRecord.classList.add("invisible");
    dataContentPrivacy.classList.remove("invisible");
    thankYou.classList.add("invisible");
}

function showFormPage() {
    form.classList.remove("invisible");
    studentHealthRecord.classList.add("invisible");
    dataContentPrivacy.classList.add("invisible");
    thankYou.classList.add("invisible");
}

function showThankYou() {
    form.classList.add("invisible");
    studentHealthRecord.classList.add("invisible");
    dataContentPrivacy.classList.add("invisible");
    thankYou.classList.remove("invisible");
}
