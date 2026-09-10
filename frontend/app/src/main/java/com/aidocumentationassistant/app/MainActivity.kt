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
import android.util.Log

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

    var isLoading by remember {
        mutableStateOf(false)
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
            enabled = !isLoading,
            onClick = {

                isLoading = true

                Log.d("BUTTON_TEST", "Button clicked")

                CoroutineScope(Dispatchers.IO).launch {

                    try {

                        Log.d("API_TEST", "Sending request...")

                        val response = ApiClient.api.askAI(
                            RepoRequest(message = data)
                        )

                        Log.d("API_TEST", response.answer)

                    } catch (e: Exception) {

                        Log.e("API_ERROR", e.message ?: "Unknown error")

                    } finally {
                        isLoading = false
                    }
                }

            }
        ) {
            if(isLoading) {
                Text("Loding..")
            } else {
                Text("Submit")
            }
        }
    }
}