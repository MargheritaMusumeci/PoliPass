
const { response } = require("express");
const express = require("express");
const cors = require('cors');
const app = express();
const port = 3000;

let email_saved = 'a';
let password_saved = 'b';
let json = {}

// end points --> 
app.use(cors());
app.use(express.json());

// receives an id and returns a json with green-pass information
app.get("/qr", async (req, res) => { 

    information = await getQR(client);
    res.send(information);
});

// receives an id and returns a json with green-pass information
app.get("/home", async (req, res) => { 

    information = await getInformation(client);
    res.send(information);
});

// receives a json, checks credential, returns ack
app.post("/login", async (req, res) => {

    credential = req.body
    result = await checkCredential(credential);
    if (result) res.send("Ack");
    else res.send("Nack"); 
});

// useful functions --> 

// checks if exist a corrispondece between mail and password provided
async function checkCredential(credential){

    let hash_password = createHash(credential.Password).toString();
    res = await findOneListingByName(client, credential.Mail, hash_password);
    return res;
}

// Encodes a password using SHA-256 algorithm
const createHash = (password) => { 

var crypto = require('crypto');
var hash = crypto.createHash('sha256').update(password).digest('hex');
return hash;
}

// database query -->

async function getQR(client){
    const result = await client.db("polipass").collection("covid_certificates").find({ EMAIL: global.email_saved, PASSWORD: global.password_saved }).toArray();
    if (result[0].GREEN_PASS == undefined) {
        json={}
    }
    else {
        json = { 
            name : result[0].NAME + " " +  result[0].SURNAME,
            birthday : ((result[0].BIRTHDATE).toString().substring(0,15)),
            vaccineName : result[0].VACCINATIONS[0].VACCINE.NAME,
            qr : result[0].GREEN_PASS.QR_CODE,
        }
    }
    return JSON.stringify(json);
}


async function getInformation(client){
    const result = await client.db("polipass").collection("covid_certificates").find({ EMAIL: global.email_saved, PASSWORD: global.password_saved }).toArray();
    const issuer = await client.db("polipass").collection("issuers").find({_id : result[0].VACCINATIONS[0].ISSUER}).toArray();
    
    if (result[0].GREEN_PASS == undefined) {
        json={}
    }
    else{
        json = { 
            name : result[0].NAME + " " +  result[0].SURNAME,
            birthday : ((result[0].BIRTHDATE).toString().substring(0,15)),
            vaccineName : result[0].VACCINATIONS[0].VACCINE.NAME,
            vaccineProducer : result[0].VACCINATIONS[0].VACCINE.PRODUCER,
            issuer : issuer[0].TYPE + " " +  issuer[0].NAME,
            doses : result[0].VACCINATIONS[0].DOSE,
            date : ((result[0].GREEN_PASS.ISSUE_DATE).toString().substring(0,15)),
            expire : ((result[0].GREEN_PASS.EXPIRATION_DATE).toString().substring(0,15)),
        }
    }
    return JSON.stringify(json);
}

async function findOneListingByName(client, email, password) {

    
   	const result = await client.db("polipass").collection("covid_certificates").find({ EMAIL: email, PASSWORD: password }).count();
    
       if (result == 1) {
        global.email_saved = email;
        global.password_saved = password;
        return true;
        }
    return false;
}

// database connection --> 
const {MongoClient} = require('mongodb');

//connection uri
const uri = "mongodb+srv://Piero_Rendina:R3nd1n%402021@cluster0.hns6k.mongodb.net/authSource=admin?ssl=true&tlsAllowInvalidCertificates=true";

//instance of mongoDB client
const client = new MongoClient(uri);

async function databaseConnection() {

    //await blocks further execution until that operation has completed
    try {
        //connect to the cluster
        await client.connect();
        console.log("Database connected");

    } catch (e) {
        console.error(e);
    }
}

databaseConnection().catch(console.error);

// app.listen() method here takes in two parameters, the first one represents the port number and the other one is a 
    // callback function that returns a message to the console, upon successfully listening to the specified port
app.listen(port,() => console.log('Server listening at port ' + port ));


