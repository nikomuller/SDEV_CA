#How To Run

git clone https://github.com/nikomuller/Game-Hosting-Website.git
cd your-repository-folder

python -m venv pyvenv
pyvenv\Scripts\activate

cd scillium

pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate

python manage.py runserver


# Notes

- Changed to this repo as I have ownership and have made it public.

- Name: Scillium Game Hosting
- Domain: https://scillium.com 
It would have been hosted at 'scillium.com' but you need a premium account for that


## Description
Scillium Game Hosting is a game hosting company that provides high quality game servers billed by the second. 
We offer a wide variety of games and game modes. We also offer a wide variety of customizations for your server.


## 3rd Party Services
- Payment Processor: Stripe
- Hosting Provider: TBD
- Design Tool: Figma
- Django Forms: Crispy


## Structure


## Pages
Figma url: https://www.figma.com/file/9kwOEjzanYXhQiQvtpzWpb/SDEVCA?t=0ES3SazBCt2AhT0C-6
This figma file realy set the whole style of the project in just one page, from the color scheme to the font, 
it was a great tool to use to help us create the website.

- Splash Page (Landing Page)
- Rent a Server
- Contact Us
- About Us
- Checkout
- Control Panel
- Terms of Service
- Login / Register


## Admin login
- Username: admin
- Password: A3i04*#UMkRj 


## PIP Packages
- django
- django-colorfield
- stripe
- pillow
- django-crispy-forms
- crispy-bootstrap5
- djangorestframework


## Who did what?

 - Nikolas Muller: I created the product, search, cart and order apps, I added stripe payment functionality and I also created some of the templates involved, I also helped my team mate finish some of his apps quicker as did he, i updated some of the css to help it match the style of the web page we were creating, i was updating the git repo aswell as this readme file and settings.py file meanwhile doing my work to make everything link together and function properly together.


 - Team Mate: I was responsible for the initial set up of the project, I mainly focues on QOL features and just generaly making the product feature rich. I designed the whole look and feel of the site, I did not create much of the apps, but I did aid Nikolas in fixing bugs and refactoring code.

We both feel that we both did a good job and we both worked well together, we both helped each other out when we got stuck and we both worked well together to get the project done on time.
