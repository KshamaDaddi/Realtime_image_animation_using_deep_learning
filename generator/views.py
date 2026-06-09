from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import base64
import json
from ml.style_pipeline import generate_anime_image
from ml.gif_creator import create_animated_gif

# --- Our App's Data ---
# This is the list of styles from your image.
# We'll use placeholder paths for the images you will add.
# You should create a 'static/images' folder for these.
STYLE_DATA = [
    { 'id': '90s_anime', 'name': '90s anime', 'img_path': '/static/images/90s_anime.jpg', 'prompt': 'Transform this photo into the style of 90s anime, with its distinct color palette, line art, and film grain.'},
    { 'id': 'aesthetic_anime', 'name': 'Aesthetic anime', 'img_path': '/static/images/aesthetic_anime.jpg', 'prompt': 'Transform this photo into a modern, aesthetic anime style with soft colors.'},
    { 'id': 'ghibli_anime', 'name': 'Ghibli anime', 'img_path': '/static/images/ghibli_anime.jpg', 'prompt': 'Convert this image into the whimsical, painted style of a Studio Ghibli film.'},
    { 'id': 'fantasy_anime', 'name': 'Fantasy anime', 'img_path': '/static/images/fantasy_anime.jpg', 'prompt': 'Reimagine this photo as a fantasy anime character, with elements of magic or armor.'},
    { 'id': 'chibi_anime', 'name': 'Chibi anime', 'img_path': '/static/images/chibi_anime.jpg', 'prompt': 'Redraw this person as a cute, "chibi" anime character with large eyes and a small body.'},
    { 'id': 'japanese_anime', 'name': 'Japanese anime', 'img_path': '/static/images/japanese_anime.jpg', 'prompt': 'Transform this photo into a contemporary Japanese anime style.'},
    { 'id': '3d_anime', 'name': '3D anime', 'img_path': '/static/images/3d_anime.jpg', 'prompt': 'Convert this photo into a 3D anime or video game character style.'},
    { 'id': 'manga_anime', 'name': 'Manga anime', 'img_path': '/static/images/m1.jpg', 'prompt': 'Transform this photo into a black and white manga panel style.'},
    { 'id': 'anime_sketch', 'name': 'Anime sketch', 'img_path': '/static/images/anime_sketch.jpg', 'prompt': 'Transform this photo into a black and white anime-style line art sketch.'},
    { 'id': 'cyberpunk_anime', 'name': 'Cyberpunk anime', 'img_path': '/static/images/cyberpunk_anime.jpg', 'prompt': 'Turn this photo into a high-tech, neon-lit cyberpunk character portrait.'},
    { 'id': 'anime_illustration', 'name': 'Anime illustration', 'img_path': '/static/images/anime_illustration.jpg', 'prompt': 'Convert this photo into a detailed, high-quality anime illustration.'},
    { 'id': 'cartoon_anime', 'name': 'Cartoon', 'img_path': '/static/images/cartoon_anime.jpg', 'prompt': 'Transform this photo into a western cartoon style, similar to modern animated shows.'},
]

# (Removed deprecated external API and demo mock generation; local pipeline handles everything.)

# --- Page Views ---

def home_view(request):
    """
    Displays the home page with all style options.
    The template will handle locking/unlocking based on user auth.
    """
    context = {
        'styles': STYLE_DATA
    }
    return render(request, 'home.html', context)

def signup_view(request):
    """
    Handles user registration.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home') # Redirect to home after signup
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    """
    Handles user login.
    """
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home') # Redirect to home after login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    """
    Handles user logout.
    """
    logout(request)
    return redirect('home') # Redirect to home after logout

@login_required # This is the "lock"! User must be logged in.
def generate_page_view(request, style_id):
    """
    The main feature page for uploading and generating an image.
    """
    # Find the selected style from our data
    selected_style = next((style for style in STYLE_DATA if style['id'] == style_id), None)

    # If the style_id is invalid, redirect to home
    if not selected_style:
        return redirect('home')

    context = {
        'style': selected_style,
        'generated_image_data': None, # Will hold the base64 string
        'error_message': None,
    }

    if request.method == 'POST':
        # Handle the image upload
        uploaded_image = request.FILES.get('user_image')

        if not uploaded_image:
            context['error_message'] = "Please upload an image."
            return render(request, 'generate.html', context)

        # Check image type
        if not uploaded_image.content_type in ['image/jpeg', 'image/png']:
            context['error_message'] = "Invalid file type. Please upload a JPEG or PNG."
            return render(request, 'generate.html', context)
        
        try:
            # Read raw bytes for local pipeline
            image_bytes = uploaded_image.read()

            # Generate locally using AnimeGAN-based pipeline
            generated_base64 = generate_anime_image(image_bytes, selected_style['id'])

            if generated_base64:
                context['generated_image_data'] = f"data:image/png;base64,{generated_base64}"
            else:
                context['error_message'] = "Sorry, image generation failed locally. Please try another image or style."
        except Exception as e:
            print(f"Error during local image generation: {str(e)}")
            context['error_message'] = "Sorry, image generation failed. Please try again."

    # This renders the page on GET request OR after the POST logic is done
    return render(request, 'generate.html', context)

@login_required
def create_gif_view(request):
    """
    Handle AJAX requests for GIF creation.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            image_data = data.get('image_data')
            animation_type = data.get('animation_type', 'face-move')
            speed = data.get('speed', 'medium')
            
            # Create animated GIF
            gif_data = create_animated_gif(image_data, animation_type, speed)
            
            response_data = {
                'success': True,
                'gif_data': gif_data,
                'message': 'GIF created successfully'
            }
            
            return JsonResponse(response_data)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})