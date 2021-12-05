import React, { Component, useState } from "react";
import {
  StyleSheet,
  View,
  StatusBar,
  Text,
  Image,
  TouchableOpacity,
  TextInput
} from "react-native";
import Divider from "./components/Divider";

function Login({navigation}) {

  const [shouldShow, setShouldShow] = useState(true);
  const [error, setError] = useState(true);
  const [errorMessage, setErrorMessage] = useState('Invalid email or password...');
  const [mail, setMail] = useState('');
  const [password, setPassword] = useState('');

  const doLogin = async (navigation) => {

    // catch input variables 
    let mail_input = mail;
    let password_input = password;
  
    // check input variables
    if (mail_input == '' ){
      setErrorMessage("Email is missing...");
      if (error == true ) setError(!error);
      return;
    }

    if ((mail_input.includes('@') == -1) || (mail_input.includes(".") == -1)){
      setErrorMessage("Invalid email...");
      if (error == true ) setError(!error);
      return;
    }

    if (password_input == ''){
      setErrorMessage("Password is missing...");
      if (error == true ) setError(!error);
      return;
    }
  
    // send input variables for continuing checks 
    try{
      let res = await fetch('http://localhost:3000/login', {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({Mail: mail, Password: password})
      });
  
      let server_message = '';
      server_message = await res.text(); 

      console.log(server_message)

      if (server_message == "Ack"){
        navigation.navigate("Home");
        
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

  return (
    <View style={styles.rect}>
      <StatusBar hidden />
      <View style={styles.textColumn}>
        <Text style={styles.text}>Log in</Text>
        <View style={styles.div}>
          <Image
            source={require("../assets/logo.png")}
            resizeMode="contain"
            style={styles.logo}
          ></Image>
          
        </View>
        <Text style={styles.email}>Email</Text>
        <TextInput placeholder=""
          onChangeText={mail => setMail(mail)}
          defaultValue={mail}
          autoCapitalize='none'
         style={styles.textInputEmail}></TextInput>
        <Text style={styles.password}>Password</Text>
        <TextInput
          placeholder=""
          autoCapitalize='none'
          onChangeText={password => setPassword(password)}
          defaultValue={password}
          secureTextEntry={true}
          style={styles.textInputPassword}
        ></TextInput>
        </View>
        <View style={styles.textColumnFiller}>
          
          { (!error && shouldShow) ? <Text style={styles.error}> {errorMessage} </Text>
          : null }
      
        {shouldShow ?
        ( <TouchableOpacity onPress={() => setShouldShow(!shouldShow)}>
          <Text style={styles.text5}>Forgotten your password?</Text>
        </TouchableOpacity>) : (
          <View style={styles.textColumnFiller}>
            <TouchableOpacity onPress={() => setShouldShow(!shouldShow)}>
        <Text style={styles.easter_egg_text}>We can’t give you your password back, but we can wish you a Merry Christmas! </Text>
      </TouchableOpacity><Image
            source={require("../assets/santa-claus.png")}
            resizeMode="contain"
            style={styles.easter_egg}
      ></Image></View>
        ) }

        </View>
      <View style={styles.rect4}>
        <Divider style={styles.divider}></Divider>
        <View style={styles.buttonRow}>
          <TouchableOpacity
            onPress={() => navigation.navigate("Main")}
            style={styles.button}>
            <Text style={styles.text2}>Back</Text>
          </TouchableOpacity>
          <TouchableOpacity
            onPress={() => doLogin(navigation)}
            style={styles.button2}
          >
            <Text style={styles.text6}>Log in</Text>
          </TouchableOpacity>
        </View>
        </View>
    </View>
  );
}

const styles = StyleSheet.create({
  rect: {
    flex: 1,
    backgroundColor: "#141f28"
  },
  text: {
    color: "rgba(255,255,255,1)",
    fontSize: 30,
    lineHeight: 50,
    fontWeight: "bold",
    marginTop: 158,
    marginLeft: 18
  },
  div: {
    height: 118,
    backgroundColor: "#1c2a38",
    marginTop: -208
  },
  logo: {
    height: 80,
    width: 80,
    marginTop: 38,
    marginLeft: 154

  },
  div2: {
    width: 124,
    height: 50,
    alignSelf: "flex-end",
    marginTop: 100,
    marginRight: 250
  },
  singupButton: {
    width: 85,
    height: 50,
    justifyContent: "center",
    marginTop: 60,
    marginLeft: 10
  },
  text2: {
    width: 66,
    height: 50,
    color: "#1da1f2",
    fontSize: 18,
    lineHeight: 50,
    alignSelf: "center"
  },
  email: {
    color: "rgba(123,139,151,1)",
    fontSize: 18,
    lineHeight: 20,
    marginTop: 121,
    marginLeft: 18
  },
  password: {
    color: "rgba(123,139,151,1)",
    fontSize: 18,
    lineHeight: 20,
    marginTop: 50,
    marginLeft: 18
  },
  textInputPassword: {
    width: 339,
    height: 42,
    color: "#1da1f2",
    borderColor: "rgba(123,139,151,1)",
    borderWidth: 0,
    borderBottomWidth: 2,
    fontSize: 18,
    lineHeight: 20,
    marginTop: 3,
    marginLeft: 18
  },
  text5: {
    color: "#7b8b97",
    fontSize: 18,
    lineHeight: 20,
    marginTop: 50,
    marginLeft: 83
  },
  textInputEmail: {
    width: 339,
    height: 42,
    color: "#1da1f2",
    borderColor: "#1da1f2",
    borderWidth: 0,
    borderBottomWidth: 2,
    fontSize: 18,
    lineHeight: 20,
    marginTop: 0,
    marginLeft: 18
  },
  textColumn: {},

  textColumnFiller: {
    flex: 1
  },
  rect4: {
    height: 91
  },
  divider: {
    width: 360,
    height: 1
  },
  button: {
    width: 85,
    height: 50,
    marginTop: 4
  },
  text2: {
    width: 66,
    height: 50,
    color: "#1da1f2",
    fontSize: 18,
    lineHeight: 50,
    marginLeft: 9
  },
  button2: {
    width: 109,
    height: 50,
    backgroundColor: "#1da1f2",
    borderRadius: 100,
    justifyContent: "center",
    marginLeft: 124
  },
  text6: {
    color: "#ffffff",
    fontSize: 20,
    lineHeight: 20,
    alignSelf: "center"
  },
  buttonRow: {
    height: 54,
    flexDirection: "row",
    marginTop: 13,
    marginLeft: 31,
    marginRight: 26
  },
  easter_egg: {
    height: 180,
    width: 180,
    marginTop: 38,
    marginLeft: 110,

  },
  easter_egg_text:{
    color: "#e36861",
    fontSize: 18,
    lineHeight: 20,
    marginTop: 60,
    marginLeft: 40,
    marginRight:40,
    textAlign: 'center',
  },
  error: {
    color: "#e36861",
    fontSize: 18,
    lineHeight: 20,
    marginTop: 40,
    marginLeft: 83
  }
});
export default Login;
