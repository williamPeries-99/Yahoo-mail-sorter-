import subprocess
import os

# Get the absolute path to the Streamlit GUI file
base_dir = os.path.dirname(os.path.abspath(__file__))
gui_file = os.path.join(base_dir, "email_sorter_gui.py")

# Run streamlit using the full path
subprocess.Popen(["streamlit", "run", gui_file])
