# 📧 Yahoo Email Sorter

This project automatically processes and categorizes Yahoo emails based on sender address using Python. It includes three main components:

- `email_sorter_core.py`: The core logic for sorting emails.
- `email_sorter_background.py` (and `email_sorter_background.exe`): A background scheduler to run sorting periodically.
- `email_sorter_gui.py`: A Streamlit-based GUI to manage configurations.

## 🗂 Folder Structure

```
YahooEmailSorter/
├── config/                        # Contains config.json
├── dist/                          # Contains compiled .exe and runtime files
│   ├── email_sorter_background    # Compiled EXE for background script
│   ├── config.json                # Copied configuration used by the EXE
│   ├── last_uid.txt               # Tracks the last processed email UID
│   └── log.txt                    # Log of email processing history
├── build/                         # Intermediate build files (used by PyInstaller)
├── __pycache__/                   # Compiled Python cache files
├── email_sorter_core.py           # Core logic to sort emails via IMAP
├── email_sorter_background.py     # Background runner (scheduler)
├── email_sorter_gui.py            # Streamlit GUI
├── *.spec                         # PyInstaller spec files
├── launch_gui.py                  # Starts the Streamlit GUI
├── start_gui.bat                  # Batch file to run GUI on Windows
├── log.txt                        # Log file from local script runs
```

## 🧠 How It Works

### 1. `email_sorter_core.py`
- Connects to Yahoo Mail via IMAP.
- Reads credentials and folder names from `config/config.json`.
- Fetches all new emails since the last processed one (`last_uid.txt`).
- If sender is in the `important_senders` list, copies the email to the destination folder.
- Logs all actions in `log.txt`.

### 2. `email_sorter_background.py`
- Calls the core script every X minutes (default: 10 minutes).
- Can be compiled to `.exe` for easy background execution on Windows.
- If using `email_sorter_background.exe` (from the `dist/` folder), it reads:
  - `config.json` — email credentials and rules.
  - `log.txt` — keeps track of actions.
  - `last_uid.txt` — ensures emails are not reprocessed.

### 3. `email_sorter_gui.py`
- Provides a user interface built with Streamlit.
- Allows easy editing of:
  - Yahoo email credentials
  - Source and destination folders
  - List of important senders

### 4. `email_sorter_background.exe`
- A compiled version of the background scheduler script.
- Ideal for deployment with Windows Task Scheduler or autostart.
- Located in the `dist/` folder along with required files (`config.json`, `last_uid.txt`, `log.txt`).

## 🛠 Configuration

Edit the `config/config.json` file:

```json
{
  "email": "your_yahoo_email@yahoo.com",
  "password": "your_app_password",
  "source_folder": "INBOX",
  "destination_folder": "Important",
  "important_senders": [
    "sender1@mail.com",
    "sender2@mail.com"
  ]
     "interval_seconds": 60 #check time interval for new mail in seconds 
}
```

> ⚠️ Use Yahoo app password instead of your regular login password for IMAP access.

## 🚀 Usage

### Option A: Development (Python)

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run once:
   ```bash
   python email_sorter_core.py
   ```

3. Run scheduler:
   ```bash
   python email_sorter_background.py
   ```

4. Launch GUI:
   ```bash
   python launch_gui.py
   ```

### Option B: Production (Windows Executable)

1. Navigate to `dist/` directory.
2. Double-click `email_sorter_background.exe` to run the background sorter.
3. Ensure `config.json`, `log.txt`, and `last_uid.txt` are present in the same directory.

> ✅ Add `email_sorter_background.exe` to Task Scheduler or `Startup` folder for automation.

## 📁 Log Files

- `log.txt` — Tracks all actions, successes, and errors.
- `last_uid.txt` — Keeps track of the last UID processed to avoid reprocessing.

## 🧪 Build the EXE (Optional)

To rebuild the `.exe` manually:
```bash
pyinstaller --onefile email_sorter_background.spec
```

## ❓ Troubleshooting

- **Missing credentials**: Ensure your `config.json` is valid and in the correct folder (`dist/` if using `.exe`).
- **IMAP errors**: Use an [app password](https://help.yahoo.com/kb/SLN15241.html) for Yahoo Mail IMAP access.
- **Not sorting**: Check `log.txt` for errors and verify sender matches exactly.

## 📬 Contact

For questions or improvements, feel free to reach out!
wiliam Peries : 0773534167

