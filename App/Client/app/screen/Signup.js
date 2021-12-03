import React, { Component } from "react";
import {
  StyleSheet,
  View,
  StatusBar,
  Image,
  Text,
  TextInput,
  TouchableOpacity
} from "react-native";
import Divider from "./components/Divider";

const doSignup = async (navigation) => {
  try{
    let res = await fetch('http://localhost:3000/signup', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({a: 3, b: 'Textual content'})
    });

    console.log(await res.text()) 
    
  }catch{
    console.error('error')
  }

  navigation.navigate("Login")
}

function Signup({ navigation }) {
  return (
    
    <View style={styles.rect}>
    <StatusBar hidden />
      <View style={styles.image1Column}>
        <Image
          source={require("../assets/logo.png")}
          resizeMode="contain"
          style={styles.logo}
        ></Image>
        <Text style={styles.title}>Create your account</Text>
        <TextInput
          placeholder="Name"
          placeholderTextColor="#788793"
          style={styles.inputTextPrimary}
        ></TextInput>
        <TextInput
          placeholder="Surname"
          placeholderTextColor="rgba(120,135,147,1)"
          style={styles.inputText}
        ></TextInput>
        <TextInput
          placeholder="Birthday "
          placeholderTextColor="#788793"
          style={styles.inputText}
        ></TextInput>
        <TextInput
          placeholder="Email address"
          placeholderTextColor="#788793"
          style={styles.inputText}
        ></TextInput>
        <TextInput
          placeholder="Phone number "
          placeholderTextColor="rgba(120,135,147,1)"
          style={styles.inputText}
        ></TextInput>
        <TextInput
          placeholder="Street"
          placeholderTextColor="rgba(120,135,147,1)"
          style={styles.inputText}
        ></TextInput>
        <TextInput
          placeholder="City"
          placeholderTextColor="rgba(120,135,147,1)"
          style={styles.inputText}
        ></TextInput>
        <TextInput
          placeholder="Country"
          placeholderTextColor="#788793"
          style={styles.inputText}
        ></TextInput>
        <TextInput
          placeholder="ZIP "
          placeholderTextColor="#788793"
          style={styles.inputText}
        ></TextInput>
        <TextInput
          placeholder="Password"
          placeholderTextColor="#788793"
          secureTextEntry={true}
          style={styles.inputText}
        ></TextInput>
        <TextInput
          placeholder="Repeated password"
          secureTextEntry={true}
          placeholderTextColor="#788793"
          style={styles.inputText}
        ></TextInput>
          </View>
          <View style={styles.image1ColumnFiller}></View>
         <View style={styles.textInput4Column}>
         <View style={styles.rect4}>
        <Divider style={styles.divider}></Divider>
        <View style={styles.buttonRow}>
          <TouchableOpacity
            onPress={() => navigation.navigate("Main")}
            style={styles.button}
          >
            <Text style={styles.text2}>Back</Text>
          </TouchableOpacity>
          <TouchableOpacity
            onPress={() => doSignup(navigation)}
            style={styles.button2}
          >
            <Text style={styles.text6}>Next</Text>
          </TouchableOpacity>
        </View>
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
  logo: {
    height: 80,
    width: 80,
    marginLeft: 118
  },
  title: {
    color: "rgba(255,255,255,1)",
    fontSize: 30,
    lineHeight: 50,
    fontWeight: "bold",
    marginTop: 13
  },
  inputTextPrimary: {
    width: 313,
    height: 42,
    color: "#1da1f2",
    borderColor: "#1da1f2",
    borderWidth: 0,
    borderBottomWidth: 2,
    fontSize: 18,
    lineHeight: 20,
    marginTop: 20,
    marginLeft: 6
  },
  inputText: {
    width: 313,
    height: 42,
    color: "#1da1f2",
    borderColor: "rgba(123,139,151,1)",
    borderWidth: 0,
    borderBottomWidth: 2,
    fontSize: 18,
    lineHeight: 20,
    marginTop: 3,
    marginLeft: 6
  },
  
  image1Column: {
    width: 316,
    marginTop: 47,
    marginLeft: 30
  },
  image1ColumnFiller: {
    flex: 1
  },

  div2: {
    height: 91
  },
  divider: {
    width: 360,
    height: 1
  },
  login: {
    width: 109,
    height: 50,
    backgroundColor: "#1da1f2",
    borderRadius: 100,
    marginTop: 25,
    marginLeft: 240
  },
  text3: {
    color: "#ffffff",
    fontSize: 20,
    lineHeight: 20,
    marginTop: 15,
    marginLeft: 28
  },
  textInput4Column: {
    marginBottom: 29
  },
  rect4: {
    paddingTop:25,
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
  }
});

export default Signup;
