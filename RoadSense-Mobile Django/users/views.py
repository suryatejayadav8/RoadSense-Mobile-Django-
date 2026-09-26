from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password

from .models import User

import base64
import cv2
import numpy as np


# ============================================================
# HOME PAGE
# ============================================================

def home(request):
    return render(
        request,
        'users/home.html'
    )


# ============================================================
# REGISTER PAGE
# ============================================================

def register(request):

    if request.method == 'POST':

        user_name = request.POST.get('user_name', '').strip()
        password = request.POST.get('password', '')
        mobile_number = request.POST.get('mobile_number', '').strip()
        place = request.POST.get('place', '').strip()

        # Check required fields
        if not user_name or not password:

            return render(
                request,
                'users/register.html',
                {
                    'error': 'Username and password are required.'
                }
            )

        # Check if username already exists
        if User.objects.filter(
            user_name=user_name
        ).exists():

            return render(
                request,
                'users/register.html',
                {
                    'error':
                    'Username already exists. Please choose another username.'
                }
            )

        # Create user
        user = User(
            user_name=user_name,
            password=make_password(password),
            mobile_number=mobile_number,
            place=place
        )

        user.save()

        return render(
            request,
            'users/login.html',
            {
                'success':
                'Registration successful. Please login.'
            }
        )

    return render(
        request,
        'users/register.html'
    )


# ============================================================
# LOGIN PAGE
# ============================================================

def login_view(request):

    if request.method == 'POST':

        user_name = request.POST.get('user_name', '').strip()
        password = request.POST.get('password', '')

        user = User.objects.filter(
            user_name=user_name
        ).first()

        # User not found
        if user is None:

            return render(
                request,
                'users/login.html',
                {
                    'error': 'User does not exist.'
                }
            )

        # Check password
        if check_password(
            password,
            user.password
        ):

            request.session['user_id'] = user.id
            request.session['user_name'] = user.user_name

            return redirect(
                'dashboard'
            )

        return render(
            request,
            'users/login.html',
            {
                'error': 'Invalid password.'
            }
        )

    return render(
        request,
        'users/login.html'
    )


# ============================================================
# ROAD IMAGE ANALYSIS
# ============================================================

def analyze_road_image(image_bytes):

    try:

        # Convert image bytes into NumPy array
        np_array = np.frombuffer(
            image_bytes,
            dtype=np.uint8
        )

        # Decode uploaded image
        image = cv2.imdecode(
            np_array,
            cv2.IMREAD_COLOR
        )

        if image is None:

            return {
                'result': 'Invalid Image',
                'confidence': 0,
                'details':
                    'The uploaded image could not be processed.'
            }

        # Resize image
        image = cv2.resize(
            image,
            (640, 480)
        )

        # Convert to grayscale
        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(
            gray,
            (7, 7),
            0
        )

        # Edge detection
        edges = cv2.Canny(
            blurred,
            50,
            150
        )

        # Morphological closing
        kernel = np.ones(
            (5, 5),
            dtype=np.uint8
        )

        closed = cv2.morphologyEx(
            edges,
            cv2.MORPH_CLOSE,
            kernel
        )

        # Find contours
        contours, _ = cv2.findContours(
            closed,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        large_contours = []
        medium_contours = []

        for contour in contours:

            area = cv2.contourArea(
                contour
            )

            if area > 2500:

                large_contours.append(
                    contour
                )

            elif area > 700:

                medium_contours.append(
                    contour
                )

        # Calculate edge density
        edge_pixels = np.count_nonzero(
            edges
        )

        total_pixels = edges.size

        if total_pixels == 0:
            edge_density = 0
        else:
            edge_density = (
                edge_pixels / total_pixels
            )

        # Calculate contrast
        contrast = float(
            np.std(gray)
        )

        # ====================================================
        # BASIC ROAD CONDITION CLASSIFICATION
        #
        # NOTE:
        # This is OpenCV-based image processing.
        # It is NOT a trained ML model yet.
        # ====================================================

        if len(large_contours) >= 3:

            result = (
                'Pothole / Severe Road Damage Detected'
            )

            confidence = min(
                95,
                70 + len(large_contours) * 4
            )

            details = (
                'Large irregular damaged regions '
                'were detected in the road image.'
            )

        elif len(large_contours) >= 1:

            result = (
                'Possible Pothole Detected'
            )

            confidence = min(
                90,
                65 + len(large_contours) * 8
            )

            details = (
                'A significant irregular road-surface '
                'region was detected.'
            )

        elif (
            len(medium_contours) >= 5
            or edge_density > 0.12
        ):

            result = (
                'Cracked / Rough Road Detected'
            )

            calculated_confidence = int(
                60 + edge_density * 150
            )

            confidence = min(
                88,
                calculated_confidence
            )

            details = (
                'The road surface contains multiple '
                'edges and irregular patterns.'
            )

        elif contrast > 70:

            result = (
                'Uneven Road Surface'
            )

            confidence = 68

            details = (
                'The image contains noticeable '
                'road-surface variation.'
            )

        else:

            result = (
                'Normal / Smooth Road'
            )

            confidence = 80

            details = (
                'No major pothole or road-damage '
                'pattern was detected.'
            )

        return {
            'result': result,
            'confidence': confidence,
            'details': details
        }

    except Exception as error:

        return {
            'result': 'Image Analysis Failed',
            'confidence': 0,
            'details': str(error)
        }


# ============================================================
# DASHBOARD PAGE
# ============================================================

def dashboard(request):

    # Check login session
    if 'user_id' not in request.session:

        return redirect(
            'login'
        )

    # Get logged-in user
    user = User.objects.filter(
        id=request.session['user_id']
    ).first()

    # If user record no longer exists
    if user is None:

        request.session.flush()

        return redirect(
            'login'
        )

    result = None
    confidence = None
    details = None
    uploaded_image = None
    error = None

    # ========================================================
    # ROAD IMAGE UPLOAD
    # ========================================================

    if request.method == 'POST':

        road_image = request.FILES.get(
            'road_image'
        )

        # No image selected
        if road_image is None:

            error = (
                'Please select a road image '
                'before starting prediction.'
            )

        # Check image type
        elif not road_image.content_type.startswith(
            'image/'
        ):

            error = (
                'Please upload a valid image file.'
            )

        # Maximum size 5 MB
        elif road_image.size > 5 * 1024 * 1024:

            error = (
                'Image is too large. '
                'Please upload an image smaller than 5 MB.'
            )

        else:

            # Read uploaded image
            image_bytes = road_image.read()

            # Convert uploaded image to Base64
            # This allows displaying it directly in HTML
            # without creating a media folder.
            encoded_image = base64.b64encode(
                image_bytes
            ).decode(
                'utf-8'
            )

            uploaded_image = (
                f'data:{road_image.content_type};'
                f'base64,{encoded_image}'
            )

            # Analyze the road image
            prediction = analyze_road_image(
                image_bytes
            )

            result = prediction.get(
                'result'
            )

            confidence = prediction.get(
                'confidence'
            )

            details = prediction.get(
                'details'
            )

    return render(
        request,
        'users/dashboard.html',
        {
            'user': user,
            'result': result,
            'confidence': confidence,
            'details': details,
            'uploaded_image': uploaded_image,
            'error': error
        }
    )


# ============================================================
# LOGOUT
# ============================================================

def logout_view(request):

    request.session.flush()

    return redirect(
        'home'
    )