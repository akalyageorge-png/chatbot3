import streamlit as st
import google.generativeai as genai
import os
import datetime
import ssl
import pandas as pd
from datetime import datetime, timedelta
import json
import http.client
import urllib.parse
import time
import random

# --- FIX for [SSL: CERTIFICATE_VERIFY_FAILED] ---
try:
    # Check if the attribute exists before using it
    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context
except AttributeError:
    # Handle case where the SSL module doesn't have this attribute
    pass
# --- END OF SSL FIX ---

# --- Custom CSS for styling ---
def set_custom_style():
    st.markdown("""
        <style>
        /* Main background and layout */
.stApp {
    background: linear-gradient(rgba(0, 0, 0, 0), rgba(0, 0, 0, 0)), url('https://www.shutterstock.com/image-photo/ai-chatbot-assisting-doctor-health-600nw-2605462455.jpg');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    color: white;
}

/* Ensure no white background */
.main .block-container {
    background-color: transparent;
}

/* Sidebar styling */
.css-1d391kg {
    background: linear-gradient(135deg, #2a3f5f, #1a2332);
    color: white;
}

/* Card styling */
div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column;"] > div > div > div {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 15px;
    backdrop-filter: blur(5px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.stButton > button {
    color: white;
    border: 1px solid white;
    border-radius: 8px;
    padding: 10px 16px;
    font-weight: bold;
    transition: all 0.3s ease;
    background: transparent;
}
.login-btn {
    color: black;
    padding: 10px 20px;
    border: 1px solid black;
    border-radius: 4px;
    cursor: pointer;
    background: transparent;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
}

/* Input field styling */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > select,
.stDateInput > div > div > input,
.stTimeInput > div > div > input {
    background-color: rgba(255, 255, 255, 0.9);
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.3);
}

/* Header styling */
.css-1vq4p4l {
    background: linear-gradient(90deg, #4e73df, #224abe);
    color: white;
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 20px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Expander styling */
.streamlit-expanderHeader {
    background-color: rgba(78, 115, 223, 0.3);
    border-radius: 8px;
    color: white;
}
div[data-testid="stFormSubmitButton"] > button {
    background-color: #4e73df; /* A solid blue background */
    color: white;
    border: 1px solid #4e73df;
    border-radius: 8px;
    padding: 10px 16px;
    font-weight: bold;
    transition: all 0.3s ease;
}
                div[data-testid="stFormSubmitButton"] > button:hover {
    background-color: blue; /* A darker blue on hover */
    transform: translateY(-2px);
    box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
}
/* Metric card styling */
div[data-testid="metric-container"] {
    background-color: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(5px);
    text-align: center;
}

/* Table styling */
.dataframe {
    background-color: rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    overflow: hidden;
}

/* Chat message styling */
.stChatMessage {
    background-color: rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    padding: 15px;
    margin-bottom: 10px;
    backdrop-filter: blur(5px);
}

/* Form styling - MADE TRANSPARENT */
.stForm {
    background-color: transparent;
    border-radius: 10px;
    padding: 20px;
    backdrop-filter: blur(5px);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

/* Success, error, warning styling */
.stAlert {
    border-radius: 10px;
    margin-bottom: 15px;
}

/* Status styling */
.stStatus {
    background-color: rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    padding: 15px;
    backdrop-filter: blur(5px);
}

/* Tabs styling */
.stTabs [data-baseweb="tab-list"] {
    background-color: rgba(255, 255, 255, 0.1);
    border-radius: 10px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px 8px 0 0;
    padding: 10px 20px;
    font-weight: bold;
}

/* Slider styling */
.stSlider [data-baseweb="slider"] {
    background-color: rgba(255, 255, 255, 0.1);
}

/* Health campaign buttons */
.health-campaign-btn {
    display: flex;
    justify-content: center;
    margin-bottom: 10px;
}

/* Login form styling */
.login-form {
    background: linear-gradient(135deg, rgba(78, 115, 223, 0.9), rgba(34, 74, 190, 0.9));
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

/* Custom header for different sections */
.section-header {
    background: linear-gradient(90deg, #4e73df, #224abe);
    color: white;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 20px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    text-align: center;
}

/* Rate limit warning styling */
.rate-limit-warning {
    background-color: rgba(255, 165, 0, 0.2);
    border: 1px solid rgba(255, 165, 0, 0.5);
    border-radius: 10px;
    padding: 15px;
    margin-bottom: 15px;
}
    </style>
    """, unsafe_allow_html=True)

# --- Rate Limiting Helper ---
def check_rate_limit():
    """Check if we should wait due to rate limiting"""
    if 'last_api_call' not in st.session_state:
        st.session_state.last_api_call = 0
        return False, 0
    
    # Free tier limit: 2 requests per minute
    # We'll be conservative and wait 35 seconds between requests
    current_time = time.time()
    time_since_last_call = current_time - st.session_state.last_api_call
    
    if time_since_last_call < 35:
        return True, 35 - time_since_last_call
    
    return False, 0

def update_last_api_call():
    """Update the timestamp of the last API call"""
    st.session_state.last_api_call = time.time()

def handle_rate_limit_error(error):
    """Handle rate limit errors with retry logic"""
    if "429" in str(error) or "quota" in str(error).lower():
        # Extract retry delay if available
        try:
            error_str = str(error)
            if "retry_delay" in error_str:
                # Try to extract the retry delay from the error message
                import re
                match = re.search(r'retry_delay \{ seconds: (\d+)', error_str)
                if match:
                    retry_seconds = int(match.group(1))
                    return True, retry_seconds
        except:
            pass
        
        # Default to 35 seconds if we can't extract the retry delay
        return True, 35
    
    return False, 0

# --- Translation Functions ---
def detect_language(text):
    """Simple language detection based on common words"""
    common_words = {
        'en': ['the', 'is', 'and', 'to', 'a', 'in', 'that', 'have', 'i', 'you', 'what', 'how'],
        'es': ['el', 'es', 'y', 'a', 'en', 'que', 'tenga', 'yo', 'tú', 'qué', 'cómo'],
        'fr': ['le', 'est', 'et', 'à', 'en', 'que', 'a', 'je', 'tu', 'quoi', 'comment'],
        'de': ['der', 'ist', 'und', 'zu', 'den', 'dass', 'haben', 'ich', 'du', 'was', 'wie'],
        'hi': ['है', 'और', 'को', 'में', 'कि', 'जो', 'हैं', 'मैं', 'तुम', 'क्या', 'कैसे'],
        'zh': ['的', '是', '和', '在', '有', '不', '这', '我', '你', '什么', '如何'],
        'ar': ['في', 'من', 'إلى', 'هذا', 'هذه', 'كان', 'كانت', 'أنا', 'أنت', 'ماذا', 'كيف'],
        'pt': ['o', 'é', 'e', 'a', 'em', 'que', 'ter', 'eu', 'você', 'o que', 'como'],
        'ru': ['в', 'и', 'на', 'с', 'что', 'это', 'быть', 'я', 'ты', 'что', 'как'],
        'ja': ['の', 'は', 'を', 'に', 'と', 'が', 'です', '私', 'あなた', '何', 'どのように'],
        'bn': ['হয়', ' এবং', 'কে', 'মধ্যে', 'যে', 'আছে', 'আমি', 'তুমি', 'কি', 'কিভাবে'],
        'ta': ['உள்ள', 'மற்றும்', 'க்கு', 'இல்', 'அது', 'நான்', 'நீ', 'என்ன', 'எப்படி'],
        'te': ['ఉంది', 'మరియు', 'కి', 'లో', 'అది', 'నేను', 'నువ్వు', 'ఏమి', 'ఎలా'],
        'mr': ['आहे', 'आणि', 'ला', 'मध्ये', 'ते', 'मी', 'तू', 'काय', 'कसे'],
        'gu': ['છે', 'અને', 'ને', 'માં', 'તે', 'હું', 'તું', 'શું', 'કેવી રીતે'],
        'kn': ['ಇದೆ', 'ಮತ್ತು', 'ಗೆ', 'ನಲ್ಲಿ', 'ಅದು', 'ನಾನು', 'ನೀನು', 'ಏನು', 'ಹೇಗೆ'],
        'ml': ['ആണ്', 'ഒപ്പം', 'ന്', 'ഇൽ', 'അത്', 'ഞാൻ', 'നീ', 'എന്ത്', 'എങ്ങനെ'],
        'pa': ['ਹੈ', 'ਅਤੇ', 'ਨੂੰ', 'ਵਿੱਚ', 'ਉਹ', 'ਮੈਂ', 'ਤੂੰ', 'ਕੀ', 'ਕਿਵੇਂ']
    }
    
    text_lower = text.lower()
    language_scores = {}
    
    for lang, words in common_words.items():
        score = sum(1 for word in words if word in text_lower)
        if score > 0:
            language_scores[lang] = score
    
    if language_scores:
        return max(language_scores, key=language_scores.get)
    else:
        return 'en'  # Default to English if no match

