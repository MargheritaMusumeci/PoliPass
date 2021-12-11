# PoliPass

## Index

- Group components
- Environment setup 
- Database Generator
- GUI


## Group Components :family_man_man_girl_boy:

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
