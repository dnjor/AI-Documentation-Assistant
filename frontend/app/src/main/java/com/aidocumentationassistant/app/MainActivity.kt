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
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll

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
    val scrollState = rememberScrollState()

    var data by remember {
        mutableStateOf("")
    }

    var answer by remember {
        mutableStateOf("")
    }

    var isLoading by remember {
        mutableStateOf(false)
    }

    Column(
        modifier = Modifier
            .verticalScroll(scrollState)
            .padding(20.dp)
    ) {
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

                        answer = response.answer

                    } catch (e: Exception) {

                        answer = "Error: ${e.message}"

                    } finally {
                        isLoading = false
                    }
                }

            }
        ) {
            if(isLoading) {
                Text("Analyzing..")
            } else {
                Text("Analyze Repository")
            }
        }

        if (isLoading) {

            CircularProgressIndicator()

        }

        if (answer.isNotEmpty()) {

            Text(
                text = answer,
                modifier = Modifier.padding(top = 20.dp)
            )

        }
    }
}