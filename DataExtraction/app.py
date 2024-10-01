import os
import shutil
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('index.html')


if __name__ == '__main__':
    # Run the app normally
    app.run(debug=True)

    # For freezing, render template and save to static HTML file
    with app.app_context():
        # Render the 'index.html' template
        rendered = render_template('index.html')

        # Define the output directory and ensure it exists
        output_path = os.path.join('build', 'index.html')
        os.makedirs('build', exist_ok=True)

        # Save the rendered HTML file to the build folder
        with open(output_path, 'w') as f:
            f.write(rendered)

        # Copy the 'static' folder to the 'build/static' folder
        static_src = os.path.join('static')
        static_dst = os.path.join('build', 'static')

        # Ensure the static folder exists before copying
        if os.path.exists(static_src):
            shutil.copytree(static_src, static_dst, dirs_exist_ok=True)
            print(f"Static files copied to {static_dst}")
        else:
            print(f"No static folder found at {static_src}")
