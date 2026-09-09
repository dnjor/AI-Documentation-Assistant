package com.aidocumentationassistant.app

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.material3.Text
import androidx.compose.material3.TextField
import androidx.compose.material3.Button
import androidx.compose.foundation.layout.Column
import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue
import com.aidocumentationassistant.app.ui.theme.FrontendTheme


class MainActivity : ComponentActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setContent {
            FrontendTheme {
                MyInput()
            }
        }
    }
}


@Composable
fun MyInput() {

    var name by remember {
        mutableStateOf("")
    }

    var greeting by remember {
        mutableStateOf("")
    }

    Column {
        TextField(
            value = name,
            onValueChange = { newValue ->
                name = newValue
            },
            label = {
                Text("Enter your name")
            }
        )

        Button(
            onClick = {
                greeting = "hello $name"
            }
        ) {
            Text("Submit")
        }

        Text(
            text = greeting
        )
    }
}