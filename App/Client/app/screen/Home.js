import React, { Component } from "react";
import {
  StyleSheet,
  View,
  StatusBar,
  TouchableOpacity,
  Image,
  ScrollView,
  Text
} from "react-native";
import FontAwesomeIcon from "react-native-vector-icons/FontAwesome";
import IoniconsIcon from "react-native-vector-icons/Ionicons";
import MaterialCommunityIconsIcon from "react-native-vector-icons/MaterialCommunityIcons";
import FeatherIcon from "react-native-vector-icons/Feather";

const getInformation = async () => {
  try{
  let res = await fetch('http://localhost:3000/home');
  console.log(await res.text()) 
  }catch{
  console.error('error')
  }
}

function Home({ navigation }) {
  return (
    <View style={styles.rect}>
      <StatusBar hidden />
      <View style={styles.rect2Column}>
        <View style={styles.rect2}>
          <View style={styles.buttonRow}>
           
            <Image
              source={require("../assets/logo.png")}
              resizeMode="contain"
              style={styles.image1}
            ></Image>
          </View>
        </View>
        <View style={styles.scrollAreaStack}>
          <View style={styles.scrollArea}>
            <ScrollView
              horizontal={false}
              contentContainerStyle={styles.scrollArea_contentContainerStyle}
            >
              <Text style={styles.greenPassCovid20}>Green Pass COVID-19</Text>
              <View style={styles.rect17}>
                <View style={styles.icon10Row}>
                  <FontAwesomeIcon
                    name="user-o"
                    style={styles.icon10}
                  ></FontAwesomeIcon>
                  <Text style={styles.surnameName}>Surname Name</Text>
                </View>
              </View>
              <Text style={styles.rossiMario}>Rossi Mario</Text>
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
                <Text style={styles.dateOfBirth1}>1999-10-9</Text>
              </View>
              <View style={styles.rect19}>
                <View style={styles.icon11Row}>
                  <IoniconsIcon
                    name="md-finger-print"
                    style={styles.icon11}
                  ></IoniconsIcon>
                  <Text style={styles.text2}>
                    Unique certificate identifier
                  </Text>
                </View>
              </View>
              <Text style={styles.a98Shi19Y33}>A98SHI19Y33</Text>
              <View style={styles.rect16}>
                <View style={styles.icon15Row}>
                  <FontAwesomeIcon
                    name="heartbeat"
                    style={styles.icon15}
                  ></FontAwesomeIcon>
                  <Text style={styles.vaccineProphylaxis1}>
                    Vaccine/Prophylaxis
                  </Text>
                </View>
              </View>
              <Text style={styles.moderna}>SARS-CoV-2 mRNA vaccine</Text>
              <View style={styles.rect11}>
                <View style={styles.icon12Row}>
                  <MaterialCommunityIconsIcon
                    name="medical-bag"
                    style={styles.icon12}
                  ></MaterialCommunityIconsIcon>
                  <Text style={styles.text3}>Vaccine medicinal product</Text>
                </View>
              </View>
              <Text style={styles.comirnaty}>Comirnaty</Text>
              <View style={styles.rect15}>
                <View style={styles.icon19Row}>
                  <MaterialCommunityIconsIcon
                    name="hospital-building"
                    style={styles.icon19}
                  ></MaterialCommunityIconsIcon>
                  <Text style={styles.issuedBy2}>Issued by</Text>
                </View>
              </View>
              <Text style={styles.ministryOfHealth}>Ministry of health</Text>
              <View style={styles.rect14}>
                <View style={styles.icon14Row}>
                  <MaterialCommunityIconsIcon
                    name="table-column-plus-before"
                    style={styles.icon14}
                  ></MaterialCommunityIconsIcon>
                  <Text style={styles.numberOfDoses}>Number of doses</Text>
                </View>
              </View>
              <Text style={styles.numberOfDoses1}>2/2</Text>
              <View style={styles.rect12}>
                <View style={styles.icon13Row}>
                  <FontAwesomeIcon
                    name="calendar"
                    style={styles.icon13}
                  ></FontAwesomeIcon>
                  <Text style={styles.dateOfVaccine}>Date of vaccine</Text>
                </View>
              </View>
              <Text style={styles.dateOfVaccine1}>2021-06-17</Text>
              <View style={styles.rect13Stack}>
                <View style={styles.rect13}>
                  <View style={styles.icon18Row}>
                    <FontAwesomeIcon
                      name="map-pin"
                      style={styles.icon18}
                    ></FontAwesomeIcon>
                    <Text style={styles.surnameName2}>
                      Member State of vaccination
                    </Text>
                  </View>
                </View>
                <Text style={styles.italy}>Italy</Text>
              </View>
            </ScrollView>
          </View>
          <TouchableOpacity style={styles.button8}>
            <View style={styles.rect5}>
              <MaterialCommunityIconsIcon
                name="download"
                style={styles.icon5}
              ></MaterialCommunityIconsIcon>
            </View>
          </TouchableOpacity>
        </View>
      </View>
      <View style={styles.rect2ColumnFiller}></View>
      <View style={styles.rect6}>
        <View style={styles.rect7}>
          <TouchableOpacity
            onPress={() => navigation.navigate("Home")}
            style={styles.button9}
          >
          <MaterialCommunityIconsIcon
            name="reload"
            style={styles.icon7}
          ></MaterialCommunityIconsIcon>
          </TouchableOpacity>
          <TouchableOpacity
            onPress={() => navigation.navigate("QRcode")}
            style={styles.button10}
          >
          <MaterialCommunityIconsIcon
            name="qrcode"
            style={styles.icon8}
          ></MaterialCommunityIconsIcon>
          </TouchableOpacity>
          <TouchableOpacity
            onPress={() => navigation.navigate("Main")}
            style={styles.button11}
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
  button: {
    width: 50,
    height: 50
  },
  image: {
    width: 50,
    height: 50,
    borderRadius: 100
  },
  image1: {
    height: 50,
    width: 50,
    marginLeft: 150,
    marginTop: 17
  },
  buttonRow: {
    height: 67,
    flexDirection: "row",
    flex: 1,
    marginRight: 169,
    marginLeft: 17,
    marginTop: 17
  },
  scrollArea: {
    top: 0,
    left: 0,
    height: 610,
    position: "absolute",
    right: 0
  },
  scrollArea_contentContainerStyle: {
    height: 610
  },
  greenPassCovid20: {
    color: "rgba(255,255,255,1)",
    fontSize: 24,
    marginTop: 6,
    fontWeight: "bold",
    marginLeft: 52
  },
  rect17: {
    width: 343,
    height: 25,
    flexDirection: "row",
    marginTop: 30
  },
  icon10: {
    color: "#8899a6",
    fontSize: 25
  },
  surnameName: {
    color: "rgba(255,255,255,1)",
    fontSize: 18,
    lineHeight: 20,
    marginLeft: 22,
    marginTop: 3
  },
  icon10Row: {
    height: 25,
    flexDirection: "row",
    flex: 1,
    marginRight: 173
  },
  rossiMario: {
    color: "rgba(255,255,255,1)",
    fontSize: 18,
    lineHeight: 20,
    marginLeft: 43
  },
  rect18: {
    width: 343,
    height: 25,
    position: "absolute",
    top: 0,
    left: 0,
    flexDirection: "row"
  },
  icon17: {
    color: "#8899a6",
    fontSize: 25
  },
  dateOfBirth: {
    color: "#fefefe",
    fontSize: 18,
    lineHeight: 20,
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
    top: 24,
    left: 43,
    color: "#fefefe",
    position: "absolute",
    fontSize: 18,
    lineHeight: 20
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
    marginTop: 16
  },
  icon11: {
    color: "#8899a6",
    fontSize: 25
  },
  text2: {
    color: "#fefefe",
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
    color: "#fefefe",
    fontSize: 18,
    lineHeight: 20,
    marginTop: 1,
    marginLeft: 43
  },
  rect16: {
    width: 343,
    height: 25,
    flexDirection: "row",
    marginTop: 14
  },
  icon15: {
    color: "#8899a6",
    fontSize: 25
  },
  vaccineProphylaxis1: {
    color: "#fefefe",
    fontSize: 18,
    lineHeight: 20,
    marginLeft: 18,
    marginTop: 3
  },
  icon15Row: {
    height: 25,
    flexDirection: "row",
    flex: 1,
    marginRight: 134
  },
  moderna: {
    color: "#fefefe",
    fontSize: 18,
    lineHeight: 20,
    marginTop: 1,
    marginLeft: 43
  },
  rect11: {
    width: 343,
    height: 25,
    flexDirection: "row",
    marginTop: 14
  },
  icon12: {
    color: "#8899a6",
    fontSize: 25
  },
  text3: {
    color: "#fefefe",
    fontSize: 18,
    lineHeight: 20,
    marginLeft: 18,
    marginTop: 3
  },
  icon12Row: {
    height: 27,
    flexDirection: "row",
    flex: 1,
    marginRight: 82
  },
  comirnaty: {
    color: "#fefefe",
    fontSize: 18,
    lineHeight: 20,
    marginLeft: 45
  },
  rect15: {
    width: 343,
    height: 25,
    flexDirection: "row",
    marginTop: 15
  },
  icon19: {
    color: "#8899a6",
    fontSize: 25
  },
  issuedBy2: {
    color: "#fefefe",
    fontSize: 18,
    lineHeight: 20,
    marginLeft: 18,
    marginTop: 3
  },
  icon19Row: {
    height: 27,
    flexDirection: "row",
    flex: 1,
    marginRight: 221
  },
  ministryOfHealth: {
    color: "#fefefe",
    fontSize: 18,
    lineHeight: 20,
    marginLeft: 45
  },
  rect14: {
    width: 343,
    height: 25,
    flexDirection: "row",
    marginTop: 15
  },
  icon14: {
    color: "#8899a6",
    fontSize: 25
  },
  numberOfDoses: {
    color: "#fefefe",
    fontSize: 18,
    lineHeight: 20,
    marginLeft: 18,
    marginTop: 3
  },
  icon14Row: {
    height: 27,
    flexDirection: "row",
    flex: 1,
    marginRight: 158
  },
  numberOfDoses1: {
    color: "#fefefe",
    fontSize: 18,
    lineHeight: 20,
    marginLeft: 43
  },
  rect12: {
    width: 343,
    height: 23,
    flexDirection: "row",
    marginTop: 15
  },
  icon13: {
    color: "#8899a6",
    fontSize: 25
  },
  dateOfVaccine: {
    color: "#fefefe",
    fontSize: 18,
    lineHeight: 20,
    marginLeft: 20,
    marginTop: 6
  },
  icon13Row: {
    height: 26,
    flexDirection: "row",
    flex: 1,
    marginRight: 173
  },
  dateOfVaccine1: {
    color: "#fefefe",
    fontSize: 18,
    lineHeight: 20,
    marginTop: 2,
    marginLeft: 43
  },
  rect13: {
    width: 343,
    height: 28,
    position: "absolute",
    top: 0,
    left: 0,
    flexDirection: "row"
  },
  icon18: {
    color: "#8899a6",
    fontSize: 25
  },
  surnameName2: {
    color: "#fefefe",
    fontSize: 18,
    lineHeight: 20,
    marginLeft: 29,
    marginTop: 3
  },
  icon18Row: {
    height: 25,
    flexDirection: "row",
    flex: 1,
    marginRight: 64
  },
  italy: {
    top: 25,
    left: 43,
    color: "#fefefe",
    position: "absolute",
    fontSize: 18,
    lineHeight: 20
  },
  rect13Stack: {
    width: 343,
    height: 45,
    marginTop: 15
  },
  button8: {
    width: 80,
    height: 80,
    backgroundColor: "#1da6fa",
    position: "absolute",
    right: 4,
    bottom: 0,
    borderRadius: 100,
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
  scrollAreaStack: {
    height: 620,
    marginTop: 10,
    marginLeft: 19,
    marginRight: 13
  },
  rect2Column: {
    marginLeft: -3,
    marginRight: 3
  },
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
  button9: {
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
  button10: {
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
  button11: {
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

export default Home;
