# selfForker
A simple Django app that forks itself into another Github account

## Building Steps
- To use this project, you need to create a Github App under your github account or use the Client ID and Client secret from an existing one.
- Using this information, create a `.env` file on `selfForker` filling all the keys present on `selfForker/.env.example`.
- **Recommended:** You can create a *Deploy Ready* docker image by running `docker build . -t selfforker` on the current directory.
    - To run this image use `docker run -d -p 8000:8000 selfforker` after building the image
- You can also run the project on the current host (not suitable for production):
    - Run `cd selfForker` to get into the Django project.
    - Run `pip install -r requirements.txt`
    - Run `python manage.py runserver --insecure` (The insecure flag is added to enable serving of static files with `DEBUG=False`)
- Open your web browser and go to `http://localhost:8000` to start using the web app.