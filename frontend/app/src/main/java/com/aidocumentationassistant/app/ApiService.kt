package com.aidocumentationassistant.app

import retrofit2.http.Body
import retrofit2.http.POST

data class RepoRequest(
    val message: String
)

data class RepoResponse(
    val mode: String,
    val answer: String
)

interface ApiService {
    @POST("ask_ai")
    suspend fun askAI(
        @Body request: RepoRequest
    ):RepoResponse
}
