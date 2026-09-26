# RoadSense-Mobile-Django

RoadSense-Mobile is a Django-based web application for smart road surface detection using machine learning.

The application allows users to register, log in, upload road images, and analyze road conditions such as normal roads, potholes, cracks, and rough road surfaces through an interactive dashboard.

---

## 🚀 Features

- User Registration
- User Login and Logout
- Django-based authentication flow
- Interactive dashboard
- Road image upload
- Road surface prediction
- Prediction confidence display
- Road condition details
- Responsive user interface
- Modern blue and green glassmorphism design
- Mobile-friendly layout

---

## 🛣️ Road Conditions

RoadSense-Mobile is designed to identify road surface conditions such as:

- ✅ Normal Road
- 🕳️ Pothole
- ⚠️ Crack
- 🚧 Rough Road

---

## 🧠 How It Works

The basic workflow of the application is:

```text
Upload Road Image
        ↓
Image Processing
        ↓
Machine Learning Analysis
        ↓
Road Condition Prediction
        ↓
Prediction Result
```

Users can upload a road image from their computer or mobile device. The system processes the image and displays the detected road condition.

---

## 💻 Technologies Used

### Backend

- Python
- Django

### Frontend

- HTML5
- CSS3
- Django Templates

### Database

- SQLite

### Machine Learning

- Image Processing
- Machine Learning / Deep Learning Model

### Tools

- Git
- GitHub
- VS Code

---

## 📁 Project Structure

```text
RoadSense-Mobile-Django/
│
├── manage.py
├── db.sqlite3
├── requirements.txt
├── README.md
│
├── roadsense_mobile/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── users/
│   ├── migrations/
│   ├── templates/
│   │   ├── home.html
│   │   ├── login.html
│   │   ├── register.html
│   │   └── dashboard.html
│   │
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── tests.py
│
├── media/
│   └── road_images/
│
└── static/
    ├── css/
    ├── js/
    └── images/
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/suryatejayadav8/RoadSense-Mobile-Django-.git
```

### 2. Open the Project Folder

```bash
cd RoadSense-Mobile-Django-
```

### 3. Create a Virtual Environment

Windows:

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

Git Bash:

```bash
source venv/Scripts/activate
```

Windows Command Prompt:

```bash
venv\Scripts\activate
```

PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not available:

```bash
pip install django
```

---

## 🗄️ Database Setup

Run Django migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## ▶️ Run the Project

Start the Django development server:

```bash
python manage.py runserver
```

Open the application in your browser:

```text
http://127.0.0.1:8000/
```

---

## 📄 Application Pages

### Home Page

Introduces the RoadSense-Mobile project and provides navigation to Login and Register pages.

```text
/
```

### Register Page

Allows a new user to create an account.

```text
/register/
```

### Login Page

Allows registered users to log in.

```text
/login/
```

### Dashboard

Provides user information, road image upload, and road surface prediction.

```text
/dashboard/
```

### Logout

Logs the current user out of the application.

```text
/logout/
```

---

## 📷 Road Image Prediction

The dashboard allows users to upload road images in common formats such as:

```text
JPG
JPEG
PNG
```

After uploading an image, the system analyzes the road surface and can display:

```text
Prediction Result
Confidence Percentage
Road Condition Details
```

---

## 🎨 User Interface

The application uses a modern responsive interface with:

- Animated blue and green gradient background
- Glassmorphism cards
- Responsive navigation
- Road condition cards
- Image preview
- Prediction result display
- Mobile-friendly design

---

## 🔒 User Information

Registered users can have information such as:

```text
User Name
Password
Mobile Number
Place
```

The dashboard displays the logged-in user's basic profile information.

---

## 🔄 Git Commands

To upload project updates to GitHub:

```bash
git add .
git commit -m "Update RoadSense Mobile Django project"
git push origin main
```

---

## 🌟 Future Improvements

Possible future enhancements include:

- Real-time road detection using smartphone camera
- GPS-based road location tracking
- Map integration
- Road damage reporting
- Admin dashboard
- Prediction history
- Improved deep learning model
- Real-time road condition monitoring
- Cloud deployment
- REST API integration
- Android/mobile application integration

---

## 🎯 Project Objective

The objective of RoadSense-Mobile is to provide a simple and intelligent system for detecting road surface conditions using uploaded road images and machine learning.

The project can support road monitoring and help identify damaged road surfaces such as potholes, cracks, and rough roads.

---

## 👨‍💻 Author

**Bommena Surya Teja**
