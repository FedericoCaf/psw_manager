import { KeyboardAvoidingView, SafeAreaView, StyleSheet, Text, View } from 'react-native'
import React from 'react'
import { useNavigation } from '@react-navigation/native';

const HomeScreen = () => {

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const navigation = useNavigation();

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


    return (
        <SafeAreaView style={{ flex: 1, backgroundColor: "white", alignItems: "center" }}>
            <KeyboardAvoidingView>

                <View style={{ marginTop: 80 }}>
                    <Text>HomeScreen</Text>
                </View>

            </KeyboardAvoidingView>

        </SafeAreaView>
    )
}

export default HomeScreen

const styles = StyleSheet.create({})