# **Monostack 🚀**

## 📌 Overview
Monostack is a **CLI tool** that helps developers generate a **full-stack project structure** interactively or using default configurations. It supports multiple technologies for **backend, frontend-web, frontend-mobile, and frontend-desktop**, allowing quick setup of a scalable and modular application. It also generates a **docker-compose.yml** file based on the selected technologies and provides database integration.

---

## 🏗 **Features**
✅ **Interactive selection of technologies** (Spring Boot, Next.js, React Native, Tauri, etc.)  
✅ **Automatic project folder structure generation**  
✅ **Custom `docker-compose.yml` generation**  
✅ **Automatic installation of selected frameworks**  
✅ **Database selection and integration**  
✅ **Pre-configured documentation (`docs/` and `README.md`)**  
✅ **Dependency checking before installation (React Native, Node.js, npm, etc.)**  

---

## 🏗 Supported Technologies
### **Backend**
- **Java**: Spring Boot, Quarkus, Micronaut, etc.
- **JavaScript**: NestJS, Express, Fastify, etc.
- **PHP**: Laravel, Symfony, CodeIgniter, etc.
- **Python**: Django, Flask, FastAPI, etc.
- **Go**: Gin, Echo, Fiber, etc.
- **Rust**: Actix, Axum, Rocket, etc.
- **Ruby**: Rails, Sinatra, Hanami, etc.
- **.NET**: ASP.NET Core, Blazor, etc.

### **Frontend Web**
- **JavaScript**: React, Next.js, Vue, Angular, Svelte, etc.
- **Python**: Dash, Streamlit, PyScript
- **Ruby**: Rails Stimulus, Bridgetown
- **PHP**: Laravel Livewire, Symfony UX
- **Dart**: Flutter Web
- **.NET**: Blazor, ASP.NET MVC

### **Frontend Mobile**
- **JavaScript**: React Native, Expo, Ionic, Capacitor
- **Dart**: Flutter
- **Kotlin**: Jetpack Compose, KMM
- **Swift**: SwiftUI, UIKit
- **.NET**: MAUI
- **Python**: Kivy, BeeWare

### **Frontend Desktop**
- **JavaScript**: Electron, Tauri, Neutralino.js
- **Dart**: Flutter Desktop
- **Kotlin**: Compose Desktop
- **Swift**: SwiftUI, AppKit
- **.NET**: WinUI, WPF, MAUI
- **Python**: PyQt, Kivy, Tkinter, BeeWare

### **Databases**
- **PostgreSQL**
- **MySQL**
- **MongoDB**
- **Redis**
- **SQLite**
- **Cassandra**
- **Elasticsearch**
- **Neo4j**

---

## 🔥 **Installation & Usage**
### **Prerequisites**
Ensure you have the following installed:
- **Python 3+**
- **Git**
- **Docker & Docker Compose**
- **Gum** (for CLI interactive selection)

### **Clone the repository**
```bash
git clone https://github.com/kooljo/monostack
cd monostack
```

### **Run the CLI tool**
#### 🔹 **Interactive Mode (Manual Selection)**
```bash
python setup.py
```
👉 You will be prompted to choose **backend, frontend-web, frontend-mobile, frontend-desktop**, and **database** technologies.

#### 🔹 **Run Services with Docker Compose**
```bash
cd ../mono-app/infra
docker-compose up --build -d
```

---

## 📂 **Generated Project Structure**
```
📦 mono-app
├── 📁 backend          # Selected backend framework (e.g., Spring Boot, Express, Laravel...)
├── 📁 frontend-web     # Selected web framework (e.g., React, Angular, Vue...)
├── 📁 frontend-mobile  # Selected mobile framework (e.g., React Native, Flutter...)
├── 📁 frontend-desktop # Selected desktop framework (e.g., Electron, Tauri...)
├── 📁 infra            # Infrastructure files (Docker, Kubernetes...)
│   ├── docker-compose.yml
│   └── ...
├── 📁 docs             # Project documentation
└── 📜 README.md
```

---

## 📌 Roadmap & Future Enhancements
- [ ] **Enhanced database management** (automated migrations, backups)
- [ ] **Integration with Git for automatic repository setup**
- [ ] **Additional frontend/backend stacks**
- [ ] **Enhanced CLI options for advanced configurations**
- [ ] **CI/CD pipeline integration**

---

## 💡 **Contribute & Contact**
This project is **open-source**, and contributions are welcome!  
👥 **Fork and PR** on **GitHub**  
📩 Contact: [kollojeannoe@gmail.com](mailto:kollojeannoe@gmail.com)
