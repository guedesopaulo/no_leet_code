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

1. Open the `main.py` file in a text editor
2. Locate the `CONFIG` dictionary at the beginning of the file
3. Create a .env with 
    - OPENAI_API_KEY=<your_open_ai_key>
    - EMAIL=<your_email>
    - PASSWORD_SMTP=<smtp_email_password>
4. You may need to create your smtp credentials
5. Optionally, change the capture hotkey (`"TECLA_ATALHO"`)

To configure email sending, you need to edit the `response_sender.py` file:

1. If not using Gmail, also change the SMTP server and port

## Running the Program

To run the program:

1. Open Command Prompt or PowerShell
2. Navigate to the folder where the files are saved
3. Run the command: `python main.py`

The program will display an initial message and then hide the console window after 3 seconds. From that moment, the program will run in the background.

## Capturing the Screen

To capture the screen and send it for analysis:

1. Display the programming question you want to solve
2. Press the configured hotkey combination (default: Ctrl+Shift+P)
3. The program will automatically capture the entire screen
4. The image will be sent to ChatGPT for analysis
5. The response will be saved in the `resposta_chatgpt.txt` file and sent by email (if configured)

## Stopping the Program

To stop the program, press Ctrl+C in the console window (if visible) or end the Python process via the Windows Task Manager.

## Troubleshooting

If you encounter problems running the program:

1. Check if all dependencies were installed correctly
2. Make sure your OpenAI API key is valid and active
3. If using email sending, verify your SMTP credentials
4. For screen capture issues, ensure the program has sufficient permissions

## Important Notes

- This program was developed to run on Windows systems
- The screen capture is performed discreetly and will not be detectable during screen sharing
- The program requires an active internet connection to send the image to ChatGPT
- Using the ChatGPT API may incur costs, depending on your OpenAI plan
"""