# ------------------- NEW AND IMPROVED TRANSLATE FUNCTION -------------------
def translate_text(text, target_lang):
    """
    Translate text using MyMemory API.
    Returns the translated text on success, or None on failure.
    """
    if target_lang == 'en':
        return text  # No translation needed
    
    try:
        # Using MyMemory API for translation
        params = urllib.parse.urlencode({'q': text, 'langpair': f'en|{target_lang}'})
        url = f"/get?{params}"
        
        conn = http.client.HTTPSConnection("api.mymemory.translated.net")
        conn.request("GET", url)
        
        res = conn.getresponse()
        data = res.read().decode("utf-8")
        conn.close()
        
        result = json.loads(data)
        
        # Check for a successful response and that the translation is not empty
        if result.get("responseStatus") == 200 and result["responseData"]["translatedText"]:
            return result["responseData"]["translatedText"]
        else:
            # The API returned a non-200 status or an empty translation, so it failed.
            print(f"Translation API failed with status: {result.get('responseStatus')}")
            return None
            
    except Exception as e:
        # Any other error (network, etc.) also means failure.
        print(f"An exception occurred during translation: {e}")
        return None
# ------------------- END OF IMPROVED FUNCTION -------------------


def get_language_name(code):
    """Get language name from code"""
    languages = {
        'en': 'English',
        'es': 'Spanish',
        'fr': 'French',
        'de': 'German',
        'hi': 'Hindi',
        'zh': 'Chinese',
        'ar': 'Arabic',
        'pt': 'Portuguese',
        'ru': 'Russian',
        'ja': 'Japanese',
        'bn': 'Bengali',
        'ta': 'Tamil',
        'te': 'Telugu',
        'mr': 'Marathi',
        'gu': 'Gujarati',
        'kn': 'Kannada',
        'ml': 'Malayalam',
        'pa': 'Punjabi'
    }
    return languages.get(code, "Unknown")

# --- Configuration ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except (FileNotFoundError, KeyError):
    # It's better practice to avoid hardcoding keys directly in the script.
    # Using an environment variable is a good alternative for local development.
    api_key = os.environ.get("GOOGLE_API_KEY", "AIzaSyASQgsp2CU5SJSEj5pMxZLsfSlszHhvxdk") # Replace with your actual key if not using secrets
    if "YOUR_GOOGLE_API_KEY" in api_key:
        st.warning("Please add your Google API key to secrets.toml or set it as an environment variable.")

genai.configure(api_key=api_key)

# Generation configuration for the model
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# System instruction for the model
system_instruction = (
    "You are a helpful medical assistant. "
    "A user can ask you about medical issues. "
    "You should provide helpful and safe suggestions. "
    "For example: If user says 'I'm getting a headache', "
    "you should suggest some precautions and advise them to consult a doctor if the issue persists. "
    "Always prioritize user safety and recommend professional medical consultation for serious matters."
)

# --- Pre-defined Health Campaign Messages ---
HEALTH_MESSAGES = {
    "hygiene": {
        "title": "🧼 Basic Hygiene Tips",
        "content": "Washing your hands frequently with soap and water is one of the most effective ways to prevent the spread of germs. Always cover your mouth and nose when you cough or sneeze. Avoid touching your eyes, nose, and mouth to prevent germs from entering your body."
    },
    "vaccination": {
        "title": "💉 Why Vaccination is Important",
        "content": "Vaccines protect you and your community from serious diseases. They work by preparing your body's immune system to fight off infections. Getting vaccinated is a safe and effective way to keep your family healthy. Consult a healthcare provider to ensure your vaccinations are up to date."
    },
    "healthy_eating": {
        "title": "🍎 Healthy Eating Habits",
        "content": "A balanced diet is crucial for good health. Eat a variety of fruits, vegetables, and whole grains. Limit the intake of processed foods, sugar, and unhealthy fats. Drinking plenty of water throughout the day is also essential for staying hydrated and healthy."
    },
    "mental_health": {
        "title": "🧘‍♀️ Managing Stress and Mental Health",
        "content": "Your mental health is as important as your physical health. Practice relaxation techniques like deep breathing or meditation. Stay connected with loved ones and don't hesitate to seek professional help if you feel overwhelmed. Taking breaks and getting enough sleep are also vital."
    },
    "exercise": {
        "title": "🏃‍♂️ Benefits of Regular Exercise",
        "content": "Aim for at least 30 minutes of moderate physical activity most days of the week. Exercise strengthens your heart, improves circulation, helps manage weight, and boosts your mood. Even a brisk walk can make a big difference."
    },
    "sleep": {
        "title": "😴 The Importance of Quality Sleep",
        "content": "Adults generally need 7-9 hours of sleep per night. Good sleep improves brain function, mood, and overall health. Create a relaxing bedtime routine and try to go to bed and wake up at the same time every day, even on weekends."
    },
    "hydration": {
        "title": "💧 Staying Properly Hydrated",
        "content": "Drinking enough water is essential for your body to function correctly. It helps regulate body temperature, prevent infections, and keep organs functioning properly. Don't wait until you feel thirsty to drink water, as thirst is a sign you are already slightly dehydrated."
    },
    "heart_attack": {
        "title": "❤️ Recognizing Heart Attack Symptoms",
        "content": "Common signs of a heart attack include chest pain or discomfort, shortness of breath, pain in the neck, back, or arms, and feeling lightheaded or nauseous. If you suspect someone is having a heart attack, call emergency services immediately."
    },
    "stroke": {
        "title": "🧠 Recognizing Stroke Symptoms (F.A.S.T.)",
        "content": "Use the F.A.S.T. method to remember the signs of a stroke. F - Face drooping: Does one side of the face droop? A - Arm weakness: Is one arm weak or numb? S - Speech difficulty: Is speech slurred? T - Time to call emergency services immediately if you see any of these signs."
    },
    "fever": {
        "title": "🌡️ How to Manage a Fever",
        "content": "A fever is often a sign your body is fighting an infection. Get plenty of rest and drink lots of fluids like water or broth to prevent dehydration. Over-the-counter medications like acetaminophen or ibuprofen can help reduce fever. If the fever is very high or persists for more than a few days, consult a doctor."
    },
    "first_aid_burns": {
        "title": "🔥 First Aid for Minor Burns",
        "content": "For minor burns, immediately cool the area by running cool (not cold) water over it for 10-20 minutes. Cover the burn with a sterile, non-adhesive bandage. Do not use ice or apply ointments. For severe burns, seek immediate medical attention."
    }
}

