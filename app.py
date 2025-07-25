from flask import Flask, request, render_template, send_from_directory
from PIL import Image, ImageDraw, ImageFont
import os
import uuid

app = Flask(__name__)
OUTPUT_DIR = "static"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    image_file = None
    error = None

    if request.method == "POST":
        user_input = request.form.get("text", "").strip()

        if not user_input:
            error = "Input cannot be empty."
        else:
            try:
                # Create a new image with Pillow
                img = Image.new("RGB", (600, 200), color=(173, 216, 230))  # lightblue background
                draw = ImageDraw.Draw(img)

                # Load a font
                try:
                    font = ImageFont.truetype("arial.ttf", 30)  # Replace with a path to a TTF on your system if needed
                except:
                    font = ImageFont.load_default()

                draw.text((20, 80), user_input, fill="black", font=font)

                # Save image with unique filename
                filename = f"{uuid.uuid4().hex}.png"
                image_path = os.path.join(OUTPUT_DIR, filename)
                img.save(image_path)

                image_file = filename
            except Exception as e:
                error = f"Error generating image: {str(e)}"

    return render_template("index.html", image_file=image_file, error=error)


@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory(OUTPUT_DIR, filename)


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="127.0.0.1", port=8000)
