import { StyleSheet, Text, View, SafeAreaView, Image, KeyboardAvoidingView, TextInput, TouchableWithoutFeedback, Pressable, Alert, Keyboard, TouchableOpacity} from 'react-native'
import React, { useState, useRef } from 'react'
import { useNavigation } from '@react-navigation/native';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { Feather } from '@expo/vector-icons';
import { AntDesign } from '@expo/vector-icons';
import axios from 'axios';

const RegisterScreen = () => {
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [password2, setPassword2] = useState("");
    const navigation = useNavigation();

    const handleRegister = () => {
        const user = {
            username: username,
            email: email,
            password: password,
            password2: password2
        }

        const config = {
            headers: {
                 Accept: 'application/json',
                "content-type": "application/json",
            },
        }

        axios.post("http://127.0.0.1:5000/register", user, config).then((response) => {
            console.log(response);
            Alert.alert(
                "Registration successfully"
            );
            setUsername("");
            setEmail("")
            setPassword("")
            setPassword2("")
        }).catch((error) => {
            Alert.alert(
                error.response.data.message
            );
            console.log("registration failed", error.response.data.message)
        })
    }

  const inputRef = React.useRef()

  const handlePress = () => {
      inputRef.current?.focus();
}

    return (
        <SafeAreaView style={{ flex: 1, backgroundColor: "white", alignItems: "center" }}>

            <View>
                <Image
                    style={{ marginTop: 50, width: 150, height: 160 }}
                    source={{
                        uri: "https://assets.stickpng.com/thumbs/5f53a54d060f2e00048580ea.png"
                    }}
                />
            </View>

            <KeyboardAvoidingView>
                <View>
                    <Text style={{ fontSize: 26, color: "#6495ed", fontWeight: "bold", marginTop: 12, alignSelf: "center" }}>
                        Registrer account
                    </Text>
                </View>
                  
                <Pressable onPress={handlePress}>
                        <View style={{ flexDirection: "row", alignItems: "center", gap: 5, width: 300, padding: 10, borderWidth:0.5, borderRadius: 5, marginTop: 20 }}>
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
                        <View style={{ flexDirection: "row", alignItems: "center", gap: 5, width: 300, padding: 10, borderWidth:0.5, borderRadius: 5, marginTop: 30 }}>
                           <MaterialCommunityIcons name="email-outline" size={24} color="gray" />
                            <TextInput
                                ref={inputRef}
                                value={email}
                                onChangeText={(email) => setEmail(email)}
                                style={{ color: "gray", flex: 1 }} placeholder='Email'
                            />
                        </View>   
                </Pressable>   

                <Pressable onPress={handlePress}>
                        <View style={{ flexDirection: "row", alignItems: "center", gap: 5, width: 300, padding: 10, borderWidth:0.5, borderRadius: 5, marginTop: 30 }}>
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


                <Pressable onPress={handlePress}>
                        <View style={{ flexDirection: "row", alignItems: "center", gap: 5, width: 300, padding: 10, borderWidth:0.5, borderRadius: 5, marginTop: 10 }}>
                            <AntDesign name="lock1" size={24} color="gray" />
                            <TextInput
                                secureTextEntry={true}
                                ref={inputRef}
                                value={password2}
                                onChangeText={(password2) => setPassword2(password2)}
                                style={{ color: "gray", flex: 1 }} placeholder='Repeat password'
                            />
                        </View>   
                </Pressable>   


                <Pressable
                    onPress={handleRegister}
                    style={{
                        marginTop: 30,
                        width: 300,
                        backgroundColor: "#6495ed",
                        borderRadius: 5,
                        marginLeft: "auto",
                        marginRight: "auto",
                        padding: 15,
                    }}
                >

                    <Text style={{ textAlign: "center", color: "white", fontSize: 16, fontWeight: "bold" }}> Sign up </Text>


                </Pressable>

                <View>
                    <Text style={{ marginTop: 50, textAlign: "center" }}>Already have an account? </Text>
                    <Pressable
                        style={{
                            marginTop: 10,
                            // width: 300,
                            backgroundColor: "#6495ed",
                            borderRadius: 5,
                            marginLeft: "auto",
                            marginRight: "auto",
                            padding: 10,
                        }}
                        onPress={() => navigation.navigate("Login")} >
                        <Text style={{ color: "white" }}> Sign in</Text>
                    </Pressable>
                </View>







            </KeyboardAvoidingView>

        </SafeAreaView>
    )
}

export default RegisterScreen

const styles = StyleSheet.create({})