import re
import streamlit as st
import random
import string

st.markdown(
    """
    <style>
    body, [data-testid="stAppViewContainer"] {
        background: url('https://seds.org/wp-content/uploads/2020/03/outer-space-stars-galaxies-nasa_www.wallpaperhi.com_18.jpg') no-repeat center center fixed;
         background-size: cover;
   
        
    }
    .content-box {
        display: flex;
        flex-direction: column;
        justify-content: center;
        width: 800px;
        height: 510px;
        margin-top: 18px;
        position: absolute;
          left: 50%; 
    transform: translateX(-50%);
        border-radius: 14px;
        border: 1px solid #f9f9f9;
        backdrop-filter: blur(30px);
        box-shadow: 0px 4px 4px -1px rgba(0, 0, 0, 0.25);
   
    }
    h1 {
    color: white !important;
}
    h1#password-strength-checker {
    text-color:white !important;
}

    input[type="password"]::-ms-reveal,
    input[type="password"]::-webkit-credentials-auto-fill-button,
    input[type="password"]::-webkit-password-eye {
        display: none !important;
    }


     .st-emotion-cache-18netey h1 {
        font-size: 30px;
        font-weight: bold;
        color: white !important;
        text-align: left;
        padding-top:0px;
    }

    .st-emotion-cache-1104ytp p {
        font-size: 18px !important;
        color: white !important;
        text-align: left;
    }

    .stButton>button {
        background-color: #A4B465;
        color: white;
        font-size: 22px !important;
        border-radius: 5px;
        padding: 7px;
        width: 100%;
        border: none;
        margin-top:10px;
        transition: transform 0.4s ease-in-out;
    }
    .st-ba {
    height: 2.5rem;
}
.st-bt {
    padding-left: 0.8rem;
}
    .st-emotion-cache-1hyd1ho p {
     font-size: 18px !important;
    }
    .st-ay {
    font-size: 1.1rem;
}
    
    .stButton>button:hover, 
    .stButton>button:focus, 
    .stButton>button:active, 
    .stButton>button:visited {
        background-color: #626F47;
        color: white !important;
        transform: scale(1.03);
    }
    @media (max-width: 768px) {
    .content-box {
        width: 110%;
        min-height: auto;
        padding: 15px;
    }
    h1 {
        font-size: 22px !important;
        text-align: center;
    }
    .stButton>button {
        font-size: 16px !important;
        padding: 8px;
    }
    .st-emotion-cache-1104ytp p {
        font-size: 16px !important;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def time_to_crack(password):
    charset_size = 0
    special_chars = "!@#$%^&*()-_=+[]{};:/?.>"
    
    if any(c.islower() for c in password):
        charset_size += 26 
    if any(c.isupper() for c in password):
        charset_size += 26  
    if any(c.isdigit() for c in password):
        charset_size += 10  
    if any(c in special_chars for c in password):
        charset_size += len(special_chars)  
    
    total_combinations = charset_size ** len(password)
    offline_attack_speed = 10**11 
    time_seconds = total_combinations / offline_attack_speed

    if time_seconds < 60:
        return f"{time_seconds:.2f} seconds"
    elif time_seconds < 3600:
        return f"{time_seconds / 60:.2f} minutes"
    elif time_seconds < 86400:
        return f"{time_seconds / 3600:.2f} hours"
    elif time_seconds < 31536000:
        return f"{time_seconds / 86400:.2f} days"
    elif time_seconds < 3153600000:
        return f"{time_seconds / 31536000:.2f} years"
    else:
        return f"{time_seconds / 3153600000:.2f} centuries"

def generate_strong_password(length=12):
    if length < 8:
        raise ValueError("Password length must be at least 8")
    
    digit = random.choice(string.digits)
    uppercase = random.choice(string.ascii_uppercase)
    lowercase = random.choice(string.ascii_lowercase)
    special = random.choice("!@#$%^&*()-_=+[]{};:/?.>")
    
    remaining_length = length - 4
    all_characters = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{};:/?.>"
    remaining_chars = random.choices(all_characters, k=remaining_length)
    
    password = [digit, uppercase, lowercase, special] + remaining_chars
    random.shuffle(password)
    
    return ''.join(password)

def password_strength_checker(password):
    crack_time = time_to_crack(password)
    
    if len(password) < 8:
        st.error("Weak: Password must be at least 8 characters long.")
        st.info(f"⏳ Estimated crack time: {crack_time}")
        return
    
    if not any(char.isdigit() for char in password):
        st.error("Weak: Password must contain a digit.")
        st.info(f"⏳ Estimated crack time: {crack_time}")
        return
    
    if not any(char.isupper() for char in password):
        st.error("Weak: Password must contain at least one uppercase letter.")
        st.info(f"⏳ Estimated crack time: {crack_time}")
        return
    
    if not any(char.islower() for char in password):
        st.error("Weak: Password must contain at least one lowercase letter.")
        st.info(f"⏳ Estimated crack time: {crack_time}")
        return
    
    if not re.search(r'[!@#$%^&*()\-_=+|[\]{};:/?.>]', password):
        st.warning("Medium: Add special characters to make the password stronger.")
        st.info(f"⏳ Estimated crack time: {crack_time}")
        return
    
    st.success("Strong: Password is secure!")
    st.info(f"⏳ Estimated crack time: {crack_time}")


if "password" not in st.session_state:
    st.session_state.password = ""



st.markdown('<div class="content-box">', unsafe_allow_html=True)
st.markdown('<h1 class="title">Password Strength Checker</h1>', unsafe_allow_html=True)
st.markdown('<p class="description">Enter a password below to check its strength.</p>', unsafe_allow_html=True)

password = st.text_input("", type="password", key="password_input", value=st.session_state.password)
if st.button("Check Password Strength"):
    if password:
        password_strength_checker(password)
    else:
        st.warning("⚠️ Please enter a password before checking.")

if st.button("Suggest Strong Password"):
    st.session_state.password = generate_strong_password(12)
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)





