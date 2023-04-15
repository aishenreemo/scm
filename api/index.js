import express from "express";
import dotenv from "dotenv";
import cors from "cors";

import { MongoClient, ObjectId, ServerApiVersion } from "mongodb";

dotenv.config();

const app = express();
const port = 3000;

const client = new MongoClient(process.env.MONGO_DB_URL, { 
    useNewUrlParser: true,
    useUnifiedTopology: true,
    serverApi: ServerApiVersion.v1
});

app.use(express.json());
app.use(cors());

app.get("/get", async (_, res) => {
    let students = client.db("Main").collection("students");

    res.send(await students.find({}).toArray())
})

app.get("/search/:text", async (req, res) => {
    let students = client.db("Main").collection("students");
    let output = await students.aggregate([ { "$search": { "index": "default", "text": { "query": req.params.text, "path": { "wildcard": "*" } } } } ]).toArray();

    res.send(output);
})

app.get("/sections/:grade_level", async (req, res) => {
    let students = client.db("Main").collection("students");
    let grade_level = parseInt(req.params.grade_level) - 7;

    let output = await students.distinct("section", { grade_level })

    res.send(output);
})

app.get("/students/:grade_level/:section", async (req, res) => {
    let students = client.db("Main").collection("students");
    let section = req.params.section;
    let grade_level = parseInt(req.params.grade_level) - 7;

    let output = await students.find({ section, grade_level }).toArray();

    res.send(output);
})

app.get("/student/:id", async (req, res) => {
    let students = client.db("Main").collection("students");
    let _id = req.params.id;

    let output = await students.findOne({ _id: new ObjectId(_id) });

    res.send(output);
})

app.post("/set", async (req, res) => {
    let output = { ok: true, msg: "Success" };

    // check for name
    for (let [key, val] of Object.entries(req.body)) {
        if (key == "grade_level") continue;
        if (key == "gender") continue;
        if (!!val) continue;

        output.ok = false;
        output.msg = `${key} is required.`;
        return res.send(output);
    }

    for (let [key, val] of Object.entries(req.body.birth)) {
        if (!!val) continue;

        output.ok = false;
        output.msg = `birth.${key} is required.`;
        return res.send(output);
    }

    for (let [key, val] of Object.entries(req.body.name)) {
        if (key == "suffix") continue;
        if (val != "") continue;

        output.ok = false;
        output.msg = `name.${key} is required.`;
        return res.send(output);
    }

    for (let [key, val] of Object.entries(req.body.father)) {
        if (val != "") continue;

        output.ok = false;
        output.msg = `father.${key} is required.`;
        return res.send(output);
    }

    for (let [key, val] of Object.entries(req.body.mother)) {
        if (val != "") continue;

        output.ok = false;
        output.msg = `mother.${key} is required.`;
        return res.send(output);
    }

    let students = client.db("Main").collection("students");
    let find_opts = {
        "name.last": req.body.name.last,
        "name.first": req.body.name.first,
    };

    try {
        let student = await students.findOne(find_opts);

        if (student == null) {
            await students.insertOne(req.body);
            console.log(`New registrar -> ${req.body.name.first} ${req.body.name.last}`);
        } else {
            output.ok = false;
            output.msg = `Name already exist!`;
        }
    } catch (err) {
        output.ok = false;
        output.msg = `${err}`;
    }

    res.send(output);
});

client.connect().then(() => {
    console.log("Database is up and running.");
}).catch(console.error);

app.listen(port, () => {
    console.log(`Express app is up and listening on port ${port}`);
});
