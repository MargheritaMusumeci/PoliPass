// https://www.mongodb.com/blog/post/quick-start-nodejs-mongodb-how-to-get-connected-to-your-database

const {MongoClient} = require('mongodb');

async function listDatabases(client){
    databasesList = await client.db().admin().listDatabases();
 
    console.log("Databases:");
    databasesList.databases.forEach(db => console.log(` - ${db.name}`));
};
async function main() {
    
    //connection uri
    const uri = "mongodb+srv://Piero_Rendina:R3nd1n%402021@cluster0.hns6k.mongodb.net/authSource=admin?ssl=true&tlsAllowInvalidCertificates=true";

    //instance of mongoDB client
    const client = new MongoClient(uri);

    //await blocks further execution until that operation has completed
    try {
        //connect to the cluster
        await client.connect();

        await  listDatabases(client);

    } catch (e) {
        console.error(e);
    } finally {
        await client.close();
    }
}

main().catch(console.error);
