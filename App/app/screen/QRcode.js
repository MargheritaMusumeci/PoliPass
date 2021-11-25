import React, { Component } from "react";
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

function QRcode({ navigation }) {
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
        <View style={styles.a21Row}>
          <Text style={styles.a21}>A98SHI19Y33</Text>
          <View style={styles.a21Filler}></View>
          <TouchableOpacity style={styles.download}>
            <View style={styles.rect5}>
              <MaterialCommunityIconsIcon
                name="download"
                style={styles.icon5}
              ></MaterialCommunityIconsIcon>
            </View>
          </TouchableOpacity>
        </View>
        <Image
          source={require("../assets/qr-code.png")}
          resizeMode="contain"
          style={styles.qrcode}
        ></Image>
        <Text style={styles.greenPassCovid20}>Green Pass COVID-19</Text>
        <View style={styles.dateOfBirth1Stack}>
          <Text style={styles.dateOfBirth1}>1999-10-9</Text>
          <View style={styles.rect10}>
            <View style={styles.icon11Row}>
              <FontAwesomeIcon
                name="birthday-cake"
                style={styles.icon11}
              ></FontAwesomeIcon>
              <Text style={styles.dateOfBirth2}>Date of birth</Text>
            </View>
          </View>
        </View>
        <Text style={styles.name}>Rossi Mario</Text>
        <View style={styles.rect9}>
          <View style={styles.icon10Row}>
            <IoniconsIcon
              name="md-finger-print"
              style={styles.icon10}
            ></IoniconsIcon>
            <Text style={styles.text1}>Unique certificate identifier</Text>
          </View>
        </View>
        <View style={styles.rect11}>
          <View style={styles.icon12Row}>
            <FontAwesomeIcon
              name="user-o"
              style={styles.icon12}
            ></FontAwesomeIcon>
            <Text style={styles.surnameName1}>Surname Name</Text>
          </View>
        </View>
      </View>
      <View style={styles.rect2ColumnFiller}></View>
      <View style={styles.rect6}>
        <View style={styles.rect7}>
          <TouchableOpacity
            onPress={() => navigation.navigate("QRcode")}
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
            onPress={() => navigation.navigate("Main")}
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
  dateOfBirth1: {
    top: 24,
    left: 44,
    color: "#fefefe",
    position: "absolute",
    fontSize: 18,
    lineHeight: 20
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
    marginTop: 3
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
  }
});

export default QRcode;
