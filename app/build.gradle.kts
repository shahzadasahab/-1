plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "com.sindhcs.crashcourse"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.sindhcs.crashcourse"
        minSdk = 24
        targetSdk = 34
        versionCode = 6
        versionName = "2.0.0"

        ndk {
            // arm64 keeps the embedded voice and the full booklet under the sideload size limit.
            abiFilters += listOf("arm64-v8a")
        }
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = "17"
    }

    buildFeatures {
        viewBinding = true
        buildConfig = true
    }

    packaging {
        jniLibs {
            useLegacyPackaging = true
        }
    }
}

tasks.register<Exec>("fetchEmbeddedTts") {
    workingDir = rootProject.projectDir
    commandLine("bash", "scripts/fetch_embedded_tts.sh")
    onlyIf {
        !file("src/main/assets/tts/ur_male/ur_PK-fasih-medium.onnx").exists() ||
            !file("libs/sherpa-onnx-android-arm.aar").exists()
    }
}

tasks.named("preBuild") {
    dependsOn("fetchEmbeddedTts")
}

dependencies {
    implementation("androidx.core:core-ktx:1.13.1")
    implementation("androidx.appcompat:appcompat:1.7.0")
    implementation("com.google.android.material:material:1.12.0")
    implementation("androidx.constraintlayout:constraintlayout:2.1.4")
    implementation("androidx.recyclerview:recyclerview:1.3.2")
    implementation("androidx.cardview:cardview:1.0.0")
    implementation("androidx.viewpager2:viewpager2:1.1.0")
    implementation("androidx.coordinatorlayout:coordinatorlayout:1.2.0")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.8.4")
    implementation(files("libs/sherpa-onnx-android-arm.aar"))
}
