plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "com.cslectures.notes"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.cslectures.notes"
        minSdk = 24
        targetSdk = 34
        versionCode = 2
        versionName = "1.1.0"
        ndk {
            // Phones: 64-bit and older 32-bit ARM. x86 is omitted to keep the download small.
            abiFilters += listOf("arm64-v8a", "armeabi-v7a")
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
    }

    packaging {
        jniLibs {
            // Compress native libraries so the downloadable APK stays smaller.
            useLegacyPackaging = true
        }
    }
}

dependencies {
    implementation(files("libs/sherpa-onnx-1.13.8.aar"))
    implementation("androidx.core:core-ktx:1.13.1")
    implementation("androidx.appcompat:appcompat:1.7.0")
    implementation("com.google.android.material:material:1.12.0")
    implementation("androidx.recyclerview:recyclerview:1.3.2")
    implementation("androidx.constraintlayout:constraintlayout:2.1.4")
    implementation("androidx.webkit:webkit:1.11.0")
}

val copyMathJax = tasks.register<Copy>("copyMathJax") {
    from(rootProject.file("lecture-notes/vendor/mathjax"))
    into(layout.buildDirectory.dir("generated/notes-vendor/notes/vendor/mathjax"))
}

android.sourceSets.named("main") {
    assets.srcDir(layout.buildDirectory.dir("generated/notes-vendor"))
}

tasks.matching { it.name.endsWith("Assets") }.configureEach {
    dependsOn(copyMathJax)
}
