# Setup

## 1. Create and activate the environment

```
conda env create -n no_leet_code -f environment.yml
conda activate no_leet_code
```

## 2. Sync dependencies
```bash
uv pip sync requirements.txt
```

If you changed something in the setug.cfg, run:

```bash
uv pip compile setup.cfg -o requirements.txt
uv pip sync requirements.txt
```

# How to Run

1. Create a .env with 
    - OPENAI_API_KEY=<your_open_ai_key>
    - EMAIL=<your_email>
    - PASSWORD_SMTP=<smtp_email_password>
2. You may need to create your smtp credentials
3. Optionally, change the capture hotkey (`"TECLA_ATALHO"`) in main.py


To configure email sending, you need to edit the `response_sender.py` file:

1. If not using Gmail, also change the SMTP server and port

## Running the Program

To run the program:

1. Open Command Prompt or PowerShell
2. Navigate to the folder where the files are saved
3. Run the command: `python main.py`

The program will display an initial message and then hide the console window after 3 seconds. From that moment, the program will run in the background.


## Important Notes

- This program was developed to run on Windows systems
- The screen capture is performed discreetly and will not be detectable during screen sharing
