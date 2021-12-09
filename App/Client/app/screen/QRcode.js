import React, { Component, useState} from "react";
import {
  StyleSheet,
  View,
  StatusBar,
  Image,
  Text,
  TouchableOpacity
} from "react-native";
import MaterialCommunityIconsIcon from "react-native-vector-icons/MaterialCommunityIcons";
import FontAwesomeIcon from "react-native-vector-icons/FontAwesome";
import IoniconsIcon from "react-native-vector-icons/Ionicons";
import EntypoIcon from "react-native-vector-icons/Entypo";
import FeatherIcon from "react-native-vector-icons/Feather";
import { get } from "react-native/Libraries/Utilities/PixelRatio";

function QRcode({ navigation }) {

  const logout = async (navigation) => {

    // send input variables for continuing checks 
    try{
      let res = await fetch('http://localhost:3000/logout');
  
      let server_message = '';
      server_message = await res.text(); 

      if (server_message == "Ack"){
        navigation.navigate("Main");
        
      }
      else{
        setErrorMessage("Invalid mail or password...");
        if (error == true ) setError(!error);
        return;
      }
  
    }catch{
      setErrorMessage("Server not reachable...");
      if (error == true ) setError(!error);
    }
}

  const reload = async (navigation) => {
    navigation.navigate("QRcode");
  }

  // false means no green pass present 
  const [error, setError] = useState(true)

  // true if green pass is a vaccine pass
  // false means test pass
  const [vaccin, setVaccin] = useState(true)

  const [errorMessage, setErrorMessage] = useState('There is no green pass associated with your account...');

  // name and surname 
  const [name, setName] = useState('');

  const [test, setTest] = useState('');

  // birthday
  const [birthday, setBirthday] = useState('');

  // vaccinate name
  const [vaccineName, setVaccineName] = useState('');

  const[image, setImage] = useState('require("../assets/qr-code.png")');

  const getInformation = async () => {

    // send input variables for continuing checks 
    try{
     let res = await fetch('http://localhost:3000/qr', {
       method: 'GET',
       headers: {
         'Accept': 'application/json',
         'Content-Type': 'application/json'
       }
     });
 
     let information = await res.json(); 

     if( Object.keys(information).length === 0){
      if (error == true ) setError(!error);
      return;
     }

     // test pass
     if(information.type != undefined){
      setName(information.name);
      setBirthday(information.birthday);
      setTest(information.type); 
      setImage('data:image/png;base64,' + information.qr);
      if (vaccin == true ) setVaccin(false);
      return;
    }

     setName(information.name);
     setBirthday(information.birthday);
     setVaccineName(information.vaccineName);
     setImage('data:image/png;base64,' + information.qr);
     
   }catch{
     setErrorMessage("Server not reachable...");
     if (error == true ) setError(!error);
   }
 }

 getInformation();

  return (
    <View style={styles.rect}>
      <StatusBar hidden />
      <View style={styles.rect2Column}>
        <View style={styles.rect2}>
          <View style={styles.image1Row}>
            <Image
              source={require("../assets/logo.png")}
              resizeMode="contain"
              style={styles.logo}
            ></Image>
            <View style={styles.rect8}></View>
          </View>
          
        </View>

        { (!error) ? <Text style={styles.error}> {errorMessage} </Text>
          : ( 
        <View>
        <View style={styles.a21Row}>

        </View>
        <Image
          source={{uri: image}}
          resizeMode="contain"
          style={styles.qrcode}
        ></Image>
        <Text style={styles.greenPassCovid20}>Green Pass COVID-19</Text>
        <View style={styles.rect17}>
                <View style={styles.icon10Row}>
                  <FontAwesomeIcon
                    name="user-o"
                    style={styles.icon10}
                  ></FontAwesomeIcon>
                  <Text style={styles.surnameName}>Name Surname</Text>
                </View>
              </View>
              <Text style={styles.rossiMario}>{name}</Text>
              <View style={styles.rect18Stack}>
                <View style={styles.rect18}>
                  <View style={styles.icon17Row}>
                    <FontAwesomeIcon
                      name="birthday-cake"
                      style={styles.icon17}
                    ></FontAwesomeIcon>
                    <Text style={styles.dateOfBirth}>Date of birth</Text>
                  </View>
                </View>
                </View>
                <Text style={styles.dateOfBirth1}>{birthday}</Text>
              
              {vaccin ? <View>
              <View style={styles.rect19}>
                <View style={styles.icon11Row}>
                  <IoniconsIcon
                    name="md-finger-print"
                    style={styles.icon11}
                  ></IoniconsIcon>
                  <Text style={styles.text2}>
                    Vaccine name
                  </Text>
                </View>
              </View>
              <Text style={styles.a98Shi19Y33}>{vaccineName}</Text>
              </View>
              : 
              <View>
              <View style={styles.rect19}>
                <View style={styles.icon11Row}>
                  <IoniconsIcon
                    name="md-finger-print"
                    style={styles.icon11}
                  ></IoniconsIcon>
                  <Text style={styles.text2}>Test name
                  </Text>
                </View>
              </View>
              <Text style={styles.a98Shi19Y33}>{test}</Text>
              </View>
}
              </View>
          )}

      </View>
      <View style={styles.rect2ColumnFiller}></View>
      <View style={styles.rect6}>
        <View style={styles.rect7}>
          <TouchableOpacity
            onPress={() => reload(navigation)}
            style={styles.buttonqr}
          >
          <MaterialCommunityIconsIcon
            name="reload"
            style={styles.icon7}
          ></MaterialCommunityIconsIcon>
          </TouchableOpacity>
          <TouchableOpacity
            onPress={() => navigation.navigate("Home")}
            style={styles.home}
          >
          <EntypoIcon name="home" style={styles.icon8}></EntypoIcon>
          </TouchableOpacity>
          <TouchableOpacity
            onPress={() => logout(navigation)}
            style={styles.main}
          >
          <FeatherIcon name="log-out" style={styles.icon9}></FeatherIcon>
          </TouchableOpacity>
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  rect17: {
    width: 343,
    height: 25,
    flexDirection: "row",
    marginTop: 380,
    marginLeft:50
    
  },
  icon10: {
    color: "#8899a6",
    fontSize: 25
  },
  surnameName: {
    color: "#1da6fa",
    fontSize: 18,
    lineHeight: 20,
    marginLeft: 22,
    marginTop: 3
  },
  icon10Row: {
    height: 25,
    flexDirection: "row",
    flex: 1,
    marginRight: 173,
  
  },
  rossiMario: {
    color: "rgba(255,255,255,1)",
    fontSize: 18,
    lineHeight: 20,
    marginTop: 10,
    marginLeft: 95


  },
  rect18: {
    width: 343,
    height: 25,
    position: "absolute",
    top: 0,
    left: 0,
    flexDirection: "row",
    marginLeft:50
  },
  icon17: {
    color: "#8899a6",
    fontSize: 25
  },
  dateOfBirth: {
    color: "#1da6fa",
    fontSize: 18,
  
    marginLeft: 18,
    marginTop: 3
  },
  icon17Row: {
    height: 25,
    flexDirection: "row",
    flex: 1,
    marginRight: 197
  },

  dateOfBirth1: {
    color: "rgba(255,255,255,1)",
    fontSize: 18,
    lineHeight: 20,
    marginLeft: 95
    
  },
  rect18Stack: {
    width: 343,
    height: 44,
    marginTop: 15
  },
  rect19: {
    width: 343,
    height: 25,
    flexDirection: "row",
    marginTop: 16,
    marginLeft:50
  },
  icon11: {
    color: "#8899a6",
    fontSize: 25
  },
  text2: {
    color: "#1da6fa",
    fontSize: 18,
    lineHeight: 20,
    marginLeft: 20,
    marginTop: 3
  },
  icon11Row: {
    height: 27,
    flexDirection: "row",
    flex: 1,
    marginRight: 75
  },
  a98Shi19Y33: {
    color: "rgba(255,255,255,1)",
    fontSize: 18,
    lineHeight: 20,
    marginTop: 10,
    marginLeft: 95
  },
  rect: {
    flex: 1,
    backgroundColor: "#141f2b"
  },
  rect2: {
    height: 84,
    backgroundColor: "#1c2a38",
    flexDirection: "row"
  },
  logo: {
    height: 50,
    width: 50,
    marginTop: 12
  },
  rect8: {
    width: 50,
    height: 40,
    marginLeft: 92
  },
  image1Row: {
    height: 62,
    flexDirection: "row",
    flex: 1,
    marginRight: 20,
    marginLeft: 163,
    marginTop: 22
  },
  a21: {
    color: "#fefefe",
    fontSize: 18,
    lineHeight: 20
  },
  a21Filler: {
    flex: 1,
    flexDirection: "row"
  },
  download: {
    width: 80,
    height: 80,
    backgroundColor: "#1da6fa",
    borderRadius: 100,
    alignSelf: "flex-end",
    justifyContent: "center"
  },
  rect5: {
    width: 50,
    height: 40,
    alignSelf: "center"
  },
  icon5: {
    color: "rgba(255,255,255,1)",
    fontSize: 40,
    alignSelf: "center"
  },
  a21Row: {
    height: 91,
    flexDirection: "row",
    marginTop: 541,
    marginLeft: 76,
    marginRight: 20
  },
  qrcode: {
    height: 310,
    width: 310,
    backgroundColor: "rgba(230, 230, 230,1)",
    borderWidth: 1,
    borderColor: "#000000",
    borderRadius: 10,
    marginTop: -565,
    marginLeft: 33
  },
  greenPassCovid20: {
    color: "rgba(255,255,255,1)",
    fontSize: 24,
    marginTop: -359,
    fontWeight: "bold",
    marginLeft: 65
  },

  rect10: {
    width: 343,
    height: 25,
    position: "absolute",
    top: 0,
    left: 0,
    flexDirection: "row"
  },
  icon11: {
    color: "#8899a6",
    fontSize: 25
  },
  dateOfBirth2: {
    color: "#fefefe",
    fontSize: 18,
    lineHeight: 20,
    marginLeft: 18,
    marginTop: 3
  },
  icon11Row: {
    height: 25,
    flexDirection: "row",
    flex: 1,
    marginRight: 197
  },
  dateOfBirth1Stack: {
    width: 343,
    height: 44,
    marginTop: 410,
    marginLeft: 32
  },
  name: {
    color: "rgba(255,255,255,1)",
    fontSize: 18,
    lineHeight: 20,
    marginTop: -80,
    marginLeft: 76
  },
  rect9: {
    width: 343,
    height: 25,
    flexDirection: "row",
    marginTop: 76,
    marginLeft: 32
  },
  icon10: {
    color: "#8899a6",
    fontSize: 25
  },
  text1: {
    color: "#fefefe",
    fontSize: 18,
    lineHeight: 20,
    marginLeft: 20,
    marginTop: 3
  },
  icon10Row: {
    height: 27,
    flexDirection: "row",
    flex: 1,
    marginRight: 75
  },
  rect11: {
    width: 343,
    height: 25,
    flexDirection: "row",
    marginTop: -146,
    marginLeft: 32
  },
  icon12: {
    color: "#8899a6",
    fontSize: 25
  },
  surnameName1: {
    color: "rgba(255,255,255,1)",
    fontSize: 18,
    lineHeight: 20,
    marginLeft: 22,
    marginTop: 5
  },
  icon12Row: {
    height: 25,
    flexDirection: "row",
    flex: 1,
    marginRight: 173
  },
  rect2Column: {},
  rect2ColumnFiller: {
    flex: 1
  },
  rect6: {
    height: 84,
    backgroundColor: "#1c2a38",
    justifyContent: "center"
  },
  rect7: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-around",
    width: 375,
    height: 84,
    alignSelf: "center"
  },
  buttonqr: {
    top: 17,
    left: 50,
    width: 50,
    height: 52,
    justifyContent: "center",
    position: "absolute",
  },
  icon7: {
    color: "rgba(255,255,255,1)",
    fontSize: 40
  },

  home: {
    top: 17,
    left: 163,
    width: 50,
    height: 52,
    justifyContent: "center",
    position: "absolute"
  },

  icon8: {
    color: "rgba(255,255,255,1)",
    fontSize: 40
  },
  main: {
    top: 17,
    left: 285,
    width: 50,
    height: 52,
    justifyContent: "center",
    position: "absolute"
  },
  icon9: {
    color: "rgba(255,255,255,1)",
    fontSize: 40
  },
  error: {
    color: "#e36861",
    fontSize: 22,
    textAlign: "center",
    lineHeight: 20,
    marginTop: 340,
  }
});

export default QRcode;