# --- HOSPITAL DATA FOR SIMULATION ---
HOSPITAL_DATA = {
    "departments": {
        "Cardiology": "2nd Floor, Wing A",
        "Orthopedics": "1st Floor, Wing B",
        "Neurology": "3rd Floor, Wing A",
        "Pediatrics": "1st Floor, Wing C",
        "General Medicine": "Ground Floor, Main Building"
    },
    "doctors": {
        "Cardiology": [
            {"name": "Dr. Emily Carter", "schedule": "Mon-Wed, 9:00 AM - 1:00 PM"},
            {"name": "Dr. Ben Adams", "schedule": "Thu-Fri, 1:00 PM - 5:00 PM"}
        ],
        "Orthopedics": [
            {"name": "Dr. Sarah Jenkins", "schedule": "Mon, Wed, Fri, 10:00 AM - 4:00 PM"}
        ],
        "Neurology": [
            {"name": "Dr. David Chen", "schedule": "Tue-Thu, 8:00 AM - 12:00 PM"},
            {"name": "Dr. Maria Rodriguez", "schedule": "Mon-Fri, 2:00 PM - 6:00 PM"}
        ],
        "Pediatrics": [
            {"name": "Dr. Lisa Wong", "schedule": "Mon-Fri, 9:00 AM - 5:00 PM"}
        ],
        "General Medicine": [
            {"name": "Dr. Robert Miller", "schedule": "Mon-Fri, 8:00 AM - 1:00 PM"},
            {"name": "Dr. Karen Hall", "schedule": "Mon-Fri, 1:00 PM - 6:00 PM"}
        ]
    },
    "faqs": {
        "What are the hospital's visiting hours?": "General visiting hours are from 11:00 AM to 8:00 PM daily.",
        "Where is the pharmacy located?": "The outpatient pharmacy is on the Ground Floor, near the main entrance.",
        "Do I need to bring my medical records?": "Yes, please bring any relevant past medical records and a list of current medications.",
        "Is parking available?": "Yes, patient and visitor parking is available in the main parking garage for a fee."
    }
}

# --- User Management System ---
def initialize_session_state():
    """Initialize session state variables"""
    if 'users' not in st.session_state:
        st.session_state.users = {
            'admin': {'password': 'admin123', 'role': 'admin', 'name': 'System Administrator'},
            'doctor1': {'password': 'doctor123', 'role': 'doctor', 'name': 'Dr. Emily Carter', 'department': 'Cardiology'},
            'doctor2': {'password': 'doctor123', 'role': 'doctor', 'name': 'Dr. Sarah Jenkins', 'department': 'Orthopedics'},
            'patient1': {'password': 'patient123', 'role': 'patient', 'name': 'John Doe'},
        }
    
    if 'appointments' not in st.session_state:
        st.session_state.appointments = []
    
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if 'current_user' not in st.session_state:
        st.session_state.current_user = None
    
    if 'user_role' not in st.session_state:
        st.session_state.user_role = None
    
    # Initialize rate limiting variables
    if 'last_api_call' not in st.session_state:
        st.session_state.last_api_call = 0
    
    if 'rate_limit_message' not in st.session_state:
        st.session_state.rate_limit_message = None

def login_user(username, password):
    """Authenticate user login"""
    if username in st.session_state.users and st.session_state.users[username]['password'] == password:
        st.session_state.logged_in = True
        st.session_state.current_user = username
        st.session_state.user_role = st.session_state.users[username]['role']
        return True
    return False

def logout_user():
    """Logout current user"""
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.session_state.user_role = None

def add_user(username, password, role, name, department=None):
    """Add a new user to the system"""
    if username in st.session_state.users:
        return False, "Username already exists"
    
    user_data = {'password': password, 'role': role, 'name': name}
    if role == 'doctor':
        user_data['department'] = department
    
    st.session_state.users[username] = user_data
    return True, "User added successfully"

