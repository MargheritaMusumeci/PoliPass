import { StatusBar } from 'expo-status-bar';
import React from 'react';
import { StyleSheet, Text, View } from 'react-native';
import { sin } from 'react-native/Libraries/Animated/Easing';
import Home from './app/screen/Home';
import Login from './app/screen/Login';
import Main from './app/screen/Main';
import QRcode from './app/screen/QRcode';
import Signup from './app/screen/Signup';

import { NavigationContainer } from '@react-navigation/native';
import {createStackNavigator} from '@react-navigation/stack';

const Stack = createStackNavigator();

const App = () => {
  return (
    <NavigationContainer>
      <Stack.Navigator>
      <Stack.Screen name="Main" component={Main}  options={{headerShown: false}} />
        <Stack.Screen name="Home" component={Home}   options={{headerShown: false}} />
        <Stack.Screen name="Login" component={Login}   options={{headerShown: false}} />
        <Stack.Screen name="QRcode" component={QRcode}   options={{headerShown: false}} />
      </Stack.Navigator>
    </NavigationContainer>
  );
};

export default App;
