package com.aidocumentationassistant.app

import retrofit2.http.Body
import retrofit2.http.POST

data class RepoRequest(
    val repoUrl: String
)

data class RepoResponse(
    val message: String
)

interface ApiService {
    @POST("analyze")
    suspend fun analyzeRepository(
        @Body request: RepoRequest
    ):RepoResponse
}
