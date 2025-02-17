import os
from flask import render_template, request
from werkzeug.utils import secure_filename
from app import app
from app.scanner.scan import DocScanner
from app.ocr import OCR

# Allowed file extensions
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

def allowed_file(filename):
    """Checks if file type is allowed"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part"
        file = request.files["file"]
        if file.filename == "":
            return "No selected file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            # Process image with scanner
            processed_filepath = os.path.join(app.config["PROCESSED_FOLDER"], filename)
            scanner = DocScanner(interactive=True)  # Enable interactive mode
            scanner.scan(filepath, processed_filepath)

            # Instantiate OCR class and extract text
            ocr = OCR()  # Create an instance of OCR
            extracted_text = ocr.extract_text(processed_filepath)  # Use the instance to call extract_text
            print("Extracted text:", extracted_text)
            # Render the result on the same page
            return render_template("index.html", text=extracted_text, image_url=processed_filepath)

    # Render the template with no results if it's a GET request or no file uploaded
    return render_template("index.html", text=None, image_url=None)
