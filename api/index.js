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

app.get("/search/:text", async (req, res) => {
    let students = client.db("Main").collection("students");
    let output = await students.aggregate([ { "$search": { "index": "default", "text": { 
        "query": req.params.text, 
        "path": { "wildcard": "*" } 
    } } } ]).toArray();

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

app.get("/get/:id", async (req, res) => {
    let students = client.db("Main").collection("students");
    let _id = req.params.id;

    let output = await students.findOne({ _id: new ObjectId(_id) });

    res.send(output);
})

app.post("/delete", async (req, res) => {
    let students = client.db("Main").collection("students");
    await students.deleteOne({ _id: new ObjectId(req.body.id) });
    res.send({ ok: true });
})

app.post("/delete_all", async (req, res) => {
    let students = client.db("Main").collection("students");
    await students.deleteMany({});
    res.send({ ok: true });
})

app.post("/add", async (req, res) => {
    let output = { ok: true, msg: "Success" };
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
            output.msg = `Already exist!`;
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
