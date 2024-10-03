import os
import shutil
import sys
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def main():
    # Fetch the application version from environment variable
    app_version = os.getenv('APP_VERSION', '1.0.0')  # Default to 1.0.0 if not set
    return render_template('index.html', app_version=app_version, cache=False)


def clean_and_build_static_site():
    """Function to generate static HTML and copy static files to the build folder."""
    with app.app_context():
        # Fetch the application version
        app_version = os.getenv('APP_VERSION', '1.0.0')

        # Define the build directory
        build_dir = 'build'

        # Remove the build directory if it already exists
        if os.path.exists(build_dir):
            shutil.rmtree(build_dir)
            print(f"Removed existing build directory: {build_dir}")

        # Recreate the build directory
        os.makedirs(build_dir, exist_ok=True)

        # Tell Flask to use static paths directly
        app.config['FREEZE'] = True

        # Render the 'index.html' template with the app version
        rendered = render_template('index.html', app_version=app_version)

        # Define the output path for the HTML file
        output_path = os.path.join(build_dir, 'index.html')

        # Save the rendered HTML file to the build folder
        with open(output_path, 'w') as f:
            f.write(rendered)

        print(f"Rendered HTML saved to {output_path}")

        # Copy the 'static' folder to the 'build/static' folder
        static_src = os.path.join('static')
        static_dst = os.path.join(build_dir, 'static')

        # Ensure the static folder exists before copying
        if os.path.exists(static_src):
            shutil.copytree(static_src, static_dst, dirs_exist_ok=True)
            print(f"Static files copied to {static_dst}")
        else:
            print(f"No static folder found at {static_src}")


if __name__ == '__main__':
    # Use a command-line argument or environment variable to control the mode
    if len(sys.argv) > 1 and sys.argv[1] == 'freeze':
        clean_and_build_static_site()
    else:
        app.run(debug=True)
