import pickle
from pathlib import Path

import streamlit_authenticator as stauth

names = ["Evan Spencer", "Keith Key"]
usernames = ["espencer", "kkey"]
passwords = ["seekingALPHA6", "temp123"]

hashed_passwords = stauth.Hasher(passwords).generate()

file_path = Path(__file__).parent / "hashed_pw_kbk.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)