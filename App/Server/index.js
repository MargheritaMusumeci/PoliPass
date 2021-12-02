
const { response } = require("express");
const express = require("express");
const cors = require('cors');
const app = express();
const port = 3000;

// end points --> 
app.use(cors());

app.get("/", (req, res) => {
    console.log("called")
    res.send("Hello World");
});

// database connection --> 
const {MongoClient} = require('mongodb');

async function databaseConnection() {
    
    //connection uri
    const uri = "mongodb+srv://Piero_Rendina:R3nd1n%402021@cluster0.hns6k.mongodb.net/authSource=admin?ssl=true&tlsAllowInvalidCertificates=true";

    //instance of mongoDB client
    const client = new MongoClient(uri);

    //await blocks further execution until that operation has completed
    try {
        //connect to the cluster
        await client.connect();
        console.log("Database connected");

    } catch (e) {
        console.error(e);

    //for the moment close the database connection immediatly 
    } finally {
        await client.close();
    }
}

databaseConnection().catch(console.error);

// app.listen() method here takes in two parameters, the first one represents the port number and the other one is a 
    // callback function that returns a message to the console, upon successfully listening to the specified port
app.listen(port,() => console.log('Server listening at port ' + port ));


