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
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch


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

    var data by remember {
        mutableStateOf("")
    }

    Column {
        TextField(
            value = data,
            onValueChange = { newValue ->
                data = newValue
            },
            label = {
                Text("Enter your question")
            }
        )

        Button(
            onClick = {

                CoroutineScope(Dispatchers.IO).launch {

                    try {

                        val response = ApiClient.api.analyzeRepository(
                            RepoRequest(data)
                        )

                        println(response.message)

                    } catch (e: Exception) {

                        println(e.message)

                    }
                }

            }
        ) {
            Text("Submit")
        }
    }
}