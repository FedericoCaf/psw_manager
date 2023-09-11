import { StyleSheet, Text, View, SafeAreaView, Image, KeyboardAvoidingView, TextInput, Pressable, Alert } from 'react-native'
import React, { useState, useRef } from 'react'
import { Feather } from '@expo/vector-icons';
import { AntDesign } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import axios from 'axios';

const LoginScreen = () => {

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const navigation = useNavigation();
    const inputRef = React.useRef();

    const handleLogin = () => {
        const user = {
            username: username,
            password: password,
        }

        const config = {
            headers: {
                Accept: 'application/json',
                "content-type": "application/json",
            },
        }

        axios.post("http://127.0.0.1:5000/login", user, config).then((response) => {
            console.log(response.data.token);
            setUsername("");
            setPassword("");
            const token = response.data.token;
            AsyncStorage.setItem("authToken", token);
            navigation.replace("Home");

        }).catch((error) => {
            Alert.alert(
                error.response.data.message
            );
            console.log("Wrong credentials", error.response.data.message)
        })
    }

    const handlePress = () => {
        inputRef.current?.focus();
    }

    return (
        <SafeAreaView style={{ flex: 1, backgroundColor: "white", alignItems: "center" }}>

            <View>
                <Image
                    style={{ marginTop: 80, width: 150, height: 160 }}
                    source={{
                        uri: "https://assets.stickpng.com/thumbs/5f53a54d060f2e00048580ea.png"
                    }}
                />
            </View>

            <KeyboardAvoidingView>
                <View>
                    <Text style={{ fontSize: 26, color: "#6495ed", fontWeight: "bold", marginTop: 12, alignSelf: "center" }}>
                        Login in to your account
                    </Text>
                </View>


                <Pressable onPress={handlePress}>
                    <View style={{ flexDirection: "row", alignItems: "center", gap: 5, width: 300, padding: 10, borderWidth: 0.5, borderRadius: 5, marginTop: 20 }}>
                        <Feather name="user" size={24} color="gray" />
                        <TextInput
                            ref={inputRef}
                            value={username}
                            onChangeText={(username) => setUsername(username)}
                            style={{ color: "gray", flex: 1 }} placeholder='Username'
                        />
                    </View>
                </Pressable>


                <Pressable onPress={handlePress}>
                    <View style={{ flexDirection: "row", alignItems: "center", gap: 5, width: 300, padding: 10, borderWidth: 0.5, borderRadius: 5, marginTop: 30 }}>
                        <AntDesign name="lock1" size={24} color="gray" />
                        <TextInput
                            secureTextEntry={true}
                            ref={inputRef}
                            value={password}
                            onChangeText={(password) => setPassword(password)}
                            style={{ color: "gray", flex: 1 }} placeholder='Password'
                        />
                    </View>
                </Pressable>

                <View style={{ marginTop: 5, flexDirection: "row", justifyContent: "space-between" }}>
                    <Text style={{ fontSize: 12 }}> Keep me logged in  </Text>
                    <Pressable>
                        <Text style={{ color: "blue", fontSize: 12 }}> Forgot password </Text>
                    </Pressable>

                </View>

                <Pressable onPress={handleLogin}
                    style={{
                        marginTop: 70,
                        width: 300,
                        backgroundColor: "#6495ed",
                        borderRadius: 5,
                        marginLeft: "auto",
                        marginRight: "auto",
                        padding: 15,
                    }}>

                    <Text style={{ textAlign: "center", color: "white", fontSize: 16, fontWeight: "bold" }}> Login </Text>


                </Pressable>


                <View>
                    <Text style={{ marginTop: 50, textAlign: "center" }}>Don't have an account? </Text>
                    <Pressable
                        style={{
                            marginTop: 10,
                            backgroundColor: "#6495ed",
                            borderRadius: 5,
                            marginLeft: "auto",
                            marginRight: "auto",
                            padding: 10,
                        }}
                        onPress={() => navigation.navigate("Register")} >
                        <Text style={{ color: "white" }}> Sign up</Text>
                    </Pressable>
                </View>





            </KeyboardAvoidingView>

        </SafeAreaView>
    )
}

export default LoginScreen

const styles = StyleSheet.create({})