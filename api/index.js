import express from "express";
import dotenv from "dotenv";
import cors from "cors";
import nodemailer from "nodemailer";
import bcrypt from "bcrypt";
import { v4 as uuidv4 } from "uuid";

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

const generateResetToken = () => uuidv4();
const sendEmail = async (to, subject, text) => {
    const transporter = nodemailer.createTransport({
        service: "gmail",
        auth: {
            user: "stanyui166@gmail.com",
            pass: process.env.PASS,
        },
    });

    const mailOptions = {
        from: "stanyui166@gmail.com",
        to,
        subject,
        text,
    };

    await transporter.sendMail(mailOptions);
};

// Create a new user
app.post("/register", async (req, res) => {
    try {
        const { email, password, admin } = req.body;
        const db = client.db("Main");
        const existingUser = await db.collection("users").findOne({ email });

        if (!(/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email))) {
            console.log(email);
            return res.status(401).json({ message: "Invalid email" });
        }

        if (existingUser) {
            return res.status(409).json({ message: "User already exists" });
        }

        const hashedPassword = await bcrypt.hash(password, 10);

        const user = {
            email,
            password: hashedPassword,
            admin: admin == "true",
        };

        await db.collection("users").insertOne(user);

        res.status(201).json({ message: "User created successfully" });

    } catch (error) {
        console.error("Error during registration:", error);
        res.status(500).json({ message: "Internal server error" });
    }
});

// Login
app.post("/login", async (req, res) => {
    try {
        const { email, password } = req.body;
        const db = client.db("Main");
        const user = await db.collection("users").findOne({ email });

        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
            return res.status(403).json({ message: "Invalid email" });
        }

        if (!user) {
            return res.status(404).json({ message: "User not found" });
        }

        const passwordMatch = await bcrypt.compare(password, user.password);

        if (!passwordMatch) {
            return res.status(401).json({ message: "Invalid credentials" });
        }

        res.status(200).json({ message: "Login successful", user });
    } catch (error) {
        console.error("Error during login:", error);
        res.status(500).json({ message: "Internal server error" });
    }
});

// Forgot Password
app.post("/forgot-password", async (req, res) => {
    try {
        const { email } = req.body;
        const db = client.db("Main");
        const user = await db.collection("users").findOne({ email });

        if (!user) {
            return res.status(404).json({ message: "User not found" });
        }

        const resetToken = generateResetToken();

        await db.collection("users").updateOne(
            { email },
            { $set: { resetToken } }
        );

        await sendEmail(email, "Password Reset", `TOKEN: ${resetToken}`);

        res.status(200).json({ message: "Password reset token sent. Please check your email." });
    } catch (error) {
        console.error("Error during forgot password:", error);
        res.status(500).json({ message: "Internal server error" });
    }
});

// Reset Password
app.post("/reset-password", async (req, res) => {
    try {
        const { token, password } = req.body;
        const db = client.db("Main");

        const user = await db.collection("users").findOne({ resetToken: token });

        if (!user) {
            return res.status(404).json({ message: "Invalid or expired token" });
        }

        const hashedPassword = await bcrypt.hash(password, 10);

        await db.collection("users").updateOne(
            { resetToken: token },
            { $set: { password: hashedPassword, resetToken: null } }
        );

        res.status(200).json({ message: "Password reset successful" });

    } catch (error) {
        console.error("Error during password reset:", error);
        res.status(500).json({ message: "Internal server error" });
    }
});

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

app.post("/add_record", async (req, res) => {
    let students = client.db("Main").collection("students");
    let filter = { _id: new ObjectId(req.body.id) };

    let output = await students.findOne(filter);
    let records = output.records ? [...output.records] : [];

    records.push(req.body.data);

    await students.updateOne(filter, { $set: { records }});

    res.send({ ok: true });
});

app.post("/delete_record", async (req, res) => {
    let students = client.db("Main").collection("students");
    let filter = { _id: new ObjectId(req.body.id) };

    let output = await students.findOne(filter);
    let records = output.records ? [...output.records] : [];

    records.splice(req.body.i, 1);

    await students.updateOne(filter, { $set: { records }});

    res.send({ ok: true });
});

client.connect().then(() => {
    console.log("Database is up and running.");
}).catch(console.error);

app.listen(port, () => {
    console.log(`Express app is up and listening on port ${port}`);
});
