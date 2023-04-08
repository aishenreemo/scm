import { MongoClient, ServerApiVersion } from "mongodb";
import dotenv from "dotenv";

dotenv.config();

const client = new MongoClient(process.env.MONGO_DB_URL, { 
    useNewUrlParser: true,
    useUnifiedTopology: true,
    serverApi: ServerApiVersion.v1 
});

// https://regex101.com/r/OBYGSX/1
const regex = /^((?:\w{2,}\s?)+)\s([A-Z]\.)\s(\w+)$\n^((?:Fe)?[Mm]ale)$\n^(\d+).*$\n^(\w+)$/mg;

// Alternative syntax using RegExp constructor
// const regex = new RegExp('^((?:\\w{2,}\\s?)+)\\s([A-Z]\\.)\\s(\\w+)$\\n^((?:Fe)?[Mm]ale)$\\n^(\\d+).*$\\n^\\w+$', 'mg')

// noooo i didn't doxxed any names

const str = `Brent Gabriel S. Almano
Male
12 STEM
Hermon

Stephanie Marie B. Apolinario
Female
12 STEM
Hermon

Keane Paul N. Abaring
Male
12 ICT
Olivet

Arabela Raine T. Alfonso
Female
12 ICT 
Olivet

Clarence R. Abellada
Male
12 STEM
Gilead

Kimberly A. Bandong
Female
12 STEM
Gilead

Austin Jhon E. Abquina
Male
12 HUMSS
Gerizim

Zhengir I. Arnecillo
Male
12 HUMSS
Ararat

Marianne R. Alcoba
Female
12 HUMSS
Ararat

Arron Justine G. Colocado
Male
12 STEM 
Zion

Daniel S. Adorador
Male
12 HUMSS 
Ephraim

Oiram Alem P. Aquino
Male
12 ABM
Horeb

Clarence Angelo F. Bautista
Male
12 STEM
Sinai

Cherie Mae D. Alcones
Female
12 STEM
Sinai

Aiah Lorraine V. Alcantara
Female
12 ABM
Carmel

Gene Royce B. Apiladas
Male
12 STEM
Nebo

Jhen Daryl F. Acosta
Female
12 STEM 
Nebo

Emil Jon S. Cadiliman
Male
12 ABM
Moriah

Joahnna Y. Alcantara
Female
12 ABM 
Moriah

Sophia G. Antalan
Female
11 STEM
Cypress

Axl Robb D. Balsicas
Male
11 STEM 
Crocus

Miguel L. Campos
Male
11 STEM 
Carob

Dexter Lee S. Allas
Male
11 STEM
Cedar

Krisshajean B. Albarico
Female
11 STEM
Cedar

James C. Alcaraz
Male
11 STEM
Citron

Madelaine R. Bautista
Female
11 STEM
Citron

Seandi Charm P. Aragon
Male
11 STEM
Caper

Alyanna D. Barzaga
Female
11 STEM
Caper

Niel Andrei M. Abuan
Male
11 STEM 
Cassia

Reinne Sheilley B. Bandiola
Female
11 STEM
Cassia

Franz Gabriel F. Badinas
Male
11 ICT
Tamarix

Bonn Marco C. Basalo
Male
11 HUMSS
Terebinth

Hasna B. Salva
Female
11 HUMSS
Terebinth

Karol Jozef O. Agapito
Male
11 HUMSS 
Poplar

Edriane O. Bona
Male
11 ABM 
Myrtle

Angelanne J. Espino
Female
11 ABM 
Myrtle

Aldrin G. Bautista
Male
11 HUMSS 
Almond

Jhanelle S. Atillio
Female
11 HUMSS
Almond

Samantha Jhade D. Aban
Female
11 ABM
Willow

Christotle B. Caluag
Male
10 
Timothy

Julianna S. Atillo
Female
10 
Timothy

Carl Ivan V. Barrera
Male
10
Silvanus

Nathalie Sei L. Aledia
Female
10 
Silvanus

Mark Russel M. Alcantara
Male
10
Philemon

Jaynielyn S. Andalis
Female
10 
Philemon

Zeus A. Borja
Male
10
Onesimus

Yuna Reese B. Arpon
Female
10 
Onesimus

Jomar Q. Alcosaba
Male
10
Eraphras

Nicole O. Andrade
Female
10
Eraphras

Jeyee L. Barcena
Male
10 
Apollos

Reese Angel C. Betito
Female
10 
Apollos

Gerome T. Compra
Male
9
Jerusalem

Joanah Ivie D. Caradin
Female
9 
Jerusalem

Monica M. Bengaura
Female
9
Semaria

Christian C. Albaytar
Male
9 
Bethany

Cielo Mier B. Almarez
Female
9 
Bethany

Kevin A. Casimpoy
Male
9
Gethsemane

Eugene N. Aguilar
Male
9 
Galilee

Zean Nidmar B. Alabana
Male
9
Capernaum

Amanda Kazey G. Ayos
Female
9 
Capernaum

Mark Gio S. Arevalo
Male
8
Emerald

Rhyan Andrie I. Bataga
Male
8 
Chrysolite

Yanisha G. Corbe
Female
8
Chrysolite

Yohan F. Lockey
Male
8
Jasper

Eimiel B. Caguete
Female
8 
Jasper

Ella Maine C. Amande
Female
8
Onyx

Darius Oliver C. Capuz
Male
8
Amethyst

Charlene D. Suarez
Female
8 
Amethyst

Ralph Yvo H. Abola
Male
8 
Beryl

Nazer M. Murillo
Male
7
Jotham

Mikhaela O. Aplaca
Female
7
Jotham

Beatriz O. Baldelomar
Female
7
Nehemiah

Althea Joy N. Aclan
Female
7
Josiah

Ivan Terence A. Batoon
Male
7
Jehoshaphat

Lycah Mae T. Nomil
Female
7 
Jehoshaphat

Lijie K. Benitez
Male
7 
Hezekiah
`;

client.connect().then(async () => {
    console.log("Database is running!");
    const students = client.db("Main").collection("students");

    await students.deleteMany({});

    let m;

    while ((m = regex.exec(str)) !== null) {
        // This is necessary to avoid infinite loops with zero-width matches
        if (m.index === regex.lastIndex) {
            regex.lastIndex++;
        }
        
        let serialized = {
            name: {
                first: m[1],
                middle: m[2],
                last: m[3],
                suffix: "",
            },
            gender: m[4] == "Male" ? 0 : 1,
            grade_level: parseInt(m[5]) - 7,
            section: m[6],
        };

        let find_opts = {
            "name.last": serialized.name.last,
            "name.first": serialized.name.first,
        };

        try {
            console.log(serialized);
            let student = await students.findOne(find_opts);

            if (student == null) {
                await students.insertOne(serialized);
                console.log(`new registrar -> ${serialized.name.first} ${serialized.name.last}`);
            }

        } catch (err) {
            console.log(err);
        }
    }

    client.close();
}).catch(console.error);
