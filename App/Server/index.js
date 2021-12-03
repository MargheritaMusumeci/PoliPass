
const { response } = require("express");
const express = require("express");
const cors = require('cors');
const app = express();
const port = 3000;

// end points --> 
app.use(cors());
app.use(express.json());

// receives an id and returns a json with green-pass information
app.get("/home", (req, res) => {

    console.log(req.body)
    res.send("Hello World Home");
});

// receives a json, checks credential, returns ack
app.post("/login", async (req, res) => {

    credential = req.body
    result = await checkCredential(credential);
    if (result) res.send("Ack");
    else res.send("Nack"); 

});

// receives a json, checks credential, returns ack
app.post("/signup", (req, res) => {

    console.log(req.body)
    res.send("Hello World Signup");
});

// useful functions 

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

async function findOneListingByName(client, email, password) {
    
   	const result = await client.db("polipass").collection("covid_certificates").find({ EMAIL: email, PASSWORD: password }).count();
    return result == 1;
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


