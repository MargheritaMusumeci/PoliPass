import React, { Component } from "react";
import {
  StyleSheet,
  View,
  StatusBar,
  Text,
  TouchableOpacity,
  Image
} from "react-native";

function Main({ navigation }) {
  
  return (
    <View style={styles.rect}>
      <StatusBar hidden />
      <Image
          source={require("../assets/logo.png")}
          resizeMode="contain"
          style={styles.logo}
        ></Image>

      <View style={styles.textColumn}>
        <Text style={styles.text}>
          Consult your green pass whenever and wherever you want!
        </Text>
        <TouchableOpacity
          onPress={() => navigation.navigate("Signup")}
          style={styles.signup}
        >
          <Text style={styles.button_text}>Create account</Text>
        </TouchableOpacity>
  
      </View>
      <View style={styles.textColumnFiller}></View>
      <View style={styles.div}>
        <TouchableOpacity
          onPress={() => navigation.navigate("Login")}
        >
          <Text style={styles.login}>Have an account already?</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  rect: {
    flex: 1,
    backgroundColor: "rgba(21,31,40,1)"
  },
  text: {
    height: 207,
    color: "rgba(255,255,255,1)",
    fontSize: 34,
    lineHeight: 50,
    textAlign: "left",
    width: 306,
    marginTop: 0,
    fontWeight: "bold",
    marginLeft: 6
  },
  signup: {
    height: 81,
    backgroundColor: "rgba(29,161,242,1)",
    borderRadius: 100,
    justifyContent: "center",
    marginTop: 20
  },
  button_text: {
    color: "rgba(255,255,255,1)",
    fontSize: 24,
    alignSelf: "center"
  },
  logo: {
    height: 200,
    width: 200,
    marginTop: 100,
    marginLeft: 100
  },

  textColumn: {
    marginTop: 67,
    marginLeft: 28,
    marginRight: 34
  },
  textColumnFiller: {
    flex: 1
  },
  div: {
    height: 39,
    marginBottom: 45,
    marginLeft: 28,
    marginRight: 28
  },
  login: {
    color: "rgba(255,255,255,1)",
    fontSize: 20,
    marginTop: 13
  }
});

export default Main;
