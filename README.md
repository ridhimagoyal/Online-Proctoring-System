# Online-Proctoring-System

An intelligent and user-friendly web application designed to ensure academic integrity during online exams by integrating real-time proctoring features such as face detection, head pose estimation, and behavior analysis.

---

## 🌐 Overview

**The Online Exam Proctor** is a Flask-based web application built to monitor and evaluate the behavior of candidates during online tests. It uses computer vision technologies to detect suspicious activities (e.g., looking away from the screen) and generates detailed violation logs along with trust and performance scores.

---

## 📸 Screenshots

### 🧪 Exam Interface

![WhatsApp Image 2025-05-26 at 23 48 55_ecaa9b3a](https://github.com/user-attachments/assets/dd8c29d5-c39c-4945-a847-d48a463260cf)

The user is greeted with an intuitive quiz start screen. Once started, the system begins monitoring and analyzing behavior in the background.

### 📊 Result Dashboard

![WhatsApp Image 2025-05-26 at 23 49 30_e27e9b3e](https://github.com/user-attachments/assets/3a2d10b6-5290-4ffa-be7d-2e07b6dadfde)

Post-exam, each candidate receives:
- **Exam Status**: Pass/Fail with reason (e.g., Cheating)
- **Trust Score**: Based on behavioral violations
- **Total Score**: Based on quiz performance
- **Violation Logs**: Timestamped incidents with duration and evidence (video link)

---

## 🔍 Key Features

- 🎥 **Real-time Face Detection** using `face_recognition`
- 📐 **Head Pose Estimation** via `MediaPipe` for attention tracking
- 🔗 **Violation Records** with time, duration, and evidence link
- 🧠 **Trust Score Calculation** to judge integrity
- ⏱️ **Quiz with Timer and Penalties** for incorrect answers
- 🧾 **Detailed Result Report** for each candidate

---

## 🛠️ Tech Stack

- **Frontend**: HTML, CSS, JavaScript (Vanilla or React optional)
- **Backend**: Python, Flask
- **Database**: MySQL
- **CV Libraries**: OpenCV, face_recognition, MediaPipe
- **Deployment**: Can be hosted on Heroku, Render, or local servers

---

## How to Run

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/online-exam-proctor.git
   cd online-exam-proctor
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Flask server:
   ```bash
   python app.py
   ```

4. Open `http://localhost:5000` in your browser.

---

## 📌 Future Enhancements

- Audio monitoring for verbal cues
- Browser activity tracking (tab switch, fullscreen exit)
- Admin dashboard for reviewing all candidate records
- Multi-language support

---

## 🧑‍💻 Author

**Ridhima Goyal**  
Second-year CSE (AI) student at IGDTUW  

**Arya Shekhar**  
Second-year ECE (AI) student at IGDTUW  

---

## 📃 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.




