# Selenium Script for Web Authentication and localStorage Access

This Python script uses Selenium to open a web browser, log in to a web application, and fetch certain data from the `localStorage`.

## Requirements

- Python 3.x
- Selenium WebDriver
- A WebDriver-compatible browser (Firefox, Chrome, etc.)

## Installation

1. Install Python from [python.org](https://www.python.org/).
2. Create a virtual enviroment

   ```bash
   python -m venv venv
   ```

3. Activate the virtual enviroment

   On Windows System:

   ```bash
   source venv/Scripts/activate
   ```

   On Linux System:

   ```bash
   source venv/bin/activate
   ```

4. Install libraries using pip:

   ```bash
   pip install datetime inquirer numpy python-dotenv requests selenium
   ```

   or if you are using Python 3, you may have to use pip3

   ```bash
   pip3 install datetime inquirer numpy python-dotenv requests selenium
   ```

5. **Download WebDriver**  
   You will also need a WebDriver for interfacing with different web browsers.

   - **Geckodriver for Firefox**:  
     Download the appropriate version of Geckodriver for your system from [Geckodriver's GitHub releases](https://github.com/mozilla/geckodriver/releases).

   - **Chromedriver for Chrome**:  
     Download the correct version of Chromedriver based on your Chrome browser's version from [Chromedriver's download page](https://sites.google.com/a/chromium.org/chromedriver/downloads).

### Important Note

- Make sure to download the WebDriver version that corresponds to the version of the browser you are using. Otherwise, you might encounter compatibility issues.

## Configuration

1. Make sure to set up the `.env` file with the necessary environment variables:

   ```env
   USERNAME_HIBO="your_username"
   PASSWORD_HIBO="your_password"
   ```

2. Import the environment variables into your script:

   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```

## Usage

1. Run the script:

   ```bash
   python getTokenParking.py
   ```

2. The script will open the browser, perform the login, and fetch the requested data from the `localStorage`.

## Compile

1. Install auto-py-to-exe
   ```bash
   pip install auto-py-to-exe
   ```
2. Run
   ```bash
   auto-py-to-exe
   ```
3. Follow the step, include geckodriver.exe, chromedriver.exe and .env file on the root
4. open the output folder and execute getTokensParking.exe

## Code Explanation

- The script uses Selenium to open up the browser and navigate to the specified URL.
- It fills in form fields using identifiers from the HTML elements.
- It runs a JavaScript script to pull data from `localStorage`.
- Extracts and displays specific keys from the JSON object stored in `localStorage`.

## Important Notes

- The script handles exceptions for each action, outputting messages to the console if anything fails.
- The `localStorage` data is printed as JSON objects for easier future use.
- **This script is designed to function when there are more than three items in the `localStorage`.**
- **Before running the script, ensure you know which keys are stored in `localStorage` and their position. The script will extract values based on their position.**
