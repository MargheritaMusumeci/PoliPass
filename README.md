# PoliPass

## Index

- Group components
- Environment setup 
- Database Generator
- GUI


## Group Components :family_man_boy_boy::family_man_girl:

| Cognome | Nome | e-mail | Matricola | Codice Persona
| ------ | ------ |----- |----- |----- |
| Musumeci | Margherita| margherita.musumeci@mail.polimi.it| 991549| 10600069
| Nunziante |  Matteo| matteo.nunziante@mail.polimi.it | 992518 | 10670132
| Rendina |Piero | piero.rendina@mail.polimi.it  | 991437 | 10629696
| Sanchini |  Andrea | andrea.sanchini@mail.polimi.it | 992072 | 10675541
| Zuccolotto |Enrico | enrico.zuccolotto@mail.polimi.it  | 993209 | 10666354

## Environment Setup :computer:

Go to App/Server and type the following commands to install the node mobules

```sh
 npm install
```
```sh
 npm install mongodb
```
Go to App/Client and type the following command to install the node mobules 

```sh
 npm install
```
If necessary 
```sh
 npm install --global expo-cli
```
Depending on the OS, it is required to change 'localhost' with the IP address of the machine where the server is running in the following Client's methods:

- Home.js line 22 and line 86
- Login.js line 48
- QRcode.js line 23 and line 74
- SignUp.js line 16

## Database Generator :floppy_disk:
To generate the database you should set the scope of the execution to the PoliPass's directory.
You can choose the following parameters to build the dataset however you like:

- Number of people (at least 100 otherwise the generator won't work)
- Max number of vaccine's doses for each person
- Max number of tests for each person
- Probability of being a doctor/nurse


## GUI :iphone:

### Server 
To run the server, go to App/Server and type the following command

```sh
 node index.js 
```
### Client 
To start the application, go to App/Client and type the following command

```sh
 npm start 
```

### Application Login 
To access the application the email and password are needed.

Here is the list of credentials to sign in.

<div style="text-align: center;">

|      Email         |    Password     |
| ------------------ | --------------- |
| lino.cannavaro@polipass.it | password |
| pacina.musumeci@polipass.it | password |
| ordalia.montezemolo@polipass.it | password |
| nunzio.rendina@polipass.it | password |
| felicia.mazzucchelli@polipass.it | password |

</div>

By default the password is set to password for everyone.

You can also create further accesses by yourself. You just need to look in the
database, find name and surname of a person in a covid certificate and then
sign in with the email built as **name.surname@polipass.it** and **password**.

