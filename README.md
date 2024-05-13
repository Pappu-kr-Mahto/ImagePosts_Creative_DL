# ImagePosts_Creative_DL
1. This project like an Instagram but in very simple way.
2. Any user can register themselves and then post any number of images they want.
3. They can also use the functionality of follow and unfollow any other users.
4. They can only see the image post of those users whom they followed.
5. They can also of like and unlike the image post of self of other users.


*************************************** IMPORTANT **************************************

This backend project is hosted on Rendor.com( https://imageposts-creative.onrender.com/ )

I have integrated the Swagger API (drf_spectacular) , so you can directly test all the API's.


    ---------------Steps to Run this Django App(for Windows)---------------

1. Download this git repository.
2. Unzip the repository  where you want to keep this project.
3. Go insite the parent folder "ImagePosts_Creative_DL-main" using command prompt/any other terminal.
4. Here we have to create a new environment for this django app.
5. Run the command "python -m venv django_env" or "virtualenv django_env" -- Here django_env is the name of environment.
6. Now run "django_env/Scripts/activate" -- This command will activate your django environment.
7. Go to "ImagePosts_Creative_DL-main > Core>" 
8. Run "pip install -r requirements.txt" -- This will install all the required packages mentioned
     in the requirements.txt file.
9. Run "python manage.py makemigrations" and then  "python manage.py migrate"
10. Now run "python manage.py runserver"

