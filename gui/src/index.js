const { app, BrowserWindow, ipcMain } = require("electron");
const { mdToPdf } = require("md-to-pdf");
const path = require("path");
const fs = require("fs");

function createWindow() {
    let mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        resizable: false,
        webPreferences: {
            preload: path.join(__dirname, "preload.js"),
        },
    });

    mainWindow.menuBarVisible = false;
    mainWindow.loadFile(path.join(__dirname, "index.html"));
};

async function printPDF(_, json) {
    let pdfPath = path.join(__dirname, `student_data.pdf`);

    await mdToPdf({ content: markdown(json) }, { dest: pdfPath });

    let pdfWindow = new BrowserWindow({
        width: 800,
        height: 600,
        resizable: false,
    });

    pdfWindow.loadFile(pdfPath);
    pdfWindow.webContents.print({});
}

app.whenReady().then(() => {
    ipcMain.on("print", printPDF); 

    createWindow();

    app.on("activate", () => {
        if (BrowserWindow.getAllWindows().length === 0) createWindow();
    })
});

function markdown(json) {
    let name = json.name
        ? `${json.name.last}, ${json.name.first} ${json.name.middle} ${json.name.suffix}`
        : "N/A";
    let grade = json.grade_level ? json.grade_level + 7 : "N/A";
    let gender = json.gender ? "Female" : "Male";
    let checked = (x) => x ? "checked" : "";
    let visual_limitations = json.medical_history?.visual_limitations?.glasses || json.medical_history?.visual_limitations?.contact_lenses;

    let records = `<div class="page-break"></div>\n\n# RECORDS\n\n`;

    for (let i = 0; i < (json.records?.length || 0); i++) {
        let record = json.records[i];

        records += `<fieldset>
    <legend>RECORD #${i}</legend>
    <div><label>IN:</label><input type="time" value="${record.in}"></div>
    <div><label>OUT:</label><input type="time" value="${record.out}"></div>
    <div><label>DATE:</label><input type="date" value="${record.date}"></div>
    <div class="block"><label>REASON/CAUSE:</label><textarea>${record.reason}</textarea></div>
    <div class="block"><label>TREATMENT:</label><textarea>${record.treatment}</textarea></div>
</fieldset>`;
        records += "<br>\n";
    }
    
    return `---
stylesheet: https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/2.10.0/github-markdown.min.css
body_class: markdown-body
css: |-
    .page-break { page-break-after: always; }
    .markdown-body { font-size: 10pt; }
    .markdown-body pre > code { white-space: pre-wrap; }
    fieldset { display: flex; flex-direction: column; gap: 0.5em; }
    fieldset.wrap { max-height: 20em; flex-wrap: wrap; }
    fieldset > div:not(.block) { display: flex; gap: 0.5em; }
    fieldset > div.block { display: flex; flex-direction: column; }
    textarea { resize: none; }
    legend { font-weight: bold; }
    label { white-space: nowrap; font-weight: bold; }
    input[type="text"] { width: 100% }
pdf_options:
    margin: 0.5in 0.5in
    format: A4
---

# STUDENT HEALTH RECORD

<fieldset>
    <legend>STUDENT DEMOGRAPHIC DATA</legend>
    <div><label>NAME:</label><input type="text" value="${name}"></div>
    <div><label>GRADE:</label><input type="text" value="${grade}"></div>
    <div><label>SECTION:</label><input type="text" value="${json.section || "N/A"}"></div>
    <div><label>ADDRESS:</label><input type="text" value="${json.address || "N/A"}"></div>
    <div><label>GENDER:</label><input type="text" value="${gender}"></div>
    <div><label>RELIGION:</label><input type="text" value="${json.religion || "N/A"}"></div>
    <div><label>NATIONALITY:</label><input type="text" value="${json.nationality || "N/A"}"></div>
    <div><label>DATE OF BIRTH:</label><input type="text" value="${json.birth?.date || "N/A"}"></div>
    <div><label>PLACE OF BIRTH:</label><input type="text" value="${json.birth?.place || "N/A"}"></div>
</fieldset><br>
<fieldset>
    <legend>NAME OF PARENTS</legend>
    <div><label>Father Name:</label><input type="text" value="${json.father?.name || "N/A"}"></div>
    <div><label>Father Contact:</label><input type="text" value="${json.father?.contact || "N/A"}"></div>
    <div><label>Mother Name:</label><input type="text" value="${json.mother?.name || "N/A"}"></div>
    <div><label>Mother Contact:</label><input type="text" value="${json.mother?.contact || "N/A"}"></div>
</fieldset><br>

## IMMUNIZATION

<fieldset>
    <legend>VACCINE</legend>
    <div><input type="checkbox" ${checked(json.immunization?.flu)}><label>Flu</label></div>
    <div><input type="checkbox" ${checked(json.immunization?.hepatitis)}><label>Hepatitis A</label></div>
    <div><input type="checkbox" ${checked(json.immunization?.varicella)}><label>Varicella</label></div>
    <div><input type="checkbox" ${checked(json.immunization?.meningococcal)}><label>Meningococcal</label></div>
    <div><input type="checkbox" ${checked(json.immunization?.pneunomococcal)}><label>Pneunomococcal</label></div>
    <div><input type="checkbox" ${checked(json.immunization?.hpv)}><label>HPV (anti-cervical ca)</label></div>
    <div class="block"><label>REMARKS</label><textarea>${json.immunization?.remarks}</textarea></div>
</fieldset>
<div class="page-break"></div>
<fieldset>
    <legend>COVID VACCINE</legend>
    <div><label>1st DOSE:</label><input type="text" value="${json.vaccination?.first || "N/A"}"></div>
    <div><label>2nd DOSE:</label><input type="text" value="${json.vaccination?.second || "N/A"}"></div>
    <div><label>BOOSTER:</label><input type="text" value="${json.vaccination?.booster || "N/A"}"></div>
    <div class="block"><label>REMARKS</label><textarea>${json.vaccination?.remarks || "N/A"}</textarea></div>
    <div class="block"><label>Reason if not vaccinated</label><textarea>${json.vaccination?.reason || "N/A"}</textarea></div>
    <div>
        <label>Is household vaccinated</label>
        <input type="radio" value=1 ${checked(json.vaccination?.household)}> <label>Yes</label> 
        <input type="radio" value=0 ${checked(!json.vaccination?.household)}> <label>No</label>
    </div>
    <div class="block">
        <label>Reason if the household not vaccinated</label>
        <textarea>${json.vaccination?.household_reason}</textarea>
    </div>
</fieldset><br>

## MEDICAL HISTORY

<fieldset>
    <legend>ALLERGIES</legend>
    <div class="block"><textarea>${json.medical_history?.allergies}</textarea></div>
</fieldset><br>
<fieldset>
    <legend>MEDICATION</legend>
    <div>
        <label>Is child taking medications</label>
        <input type="radio" value=1 ${checked(json.medical_history?.medication?.has_meds)}> <label>Yes</label> 
        <input type="radio" value=0 ${checked(!json.medical_history?.medication?.has_meds)}> <label>No</label>
    </div>
    <div><label>Medication:</label><input type="text" value="${json.medical_history?.medication?.name}"></div>
    <div><label>Used to treat:</label><input type="text" value="${json.medical_history?.medication?.treat}"></div>
    <div><label>Dose/Time:</label><input type="text" value="${json.medical_history?.medication?.dose}"></div>
</fieldset><br>
<fieldset>
    <legend>Medicine can be given to the child</legend>
    <div><label>Headache:</label><input type="text" value="${json.medical_history?.conditions?.headache}"></div>
    <div><label>Toothache:</label><input type="text" value="${json.medical_history?.conditions?.toothache}"></div>
    <div><label>Fever:</label><input type="text" value="${json.medical_history?.conditions?.fever}"></div>
    <div><label>Allergy/rhinitis:</label><input type="text" value="${json.medical_history?.conditions?.rhinitis}"></div>
    <div><label>Stomach ache:</label><input type="text" value="${json.medical_history?.conditions?.stomach_ache}"></div>
    <div class="block"><label>Others: please specify</label><textarea>${json.medical_history?.conditions?.others || "N/A"}</textarea></div>
</fieldset>
<div class="page-break"></div>
<fieldset>
    <legend>Ongoing treatments</legend>
    <div class="block"><textarea>${json.medical_history?.ongoing_treatment || "N/A"}</textarea></div>
</fieldset><br>
<fieldset>
    <legend>Reason why the child cannot participate in Physical Education classes</legend>
    <div class="block"><textarea>${json.medical_history?.sport_limitations || "N/A"}</textarea></div>
</fieldset><br>
<fieldset>
    <legend>Visual Difficulties</legend>
    <div>
        <input type="radio" value=1 ${checked(visual_limitations)}> <label>Yes</label> 
        <input type="radio" value=0 ${checked(!visual_limitations)}> <label>No</label>
    </div>
    <div><input type="checkbox" ${checked(json.medical_history?.visual_limitations?.glasses)}><label>Glasses</label></div>
    <div><input type="checkbox" ${checked(json.medical_history?.visual_limitations?.contact_lenses)}><label>Contact Lenses</label></div>
</fieldset><br>
<fieldset>
    <legend>Difficulties with Hearing, Speech or Language Development</legend>
    <div class="block"><textarea>${json.medical_history?.language_limitations || "N/A"}</textarea></div>
</fieldset><br>
<fieldset class="wrap">
    <legend>Indicate if the child has had the following conditions:</legend>
    <div><input type="checkbox" ${checked(json.medical_history?.other_limitations?.backaches)}><label>Backaches</label></div>
    <div><input type="checkbox" ${checked(json.medical_history?.other_limitations?.chest_pain)}><label>Chest Pain</label></div>
    <div><input type="checkbox" ${checked(json.medical_history?.other_limitations?.cough)}><label>Cough</label></div>
    <div><input type="checkbox" ${checked(json.medical_history?.other_limitations?.cyclic_vomiting)}><label>Cyclic Vomiting</label></div>
    <div><input type="checkbox" ${checked(json.medical_history?.other_limitations?.depression)}><label>Depression</label></div>
    <div><input type="checkbox" ${checked(json.medical_history?.other_limitations?.difficulty_of_breathing)}><label>Difficulty of Breathing</label></div>
    <div><input type="checkbox" ${checked(json.medical_history?.other_limitations?.dizziness)}><label>Dizziness</label></div>
    <div><input type="checkbox" ${checked(json.medical_history?.other_limitations?.epistaxis)}><label>Epistaxis</label></div>
    <div><input type="checkbox" ${checked(json.medical_history?.other_limitations?.eczema)}><label>Eczema</label></div>
    <div><input type="checkbox" ${checked(json.medical_history?.other_limitations?.fainting_spells)}><label>Fainting Spells</label></div>
    <div><input type="checkbox" ${checked(json.medical_history?.other_limitations?.headaches)}><label>Headaches</label></div>
    <div><input type="checkbox" ${checked(json.medical_history?.other_limitations?.insomias)}><label>Insomias</label></div>
    <div><input type="checkbox" ${checked(json.medical_history?.other_limitations?.joint_pains)}><label>Joint Pains</label></div>
    <div><input type="checkbox" ${checked(json.medical_history?.other_limitations?.recurrent_abdominal_pain)}><label>Recurrent Abdominal Pain</label></div>
    <div><input type="checkbox" ${checked(json.medical_history?.other_limitations?.seizure)}><label>Seizure</label></div>
    <div><input type="checkbox" ${checked(json.medical_history?.other_limitations?.urinary_problems)}><label>Urinary Problems</label></div>
    <div><input type="checkbox" ${checked(json.medical_history?.other_limitations?.weight)}><label>Weight loss</label></div>
    <div><input type="checkbox" ${checked(json.medical_history?.other_limitations?.others)}><label>Others</label></div>
</fieldset><br>
<fieldset>
    <legend>Any prescription drugs that the child is taking at the moment.</legend>
    <div class="block"><textarea>${json.medical_history?.drugs_taken || "N/A"}</textarea></div>
</fieldset><br>
<fieldset>
    <legend>0ther medical information that may help understand the child's health needs:</legend>
    <div class="block"><textarea>${json.medical_history?.other_info || "N/A"}</textarea></div>
</fieldset><br>
${json.records ? records : ""}
`
}
