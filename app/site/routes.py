from flask import Blueprint, render_template

site = Blueprint('site', __name__, template_folder='site_templates')

# default page start
@site.route('/')
def home():
    return render_template('index.html')
# default page end

@site.route('/profile')
def profile():
    return render_template('profile.html')

@site.route('/ebooks')
def ebooks():
    return render_template('ebooks.html')