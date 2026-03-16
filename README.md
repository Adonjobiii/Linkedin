# How to Run the Website (Flask Edition)

The project has been updated to use **Flask**, a Python web framework. This allows for better organization of templates and assets.

## 1. Install Dependencies
First, ensure you have Flask installed:
```powershell
pip install flask
```

## 2. Running the Application
To run the website, execute the `app.py` script:
```powershell
python app.py
```
- The server will start on `http://127.0.0.1:5000`.
- Open your browser and navigate to that address.

## 3. Project Structure
- `app.py`: The main Flask entry point.
- `templates/`: Contains HTML files (e.g., `index.html`).
- `static/`: Contains CSS, JS, and images.
  - `static/css/`: Stylesheets.
  - `static/js/`: JavaScript files.
  - `static/assets/`: Images and other assets.

---
*Note: Using `app.py` is now the preferred way to run this project. Direct file opening of `index.html` will no longer work correctly for assets because pathing now depends on the Flask static folder.*

---
*Note: Using a local server (Methods 2 & 3) is better than direct opening, as it avoids issues with browser security policies (CORS) when you start adding more features or external scripts.*
