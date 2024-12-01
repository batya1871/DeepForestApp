# **DeepForestApp**

---

## **Description**

`DeepForestApp` is a web application built with Django that utilizes a neural network to analyze images. The primary goal of the application is to detect and classify objects as "trees" within uploaded images. Users can upload an image, receive a processed result with identified trees marked, and view the total count of detected trees.

---

## **Main Components**

1. **`users` App**:
   - Responsible for authentication and user management.
   - Supports login, registration, password change, and password recovery.

2. **`deepForestNN` App**:
   - Core functionality for image analysis.
   - Processes images and displays the results.

---

## **Project Structure**

- **Media Files (`media`)**:
  - **`background`**: Contains background images (if applicable).
  - **`analyzing_images`**:
    - **`source_images`**: Stores uploaded source images.
    - **`result_images`**: Contains processed images with marked objects.

- **Static Files (`static/deepForestNN`)**:
  - **`css`**: Stylesheets for UI design.
  - **`img`**: Images for the interface (logos, icons, etc.).
  - **`js`**: Includes the JavaScript file `validation.js` for form validation and enhanced user experience.

---

## **Files and Their Purpose**

### **Templates in `deepForestNN` App**:
1. **`base.html`**:
   - The main template for all pages.
   - Includes navigation and static resource linking (Bootstrap, CSS, JS).

2. **`main.html`**:
   - The home page for uploading images.
   - Provides a form to select and upload files for processing.

3. **`result.html`**:
   - The results page.
   - Displays the source image, processed result, and the count of detected trees.

### **Templates in `users` App**:
1. **`login.html`**:
   - Login page with an authorization form.
   - Includes links for registration and password recovery.

2. **`password_reset_form.html`**, **`password_reset_email.html`**, **`password_reset_confirm.html`**, **`password_reset_complete.html`**:
   - Implements the password reset process.

3. **`password_change_form.html`**, **`password_change_done.html`**:
   - Forms for changing the current password.

### **JavaScript File `validation.js`**:
- Implements:
  - Form validation before submission.
  - Dynamic updates to text and styles of elements (`label`, `input`, `button`) based on user actions.
  - Error notifications (e.g., no file selected).

---

## **How to Run the Project**

1. Install dependencies:
   pip install -r requirements.txt
2. Apply migrations:
   python manage.py migrate
3. Run the development server:
   python manage.py runserver
4. Open in the browser:
   http://127.0.0.1:8000
## **Key Features**
- **Image Analysis:**
Upload images via the interface.
Display processing results with the number of detected trees.
- **User Management:**
Registration, login, and logout.
Password change and recovery.
Notes
All uploaded images are saved in the media/analyzing_images folder.
Processed images are saved in a format suitable for further analysis.


Developed by Escapist_1871











