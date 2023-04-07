let url = new URL(window.location);
let page_ptr = url.searchParams.get("thank_you") ? 4 : 0;
let page_vec = [
    ".sccr-intro",
    ".sccr-dcp",
    ".sccr-shr",
    ".sccr-form-section",
    ".sccr-thank-you-section",
];

async function on_submit() {
    let elements = document.querySelectorAll(".sccr-form input")
    let error = document.querySelector(".sccr-error");
    let values = {};

    for (let i = 0; i < elements.length; i++) {
        let element = elements[i];

        if (element.type == "checkbox") {
            values[element.name] = element.checked;
        } else {
            values[element.name] = element.value;
        }
    }

    try {
        let grade_levels = ["is_7", "is_8", "is_9", "is_10", "is_11", "is_12"];
        let grade_level = 0;
        let grade_count = 0;

        for (let i = 0; i < grade_levels.length; i++) {
            if (!values[grade_levels[i]]) continue;
            grade_count += 1;
            grade_level = i;
        }

        let genders = ["is_male", "is_female"];
        let gender = 0;
        let gender_count = 0;

        for (let i = 0; i < genders.length; i++) {
            if (!values[genders[i]]) continue;
            gender_count += 1;
            gender = i;
        }

        if (grade_count > 1) {
            throw new Error("choose only 1 grade level");
        } else if (grade_count == 0) {
            throw new Error("choose a grade level");
        } else if (gender_count == 0) {
            throw new Error("choose a gender");
        } else if (gender_count > 1) {
            throw new Error("choose only 1 gender");
        }

        let serialized = {
            name: {
                last: values.surname,
                first: values.first_name,
                middle: values.middle_initial,
                suffix: values.suffix,
            },
            birth: {
                date: new Date(values.birth_date),
                place: values.birth_place
            },
            father: {
                name: values.father_name,
                contact: values.father_contact,
            },
            mother: {
                name: values.mother_name,
                contact: values.mother_contact,
            },
            section: values.section,
            address: values.address,
            religion: values.religion,
            nationality: values.nationality,
            contact: values.contact,
            grade_level,
            gender,
        };

        const options = {
            method: "POST",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            body: JSON.stringify(serialized, null, 4)
        };

        const response = await fetch("http://localhost:3000/set/", options);
        const json = await response.json();

        if (!json.ok) {
            throw new Error(json.msg);
        } 
    } catch (err) {
        console.log(err);
        error.innerHTML = `${err.message}`;
        return;
    }

    // Call DATABASE API here
    error.innerHTML = ``;
    
    window.location.href = "?thank_you=true";
}

function select_page(new_page_ptr) {
    hide_element(page_vec[page_ptr]);
    page_ptr = new_page_ptr;
    page_ptr %= page_vec.length;
    show_element(page_vec[page_ptr]);
}

function next_page() {
    hide_element(page_vec[page_ptr]);

    page_ptr += 1;
    page_ptr %= page_vec.length;

    show_element(page_vec[page_ptr]);
}

function show_element(selector) {
    let element = document.querySelector(selector);
    element.style.display = "block";
}

function hide_element(selector) {
    let element = document.querySelector(selector);
    element.style.display = "none";
}

function init() {
    for (let i = 0; i < page_vec.length; i++) {
        if (i == page_ptr) continue;
        hide_element(page_vec[i]);
    }
}

function main() {
    init();
}

main();
