# **Monostack 🚀**

## 📌 Overview
Monostack is a simple **CLI tool** that helps developers generate a **full-stack project structure** interactively or using default configurations. It supports multiple technologies for **backend, frontend-web, frontend-mobile, and frontend-desktop**, allowing quick setup of a scalable and modular application.

---

## 🏗 **Features**
✅ **Interactive selection of technologies** (Spring Boot, Next.js, React Native, Tauri, etc.)  
✅ **Default mode for instant setup**  
✅ **Automatic project folder structure generation**  
✅ **Modular and scalable architecture**  

---

## 🔥 **Installation & Usage**

### **Prerequisites**
Ensure you have **Python 3.x** installed.

### **Clone the repository**
```bash
git clone https://github.com/kooljo/monostack.git
cd monostack
```

### **Run the CLI tool**

#### 🔹 **Interactive Mode (Manual Selection)**
```bash
python setup_project.py
```
👉 You will be prompted to choose **backend, frontend-web, frontend-mobile, and frontend-desktop** technologies.

#### 🔹 **Non-Interactive Mode (Default Values)**
```bash
python setup_project.py --default
```
👉 Uses default technologies:
- **Backend**: Spring Boot
- **Frontend Web**: Next.js
- **Frontend Mobile**: React Native
- **Frontend Desktop**: Tauri

---

## 📂 **Generated Project Structure**
```
📦 sport-app
├── 📁 backend (Spring Boot)
│   ├── README.md
├── 📁 frontend-web (Next.js)
│   ├── README.md
├── 📁 frontend-mobile (React Native)
│   ├── README.md
├── 📁 frontend-desktop (Tauri)
│   ├── README.md
├── 📁 infra (Infrastructure)
│   ├── README.md
├── 📁 docs (Documentation)
│   ├── README.md
```

---

## 📌 Roadmap & Future Enhancements
- [ ] **Automatic generation of `docker-compose.yml` for local deployment**
- [ ] **Integration with Git for automatic repository setup**
- [ ] **Support for additional frontend/backend stacks**
- [ ] **Optional database setup (PostgreSQL, MySQL, MongoDB, etc.)**

---

## 💡 **Contribute & Contact**
This project is **open-source**, and contributions are welcome!  
👥 **Fork and PR** on **GitHub**  
📩 Contact: [kollojeannoe@gmail.com](mailto:kollojeannoe@gmail.com)