def add_appointment(patient_name, doctor_name, department, date, time, symptoms=None):
    """Add a new appointment"""
    appointment_id = len(st.session_state.appointments) + 1
    appointment = {
        'id': appointment_id,
        'patient_name': patient_name,
        'doctor_name': doctor_name,
        'department': department,
        'date': date,
        'time': time,
        'symptoms': symptoms,
        'status': 'pending',  # pending, approved, rejected
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state.appointments.append(appointment)
    return appointment_id

# --- Initialize session state ---
initialize_session_state()

# --- Streamlit App ---
st.set_page_config(page_title="Multilingual Medical Assistant", page_icon="🩺", layout="wide")

# Apply custom styling
set_custom_style()

# --- Login/Logout Section ---
if not st.session_state.logged_in:
    # Create a centered layout for login
    st.markdown("""
    <div class="login-form">
        <h1 style="text-align: center; color: white; margin-bottom: 30px;">🩺 Multilingual Medical Assistant</h1>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        with st.form("login_form"):
            st.markdown("""
            <div class="login-form">
                <h2 style="text-align: center; color: white; margin-bottom: 20px;">Login to Your Account</h2>
            </div>
            """, unsafe_allow_html=True)
            
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_button = st.form_submit_button("Login")
            
            if login_button:
                if login_user(username, password):
                    st.success(f"Welcome {st.session_state.users[username]['name']}!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
        
        st.markdown("""
        <div style="background-color: rgba(255, 255, 255, 0.1); border-radius: 10px; padding: 15px; margin-top: 20px;">
            <h3 style="text-align: center;">Demo Accounts</h3>
            <p><strong>Admin:</strong> username: <code>admin</code>, password: <code>admin123</code></p>
            <p><strong>Doctor:</strong> username: <code>doctor1</code>, password: <code>doctor123</code></p>
            <p><strong>Patient:</strong> username: <code>patient1</code>, password: <code>patient123</code></p>
        </div>
        """, unsafe_allow_html=True)
    
else:
    # User is logged in - show the main application
    st.sidebar.markdown(f"""
    <div style="background-color: rgba(78, 115, 223, 0.3); border-radius: 10px; padding: 15px; margin-bottom: 15px;">
        <h3 style="color: white; margin-top: 0;">Welcome, {st.session_state.users[st.session_state.current_user]['name']}</h3>
        <p style="color: white; margin-bottom: 0;">Role: {st.session_state.user_role.title()}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.sidebar.button("Logout"):
        logout_user()
        st.rerun()
    
    # Main application based on user role
    if st.session_state.user_role == 'admin':
        # --- ADMIN DASHBOARD ---
        st.markdown("""
        <div class="section-header">
            <h1>🏥 Admin Dashboard</h1>
        </div>
        """, unsafe_allow_html=True)
        
        # Admin navigation
        admin_option = st.sidebar.selectbox(
            "Admin Menu",
            ["📊 Overview", "👥 User Management", "📅 All Appointments", "➕ Add Doctor", "📋 Manage Departments"]
        )
        
        if admin_option == "📊 Overview":
            st.markdown("""
            <div class="section-header">
                <h2>System Overview</h2>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                total_users = len(st.session_state.users)
                st.metric("Total Users", total_users)
            with col2:
                total_doctors = len([u for u in st.session_state.users.values() if u['role'] == 'doctor'])
                st.metric("Total Doctors", total_doctors)
            with col3:
                total_patients = len([u for u in st.session_state.users.values() if u['role'] == 'patient'])
                st.metric("Total Patients", total_patients)
            with col4:
                total_appointments = len(st.session_state.appointments)
                st.metric("Total Appointments", total_appointments)
            
            st.markdown("""
            <div class="section-header">
                <h3>Recent Appointments</h3>
            </div>
            """, unsafe_allow_html=True)
            
            if st.session_state.appointments:
                # Show last 10 appointments
                recent_appointments = sorted(st.session_state.appointments, key=lambda x: x['created_at'], reverse=True)[:10]
                for appt in recent_appointments:
                    status_color = {
                        'pending': '🟡',
                        'approved': '🟢',
                        'rejected': '🔴'
                    }
                    with st.expander(f"{status_color[appt['status']]} {appt['patient_name']} with {appt['doctor_name']} - {appt['date']}"):
                        st.write(f"**Department:** {appt['department']}")
                        st.write(f"**Time:** {appt['time']}")
                        st.write(f"**Status:** {appt['status'].title()}")
                        if appt['symptoms']:
                            st.write(f"**Symptoms:** {appt['symptoms']}")
                        st.write(f"**Created:** {appt['created_at']}")
            else:
                st.info("No appointments found.")
        
        elif admin_option == "👥 User Management":
            st.markdown("""
            <div class="section-header">
                <h2>User Management</h2>
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("add_user_form"):
                st.markdown("""
                <div style="background-color: rgba(255, 255, 255, 0.1); border-radius: 10px; padding: 15px; margin-bottom: 15px;">
                    <h3>Add New User</h3>
                </div>
                """, unsafe_allow_html=True)
                
                new_username = st.text_input("Username")
                new_password = st.text_input("Password", type="password")
                new_role = st.selectbox("Role", ["patient", "doctor", "admin"])
                new_name = st.text_input("Full Name")
                
                new_department = None
                if new_role == 'doctor':
                    new_department = st.selectbox("Department", list(HOSPITAL_DATA["departments"].keys()))
                
                add_user_button = st.form_submit_button("Add User")
                
                if add_user_button:
                    if new_username and new_password and new_name:
                        success, message = add_user(new_username, new_password, new_role, new_name, new_department)
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
                    else:
                        st.error("Please fill all required fields")
            
            st.markdown("""
            <div style="background-color: rgba(255, 255, 255, 0.1); border-radius: 10px; padding: 15px; margin-bottom: 15px;">
                <h3>Current Users</h3>
            </div>
            """, unsafe_allow_html=True)
            
            users_list = []
            for username, user_data in st.session_state.users.items():
                user_row = {
                    'Username': username,
                    'Name': user_data['name'],
                    'Role': user_data['role'].title()
                }
                if user_data['role'] == 'doctor':
                    user_row['Department'] = user_data.get('department', 'N/A')
                else:
                    user_row['Department'] = 'N/A'
                users_list.append(user_row)
            
            if users_list:
                users_df = pd.DataFrame(users_list)
                st.dataframe(users_df, use_container_width=True)
            else:
                st.info("No users found.")
        
        elif admin_option == "📅 All Appointments":
            st.markdown("""
            <div class="section-header">
                <h2>All Appointments</h2>
            </div>
            """, unsafe_allow_html=True)
            
            if st.session_state.appointments:
                appointments_list = []
                for appt in st.session_state.appointments:
                    appointments_list.append({
                        'ID': appt['id'],
                        'Patient': appt['patient_name'],
                        'Doctor': appt['doctor_name'],
                        'Department': appt['department'],
                        'Date': appt['date'],
                        'Time': appt['time'],
                        'Status': appt['status'].title(),
                        'Created': appt['created_at']
                    })
                
                appointments_df = pd.DataFrame(appointments_list)
                st.dataframe(appointments_df, use_container_width=True)
                
                # Appointment management
                st.markdown("""
                <div style="background-color: rgba(255, 255, 255, 0.1); border-radius: 10px; padding: 15px; margin-top: 15px;">
                    <h3>Manage Appointments</h3>
                </div>
                """, unsafe_allow_html=True)
                
                appointment_ids = [appt['id'] for appt in st.session_state.appointments]
                if appointment_ids:
                    selected_appointment_id = st.selectbox("Select Appointment ID to Manage", appointment_ids)
                    
                    if selected_appointment_id:
                        appointment = next((appt for appt in st.session_state.appointments if appt['id'] == selected_appointment_id), None)
                        if appointment:
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                if st.button("✅ Approve Appointment"):
                                    appointment['status'] = 'approved'
                                    st.success("Appointment approved!")
                                    st.rerun()
                            with col2:
                                if st.button("❌ Reject Appointment"):
                                    appointment['status'] = 'rejected'
                                    st.error("Appointment rejected!")
                                    st.rerun()
                            with col3:
                                if st.button("🗑️ Delete Appointment"):
                                    st.session_state.appointments = [appt for appt in st.session_state.appointments if appt['id'] != selected_appointment_id]
                                    st.warning("Appointment deleted!")
                                    st.rerun()
                else:
                    st.info("No appointments to manage.")
            else:
                st.info("No appointments found.")

        elif admin_option == "➕ Add Doctor":
            st.markdown("""
            <div class="section-header">
                <h2>Add New Doctor</h2>
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("add_doctor_form"):
                st.markdown("""
                <div style="background-color: rgba(255, 255, 255, 0.1); border-radius: 10px; padding: 15px; margin-bottom: 15px;">
                    <h3>Doctor Details</h3>
                </div>
                """, unsafe_allow_html=True)
                
                doc_username = st.text_input("Username")
                doc_password = st.text_input("Password", type="password")
                doc_name = st.text_input("Full Name")
                doc_department = st.selectbox("Department", list(HOSPITAL_DATA["departments"].keys()))
                doc_schedule = st.text_input("Schedule (e.g., Mon-Wed, 9:00 AM - 1:00 PM)")
                
                add_doctor_button = st.form_submit_button("Add Doctor")
                
                if add_doctor_button:
                    if doc_username and doc_password and doc_name and doc_department and doc_schedule:
                        # Add to users
                        success, message = add_user(doc_username, doc_password, 'doctor', doc_name, doc_department)
                        if success:
                            # Add to hospital data (simulation)
                            if doc_department not in HOSPITAL_DATA["doctors"]:
                                HOSPITAL_DATA["doctors"][doc_department] = []
                            
                            HOSPITAL_DATA["doctors"][doc_department].append({
                                "name": doc_name,
                                "schedule": doc_schedule
                            })
                            st.success("Doctor added successfully!")
                            st.rerun()
                        else:
                            st.error(message)
                    else:
                        st.error("Please fill all required fields")
        
        elif admin_option == "📋 Manage Departments":
            st.markdown("""
            <div class="section-header">
                <h2>Manage Departments</h2>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div style="background-color: rgba(255, 255, 255, 0.1); border-radius: 10px; padding: 15px; margin-bottom: 15px;">
                    <h3>Add New Department</h3>
                </div>
                """, unsafe_allow_html=True)
                
                with st.form("add_department_form"):
                    new_dept_name = st.text_input("Department Name")
                    new_dept_location = st.text_input("Department Location")
                    add_dept_button = st.form_submit_button("Add Department")
                    
                    if add_dept_button:
                        if new_dept_name and new_dept_location:
                            if new_dept_name not in HOSPITAL_DATA["departments"]:
                                HOSPITAL_DATA["departments"][new_dept_name] = new_dept_location
                                HOSPITAL_DATA["doctors"][new_dept_name] = []
                                st.success(f"Department '{new_dept_name}' added successfully!")
                                st.rerun()
                            else:
                                st.error("Department with this name already exists.")
                        else:
                            st.error("Please fill all fields")
            
            with col2:
                st.markdown("""
                <div style="background-color: rgba(255, 255, 255, 0.1); border-radius: 10px; padding: 15px; margin-bottom: 15px;">
                    <h3>Current Departments</h3>
                </div>
                """, unsafe_allow_html=True)
                
                for dept, location in list(HOSPITAL_DATA["departments"].items()):
                    with st.expander(f"🏥 {dept}"):
                        st.write(f"**Location:** {location}")
                        st.write(f"**Doctors:** {len(HOSPITAL_DATA['doctors'].get(dept, []))}")
                        if st.button(f"Delete {dept}", key=f"delete_{dept}"):
                            # This is a temporary deletion for the session
                            del HOSPITAL_DATA["departments"][dept]
                            if dept in HOSPITAL_DATA["doctors"]:
                                del HOSPITAL_DATA["doctors"][dept]
                            st.warning(f"Department '{dept}' deleted for this session!")
                            st.rerun()
    
    elif st.session_state.user_role == 'doctor':
        # --- DOCTOR DASHBOARD ---
        doctor_name = st.session_state.users[st.session_state.current_user]['name']
        doctor_dept = st.session_state.users[st.session_state.current_user]['department']
        
        st.markdown(f"""
        <div class="section-header">
            <h1>👨‍⚕️ Doctor Dashboard - {doctor_name}</h1>
            <p>Department: {doctor_dept}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Doctor navigation
        doctor_option = st.sidebar.selectbox(
            "Doctor Menu",
            ["📋 Appointment Requests", "📊 My Schedule", "👥 My Patients"]
        )
        
        if doctor_option == "📋 Appointment Requests":
            st.markdown("""
            <div class="section-header">
                <h2>Appointment Requests</h2>
            </div>
            """, unsafe_allow_html=True)
            
            # Filter appointments for this doctor
            my_appointments = [appt for appt in st.session_state.appointments 
                             if appt['doctor_name'] == doctor_name]
            
            pending_appointments = [appt for appt in my_appointments if appt['status'] == 'pending']
            
            st.markdown(f"""
            <div style="background-color: rgba(255, 255, 255, 0.1); border-radius: 10px; padding: 15px; margin-bottom: 15px;">
                <h3>Pending Requests ({len(pending_appointments)})</h3>
            </div>
            """, unsafe_allow_html=True)
            
            if pending_appointments:
                for appt in pending_appointments:
                    with st.container():
                        st.markdown(f"**Patient:** {appt['patient_name']} | **Date:** {appt['date']} at {appt['time']}")
                        if appt['symptoms']:
                            st.info(f"**Reported Symptoms:** {appt['symptoms']}")
                        
                        col1, col2, col3 = st.columns([1,1,5])
                        with col1:
                            if st.button("✅ Approve", key=f"approve_{appt['id']}"):
                                appt['status'] = 'approved'
                                st.success(f"Approved appointment with {appt['patient_name']}")
                                st.rerun()
                        with col2:
                            if st.button("❌ Reject", key=f"reject_{appt['id']}"):
                                appt['status'] = 'rejected'
                                st.error(f"Rejected appointment with {appt['patient_name']}")
                                st.rerun()
                        st.markdown("---")
            else:
                st.info("No pending appointment requests.")

            # Expander for past decisions
            with st.expander("View Processed Appointments"):
                approved_appointments = [appt for appt in my_appointments if appt['status'] == 'approved']
                rejected_appointments = [appt for appt in my_appointments if appt['status'] == 'rejected']

                st.markdown("<h4>Approved Appointments</h4>", unsafe_allow_html=True)
                if approved_appointments:
                    for appt in approved_appointments:
                        st.success(f"✅ {appt['patient_name']} - {appt['date']} at {appt['time']}")
                else:
                    st.info("No approved appointments.")

                st.markdown("<h4>Rejected Appointments</h4>", unsafe_allow_html=True)
                if rejected_appointments:
                    for appt in rejected_appointments:
                        st.error(f"❌ {appt['patient_name']} - {appt['date']} at {appt['time']}")
                else:
                    st.info("No rejected appointments.")
        
        elif doctor_option == "📊 My Schedule":
            st.markdown("""
            <div class="section-header">
                <h2>My Schedule</h2>
            </div>
            """, unsafe_allow_html=True)
            
            # Show upcoming approved appointments
            upcoming_appointments = [appt for appt in st.session_state.appointments 
                                   if appt['doctor_name'] == doctor_name and 
                                   appt['status'] == 'approved' and
                                   datetime.strptime(appt['date'], "%Y-%m-%d").date() >= datetime.now().date()]
            
            if upcoming_appointments:
                st.info("Showing upcoming appointments sorted by date and time.")
                for appt in sorted(upcoming_appointments, key=lambda x: (x['date'], x['time'])):
                    with st.expander(f"📅 {appt['date']} at {appt['time']} - {appt['patient_name']}"):
                        st.write(f"**Department:** {appt['department']}")
                        if appt['symptoms']:
                            st.write(f"**Reported Symptoms:** {appt['symptoms']}")
                        st.write(f"**Appointment Requested On:** {appt['created_at']}")
            else:
                st.info("No upcoming appointments.")
        
        elif doctor_option == "👥 My Patients":
            st.markdown("""
            <div class="section-header">
                <h2>My Patients</h2>
            </div>
            """, unsafe_allow_html=True)
            
            # Get all patients who have approved appointments with this doctor
            my_patients_appts = [appt for appt in st.session_state.appointments 
                               if appt['doctor_name'] == doctor_name and appt['status'] == 'approved']
            
            if my_patients_appts:
                # Group appointments by patient name
                patients_summary = {}
                for appt in my_patients_appts:
                    patient_name = appt['patient_name']
                    if patient_name not in patients_summary:
                        patients_summary[patient_name] = {'appointments': [], 'symptoms': set()}
                    
                    patients_summary[patient_name]['appointments'].append(appt)
                    if appt['symptoms']:
                        patients_summary[patient_name]['symptoms'].add(appt['symptoms'])
                
                for patient, data in patients_summary.items():
                    with st.expander(f"👤 {patient} ({len(data['appointments'])} appointments)"):
                        st.write(f"**Total Approved Appointments:** {len(data['appointments'])}")
                        if data['symptoms']:
                            st.write("**All Reported Symptoms:**")
                            for symptom in data['symptoms']:
                                st.markdown(f"- {symptom}")
                        
                        st.write("**Appointment History:**")
                        for appt in sorted(data['appointments'], key=lambda x: x['date'], reverse=True):
                            st.write(f"- {appt['date']} at {appt['time']}")
            else:
                st.info("No patients with approved appointments found.")
    
    elif st.session_state.user_role == 'patient':
        # --- PATIENT DASHBOARD ---
        patient_name = st.session_state.users[st.session_state.current_user]['name']
        
        st.markdown(f"""
        <div class="section-header">
            <h1>🩺 Multilingual Medical Assistant</h1>
            <p>Welcome, {patient_name}</p>
        </div>
        """, unsafe_allow_html=True)

        # Patient navigation
        patient_option = st.sidebar.selectbox(
            "Patient Menu",
            ["💬 Chatbot", "❤️ Health Awareness", "🏥 Appointment Assistance", "🩺 Symptom Checker", 
             "📖 Medical Education", "🧑‍🌾 Rural Healthcare", "📋 My Medical History"]
        )

        if patient_option == "💬 Chatbot":
            st.markdown("""
            <div class="section-header">
                <h2>Ask a Medical Question</h2>
            </div>
            """, unsafe_allow_html=True)
            
            # Check if we need to show a rate limit warning
            is_rate_limited, wait_time = check_rate_limit()
            if is_rate_limited:
                st.markdown(f"""
                <div class="rate-limit-warning">
                    <h3>⏱️ Rate Limit Notice</h3>
                    <p>You've reached the free tier limit for API requests. Please wait <strong>{int(wait_time)} seconds</strong> before making another request.</p>
                    <p>This is a limitation of the free API tier. For unlimited usage, consider upgrading to a paid plan.</p>
                </div>
                """, unsafe_allow_html=True)
            
            if 'model' not in st.session_state:
                st.session_state.model = genai.GenerativeModel(
                    model_name="gemini-2.5-pro",
                    generation_config=generation_config,
                    system_instruction=system_instruction,
                )
            if 'chat' not in st.session_state:
                st.session_state.chat = st.session_state.model.start_chat(history=[])
            if "messages" not in st.session_state:
                st.session_state.messages = []

            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
            
            if prompt := st.chat_input("What is your medical query?"):
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)

                try:
                    # FIXED TRANSLATION CODE
                    # Detect language
                    detected_lang_code = detect_language(prompt)
                    detected_lang_name = get_language_name(detected_lang_code)
                    
                    # Translate to English if needed
                    translated_to_english = prompt
                    if detected_lang_code != 'en':
                        # Use the improved translation function
                        translated_prompt = translate_text(prompt, 'en')
                        if translated_prompt:
                            translated_to_english = translated_prompt
                        else:
                            st.warning("Could not translate your query to English. The AI will respond based on the original text.")

                    with st.chat_message("assistant"):
                        with st.status(f"Detected: {detected_lang_name.title()}. Thinking...", expanded=True):
                            # Check rate limit before making API call
                            is_rate_limited, wait_time = check_rate_limit()
                            if is_rate_limited:
                                st.error(f"Rate limit exceeded. Please wait {int(wait_time)} seconds before trying again.")
                                st.stop()
                            
                            # Get AI response with retry logic
                            max_retries = 3
                            retry_count = 0
                            english_response = None
                            
                            while retry_count < max_retries and english_response is None:
                                try:
                                    update_last_api_call()
                                    response = st.session_state.chat.send_message(translated_to_english)
                                    english_response = response.text
                                except Exception as e:
                                    is_rate_error, retry_delay = handle_rate_limit_error(e)
                                    
                                    if is_rate_error and retry_count < max_retries - 1:
                                        st.warning(f"Rate limit hit. Waiting {retry_delay} seconds before retry...")
                                        time.sleep(retry_delay)
                                        retry_count += 1
                                    else:
                                        st.error(f"Error: {str(e)}")
                                        st.stop()
                            
                            if english_response:
                                st.write("Translating response back to your language...")
                                
                                # Translate response back to original language if needed
                                translated_response_to_original = english_response
                                if detected_lang_code != 'en':
                                    final_response = translate_text(english_response, detected_lang_code)
                                    if final_response:
                                       translated_response_to_original = final_response
                                    else:
                                        st.warning("Could not translate the response back to your language. Displaying the original English response.")


                        if english_response:
                            st.markdown(translated_response_to_original)
                            with st.expander("See original response from the doctor (AI)"):
                                st.write(english_response)
                            st.session_state.messages.append({"role": "assistant", "content": translated_response_to_original})
                
                except Exception as e:
                    st.error(f"An error occurred during translation or AI response: {str(e)}")
                    # Add debug information
                    st.info("If translation continues to fail, the chatbot will work in English only.")
        
        # ------------------- CORRECTED HEALTH AWARENESS BLOCK START -------------------
        elif patient_option == "❤️ Health Awareness":
            st.markdown("""
            <div class="section-header">
                <h2>Public Health Awareness Campaigns</h2>
                <p>Get important health information in your local language.</p>
            </div>
            """, unsafe_allow_html=True)

            LANGUAGES = {
                'en': 'English', 'es': 'Spanish', 'fr': 'French', 'de': 'German', 'hi': 'Hindi', 'zh': 'Chinese',
                'ar': 'Arabic', 'pt': 'Portuguese', 'ru': 'Russian', 'ja': 'Japanese', 'bn': 'Bengali', 'ta': 'Tamil',
                'te': 'Telugu', 'mr': 'Marathi', 'gu': 'Gujarati', 'kn': 'Kannada', 'ml': 'Malayalam', 'pa': 'Punjabi'
            }
            
            lang_names = {code: name.title() for code, name in LANGUAGES.items()}
            selected_lang_name = st.selectbox(
                "First, select your language:",
                options=list(lang_names.values()),
                index=list(lang_names.keys()).index('en'),
                key='health_lang_select'
            )
            selected_lang_code = [code for code, name in lang_names.items() if name == selected_lang_name][0]
            
            st.markdown("""
            <div style="background-color: rgba(255, 255, 255, 0.1); border-radius: 10px; padding: 15px; margin-bottom: 15px;">
                <h3>Click a topic to learn more:</h3>
            </div>
            """, unsafe_allow_html=True)
            
            if 'health_info' not in st.session_state:
                st.session_state.health_info = None

            def set_health_info(topic_key):
                topic = HEALTH_MESSAGES[topic_key]
                
                # Default to English
                translated_title = topic["title"]
                translated_content = topic["content"]

                # Attempt translation if a different language is selected
                if selected_lang_code != 'en':
                    # Use the improved translate_text function
                    title_result = translate_text(topic["title"], selected_lang_code)
                    content_result = translate_text(topic["content"], selected_lang_code)
                    
                    # Check if both translations were successful
                    if title_result and content_result:
                        translated_title = title_result
                        translated_content = content_result
                    else:
                        # If translation fails, show a clear warning to the user
                        st.warning("Translation service failed. Displaying content in English.")
                
                st.session_state.health_info = (translated_title, translated_content)

            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🧼 Hygiene Tips", use_container_width=True): set_health_info("hygiene")
            with col2:
                if st.button("💉 Vaccination", use_container_width=True): set_health_info("vaccination")
            with col3:
                if st.button("🍎 Healthy Eating", use_container_width=True): set_health_info("healthy_eating")
            col4, col5, col6 = st.columns(3)
            with col4:
                if st.button("🧘‍♀️ Mental Health", use_container_width=True): set_health_info("mental_health")
            with col5:
                if st.button("🏃‍♂️ Regular Exercise", use_container_width=True): set_health_info("exercise")
            with col6:
                if st.button("😴 Quality Sleep", use_container_width=True): set_health_info("sleep")
            col7, col8, col9 = st.columns(3)
            with col7:
                if st.button("💧 Hydration", use_container_width=True): set_health_info("hydration")
            with col8:
                if st.button("❤️ Heart Attack Signs", use_container_width=True): set_health_info("heart_attack")
            with col9:
                if st.button("🧠 Stroke Signs (F.A.S.T.)", use_container_width=True): set_health_info("stroke")
            col10, col11, _ = st.columns(3)
            with col10:
                if st.button("🌡️ Fever Management", use_container_width=True): set_health_info("fever")
            with col11:
                if st.button("🔥 First Aid for Burns", use_container_width=True): set_health_info("first_aid_burns")
            
            if st.session_state.health_info:
                title, content = st.session_state.health_info
                st.markdown(f"""
                <div style="background-color: rgba(78, 115, 223, 0.3); border-radius: 10px; padding: 15px; margin-top: 15px;">
                    <h3>{title}</h3>
                    <p>{content}</p>
                </div>
                """, unsafe_allow_html=True)
        # ------------------- CORRECTED HEALTH AWARENESS BLOCK END -------------------

        elif patient_option == "🏥 Appointment Assistance":
            st.markdown("""
            <div class="section-header">
                <h2>Hospital and Appointment Assistance</h2>
                <p>Find information about departments, doctors, and book a simulated appointment.</p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("appointment_form"):
                st.markdown("""
                <div style="background-color: rgba(255, 255, 255, 0.1); border-radius: 10px; padding: 15px; margin-bottom: 15px;">
                    <h3>🗓️ Book an Appointment</h3>
                </div>
                """, unsafe_allow_html=True)
            
                departments = list(HOSPITAL_DATA["departments"].keys())
                dept_choice = st.selectbox("1. Select a Department:", departments)
                
                doctors_in_dept = []
                if dept_choice and dept_choice in HOSPITAL_DATA["doctors"]:
                    doctors_in_dept = [doc["name"] for doc in HOSPITAL_DATA["doctors"][dept_choice]]
                
                doc_choice = st.selectbox("2. Select a Doctor:", doctors_in_dept if doctors_in_dept else ["No doctors available"])
                
                app_date = st.date_input("3. Select a Date:", min_value=datetime.now().date())
                app_time = st.time_input("4. Select a Time:", value=datetime.now().time())
                
                symptoms = st.text_area("5. Describe your symptoms (optional):", 
                                      placeholder="Briefly describe what brings you in today...")
                
                submitted = st.form_submit_button("Confirm Appointment")
                if submitted:
                    if dept_choice and doc_choice != "No doctors available" and app_date and app_time:
                        add_appointment(
                            patient_name=patient_name,
                            doctor_name=doc_choice,
                            department=dept_choice,
                            date=app_date.strftime("%Y-%m-%d"),
                            time=app_time.strftime("%H:%M"),
                            symptoms=symptoms
                        )
                        st.success(f"✅ Your appointment with **{doc_choice}** on **{app_date}** at **{app_time.strftime('%I:%M %p')}** has been requested. You will receive a confirmation shortly.")
                        st.balloons()
                    else:
                        st.error("Please ensure a valid department and doctor are selected.")
            
            st.markdown("""
            <div style="background-color: rgba(255, 255, 255, 0.1); border-radius: 10px; padding: 15px; margin-top: 20px;">
                <h3>My Appointments</h3>
            </div>
            """, unsafe_allow_html=True)
            
            patient_appointments = [appt for appt in st.session_state.appointments 
                                  if appt['patient_name'] == patient_name]
            
            if patient_appointments:
                for appt in sorted(patient_appointments, key=lambda x: x['date'], reverse=True):
                    status_icon = {'pending': '🟡', 'approved': '🟢', 'rejected': '🔴'}
                    with st.expander(f"{status_icon[appt['status']]} {appt['doctor_name']} - {appt['date']} ({appt['status'].title()})"):
                        st.write(f"**Department:** {appt['department']}")
                        st.write(f"**Time:** {appt['time']}")
                        st.write(f"**Status:** {appt['status'].title()}")
                        if appt['symptoms']:
                            st.write(f"**Your Symptoms:** {appt['symptoms']}")
                        st.write(f"**Requested:** {appt['created_at']}")
            else:
                st.info("You have no appointments yet.")
            
            with st.expander("ℹ️ Hospital Information and FAQs", expanded=False):
                st.markdown("<h4>Department and Doctor Information</h4>", unsafe_allow_html=True)
                info_dept_choice = st.selectbox(
                    "Select a department to see its location and doctor schedules:",
                    list(HOSPITAL_DATA["departments"].keys()),
                    key="info_dept"
                )
                if info_dept_choice:
                    location = HOSPITAL_DATA["departments"][info_dept_choice]
                    st.info(f"**Location for {info_dept_choice}:** {location}")
                    st.markdown(f"**Doctors in {info_dept_choice}:**")
                    if info_dept_choice in HOSPITAL_DATA["doctors"]:
                        for doc in HOSPITAL_DATA["doctors"][info_dept_choice]:
                            st.markdown(f"- **{doc['name']}**: {doc['schedule']}")
                    else:
                        st.write("No doctors listed for this department.")
                
                st.markdown("<h4>Frequently Asked Questions</h4>", unsafe_allow_html=True)
                for question, answer in HOSPITAL_DATA["faqs"].items():
                    st.markdown(f"**Q: {question}**")
                    st.markdown(f"A: {answer}")

        elif patient_option == "🩺 Symptom Checker":
            st.markdown("""
            <div class="section-header">
                <h2>🩺 Symptom Pre-Screening</h2>
                <p>Fill out this form before your consultation to help the doctor understand your condition better.</p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.form(key="symptom_form"):
                st.markdown("""
                <div style="background-color: rgba(255, 255, 255, 0.1); border-radius: 10px; padding: 15px; margin-bottom: 15px;">
                    <h3>Please describe your symptoms</h3>
                </div>
                """, unsafe_allow_html=True)
                
                main_symptom = st.text_input("What is your main symptom? (e.g., sore throat, back pain)")
                symptom_duration = st.text_input("How long have you had this symptom? (e.g., 3 days, 2 weeks)")
                symptom_severity = st.slider("On a scale of 1 (mild) to 10 (severe), how would you rate it?", 1, 10, 5)
                other_symptoms = st.text_area("Are you experiencing any other related symptoms? (optional)")
                preexisting_conditions = st.text_area("Do you have any pre-existing medical conditions? (e.g., diabetes, asthma) (optional)")
                
                submitted = st.form_submit_button("Generate Doctor's Summary")

            if submitted:
                if not main_symptom:
                    st.warning("Please enter your main symptom.")
                else:
                    st.markdown("""
                    <div style="background-color: rgba(78, 115, 223, 0.3); border-radius: 10px; padding: 15px; margin-top: 15px;">
                        <h3>Summary for Your Doctor</h3>
                        <p>You can show this summary to your doctor during the consultation.</p>
                    </div>
                    """, unsafe_allow_html=True)

                    summary = f"""
                    **Patient Symptom Report**
                    - **Main Symptom:** {main_symptom}
                    - **Symptom Duration:** {symptom_duration}
                    - **Reported Severity:** {symptom_severity}/10
                    - **Other Symptoms:** {other_symptoms if other_symptoms else "None reported"}
                    - **Pre-existing Conditions:** {preexisting_conditions if preexisting_conditions else "None reported"}
                    """
                    
                    st.success("Your summary has been generated successfully!")
                    st.markdown(summary)
                    
                    st.markdown("""
                    <div style="background-color: rgba(255, 255, 255, 0.1); border-radius: 10px; padding: 15px; margin-top: 15px;">
                        <h3>General Recovery Tips</h3>
                        <ul>
                            <li><strong>Rest:</strong> Your body needs energy to heal. Make sure to get plenty of sleep and rest.</li>
                            <li><strong>Stay Hydrated:</strong> Drink lots of fluids like water, broth, or herbal tea.</li>
                            <li><strong>Eat Nutritious Food:</strong> If you have an appetite, eat light, nutritious foods.</li>
                            <li><strong>Monitor Your Symptoms:</strong> If they get worse, contact a healthcare provider.</li>
                        </ul>
                        <p><strong>Disclaimer:</strong> <em>This is not medical advice. Always consult a professional.</em></p>
                    </div>
                    """, unsafe_allow_html=True)

        elif patient_option == "📖 Medical Education":
            st.markdown("""
            <div class="section-header">
                <h2>📖 Medical Education & Patient Guidance</h2>
                <p>Use this tool to better understand medical topics. This is for informational purposes only.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.warning("**Disclaimer:** The information provided here is generated by an AI and is not a substitute for professional medical advice. Always consult a qualified healthcare provider.")

            def get_ai_explanation(user_query, prompt_template):
                if 'model' not in st.session_state:
                    st.error("Please visit the Chatbot tab first to initialize the AI model.")
                    return None
                
                try:
                    # Check rate limit before making API call
                    is_rate_limited, wait_time = check_rate_limit()
                    if is_rate_limited:
                        st.error(f"Rate limit exceeded. Please wait {int(wait_time)} seconds before trying again.")
                        return None
                    
                    full_prompt = prompt_template.format(query=user_query)
                    
                    # Get AI response with retry logic
                    max_retries = 3
                    retry_count = 0
                    response_text = None
                    
                    while retry_count < max_retries and response_text is None:
                        try:
                            update_last_api_call()
                            response = st.session_state.model.generate_content(full_prompt)
                            response_text = response.text
                        except Exception as e:
                            is_rate_error, retry_delay = handle_rate_limit_error(e)
                            
                            if is_rate_error and retry_count < max_retries - 1:
                                st.warning(f"Rate limit hit. Waiting {retry_delay} seconds before retry...")
                                time.sleep(retry_delay)
                                retry_count += 1
                            else:
                                st.error(f"Error: {str(e)}")
                                return None
                    
                    return response_text
                except Exception as e:
                    st.error(f"An error occurred while communicating with the AI: {e}")
                    return None

            st.markdown("""
            <div style="background-color: rgba(255, 255, 255, 0.1); border-radius: 10px; padding: 15px; margin-bottom: 15px;">
                <h3>🔬 Explain a Medical Term</h3>
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("term_form"):
                term_to_explain = st.text_input("Enter a medical term (e.g., Hypertension, Anemia)", key="med_term")
                submit_term = st.form_submit_button("Explain Term")

            if submit_term and term_to_explain:
                prompt = "Explain the medical term '{query}' in simple, easy-to-understand language for a patient. Do not give any medical advice. Start by defining the term clearly."
                with st.spinner(f"Generating explanation for '{term_to_explain}'..."):
                    explanation = get_ai_explanation(term_to_explain, prompt)
                    if explanation:
                        st.markdown(f"""
                        <div style="background-color: rgba(78, 115, 223, 0.3); border-radius: 10px; padding: 15px;">
                            <h4>Explanation of {term_to_explain.title()}</h4>
                            <p>{explanation}</p>
                        </div>
                        """, unsafe_allow_html=True)

            st.markdown("""
            <div style="background-color: rgba(255, 255, 255, 0.1); border-radius: 10px; padding: 15px; margin-bottom: 15px;">
                <h3>💊 Get Medication Information</h3>
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("med_form"):
                med_name = st.text_input("Enter a medication name (e.g., Paracetamol, Amoxicillin)", key="med_name")
                submit_med = st.form_submit_button("Get Info")
                
            if submit_med and med_name:
                prompt = "Provide general patient information about the medication '{query}'. Include what it is typically used for and common precautions in simple language. Do not provide dosage information or medical advice. State clearly that this information does not replace a doctor's prescription."
                with st.spinner(f"Getting information for '{med_name}'..."):
                    explanation = get_ai_explanation(med_name, prompt)
                    if explanation:
                        st.markdown(f"""
                        <div style="background-color: rgba(78, 115, 223, 0.3); border-radius: 10px; padding: 15px;">
                            <h4>Information on {med_name.title()}</h4>
                            <p>{explanation}</p>
                        </div>
                        """, unsafe_allow_html=True)

            st.markdown("""
            <div style="background-color: rgba(255, 255, 255, 0.1); border-radius: 10px; padding: 15px; margin-bottom: 15px;">
                <h3>📄 Understand Lab Report Items</h3>
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("lab_form"):
                report_item = st.text_area(
                    "Enter a term or a line from a lab report (e.g., 'Hemoglobin A1c', 'High LDL Cholesterol')", 
                    key="lab_report",
                    help="Do NOT enter personal identifying information."
                )
                submit_lab = st.form_submit_button("Explain Report Item")
            
            if submit_lab and report_item:
                prompt = "Explain what the following lab report item '{query}' generally measures or indicates, in simple, easy-to-understand language for a patient. Explain what 'high' or 'low' levels might generally suggest. Do not provide a diagnosis or medical advice. Emphasize the importance of discussing results with a doctor."
                with st.spinner(f"Generating explanation for '{report_item}'..."):
                    explanation = get_ai_explanation(report_item, prompt)
                    if explanation:
                        st.markdown(f"""
                        <div style="background-color: rgba(78, 115, 223, 0.3); border-radius: 10px; padding: 15px;">
                            <h4>Explanation of {report_item.title()}</h4>
                            <p>{explanation}</p>
                        </div>
                        """, unsafe_allow_html=True)

        elif patient_option == "🧑‍🌾 Rural Healthcare":
            st.markdown("""
            <div class="section-header">
                <h2>🧑‍🌾 Rural & Remote Healthcare Assistance</h2>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="background-color: rgba(255, 255, 255, 0.1); border-radius: 10px; padding: 15px; margin-bottom: 15px;">
                <p>This section is dedicated to users in rural and remote areas who may face challenges 
                in accessing timely medical guidance due to distance or language barriers.</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div style="background-color: rgba(255, 255, 255, 0.1); border-radius: 10px; padding: 15px; margin-bottom: 15px;">
                <h3>💬 First-Level Guidance in Your Regional Language</h3>
                <p>Have a health question? Our medical assistant can provide basic first-level information
                and safe suggestions in many local languages. This can help you understand your symptoms
                better and know the next steps to take.</p>
                <p><strong>To use this feature, please go to the '💬 Chatbot' tab in the sidebar.</strong></p>
            </div>
            """, unsafe_allow_html=True)
            
            st.warning(
                "**Disclaimer:** The chatbot provides general health information and is not a substitute for a real doctor. "
                "For serious medical conditions, or in an emergency, please consult a qualified healthcare professional immediately."
            )
            
            st.markdown("""
            <div style="background-color: rgba(255, 255, 255, 0.1); border-radius: 10px; padding: 15px; margin-bottom: 15px;">
                <h3>❤️ Health Knowledge at Your Fingertips</h3>
                <p>Learn about important health topics like hygiene, nutrition, first aid, and recognizing
                symptoms of common illnesses. This information is available in multiple languages to
                improve healthcare awareness and accessibility.</p>
                <p><strong>To access these resources, please visit the '❤️ Health Awareness' tab in the sidebar and select your language.</strong></p>
            </div>
            """, unsafe_allow_html=True)

        elif patient_option == "📋 My Medical History":
            st.markdown("""
            <div class="section-header">
                <h2>📋 My Medical History</h2>
                <p>View your medical appointments and history.</p>
            </div>
            """, unsafe_allow_html=True)
            
            patient_appointments = [appt for appt in st.session_state.appointments 
                                  if appt['patient_name'] == patient_name]
            
            if patient_appointments:
                st.markdown("""
                <div style="background-color: rgba(255, 255, 255, 0.1); border-radius: 10px; padding: 15px; margin-bottom: 15px;">
                    <h3>Appointment History</h3>
                </div>
                """, unsafe_allow_html=True)
                
                for appt in sorted(patient_appointments, key=lambda x: x['date'], reverse=True):
                    status_color = {'pending': '🟡 Pending', 'approved': '🟢 Approved', 'rejected': '🔴 Rejected'}
                    with st.expander(f"{appt['date']} - {appt['doctor_name']} ({status_color[appt['status']]})"):
                        st.write(f"**Department:** {appt['department']}")
                        st.write(f"**Time:** {appt['time']}")
                        st.write(f"**Status:** {appt['status'].title()}")
                        if appt['symptoms']:
                            st.write(f"**Symptoms Reported:** {appt['symptoms']}")
                        st.write(f"**Appointment Created:** {appt['created_at']}")
            else:
                st.info("No medical history found.")
            
            st.markdown("""
            <div style="background-color: rgba(255, 255, 255, 0.1); border-radius: 10px; padding: 15px; margin-top: 15px;">
                <h3>Health Statistics</h3>
            </div>
            """, unsafe_allow_html=True)
            
            if patient_appointments:
                total_appointments = len(patient_appointments)
                approved_appointments = len([appt for appt in patient_appointments if appt['status'] == 'approved'])
                pending_appointments = len([appt for appt in patient_appointments if appt['status'] == 'pending'])
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Appointments", total_appointments)
                with col2:
                    st.metric("Approved Appointments", approved_appointments)
                with col3:
                    st.metric("Pending Appointments", pending_appointments)
            else:
                st.info("No health statistics available.")