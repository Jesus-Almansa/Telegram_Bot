# Telegram Bot Project

Welcome to your first **Telegram Bot** built with Python, Docker, and Docker Compose! This project contains everything you need to set up and run your bot in a containerized environment.

---

## Table of Contents

1. [Project Overview](#project-overview)  
2. [Prerequisites](#prerequisites)  
3. [Setup & Configuration](#setup--configuration)  
   1. [Obtain Your API Key from BotFather](#1-obtain-your-api-key-from-botfather)  
   2. [Create and Configure Your `.env` File](#2-create-and-configure-your-env-file)  
   3. [Docker Configuration](#3-docker-configuration)  
4. [Running the Bot](#running-the-bot)  
5. [Project Structure](#project-structure)  
6. [Usage](#usage)  
7. [Troubleshooting](#troubleshooting)  
8. [License](#license)

---

## Project Overview

This repository sets up a **Telegram Bot** using Python 3.12. The bot can respond to various commands (`/start`, `/help`, `/custom`, `/anonymous`) as well as custom text messages (like greetings and farewells). It’s fully containerized, meaning you can run the bot with **Docker Compose** and avoid installing Python and dependencies locally.

Key highlights:

- **Python 3.12-based** Docker image (slim build).  
- Uses **`python-telegram-bot`** for bot functionality.  
- Contains a **Dockerfile** and a **docker-compose.yml** file for easy setup.  
- Demonstrates environment variable usage (`.env`) to keep secrets and tokens private.

---

## Prerequisites

Before you begin, ensure you have the following installed:

1. [Docker](https://www.docker.com/)  
2. [Docker Compose](https://docs.docker.com/compose/)  

That’s it—no local Python installation is required since everything is handled inside Docker.

---

## Setup & Configuration

### **1. Obtain Your API Key from BotFather**

1. In Telegram, search for **BotFather** (the official bot to create and manage Telegram bots).
2. Use the `/newbot` command to create a new bot.
3. BotFather will ask for a name and username (must end in "`_bot`" or "`Bot`").
4. Once created, BotFather will provide a **token** (API key). Copy this token for later use (it looks like `123456789:ABC-DEF1234ghIkl-zyx57W2v...`).

---

### **2. Create and Configure Your `.env` File**

1. Create a file named `.env` in the root of your project (next to the `docker-compose.yml` and `Dockerfile`).
2. Add the following lines (replacing with your actual values):

   ```ini
   API_KEY=123456789:ABCDEF_your_bot_token_here
   BOT_USERNAME=@YourBotUsername
   JESUS_PASSWORD=yourpassword
   IKER_PASSWORD=anotherpassword
   ```
   
   - **`API_KEY`** is the token from BotFather.  
   - **`BOT_USERNAME`** is your bot’s username (remember the `@` sign if you want to reference it in group chats).  
   - **`JESUS_PASSWORD` and `IKER_PASSWORD`** are just example user passwords for the container’s users.  

> **Note:** Never commit your `.env` file to public repositories to keep your secrets safe!

---

### **3. Docker Configuration**

#### **docker-compose.yml**

This file defines your service called **`app`**:

```yaml
services:
  app:
    build:
      context: .
      args:
        JESUS_PASSWORD: ${JESUS_PASSWORD}
        IKER_PASSWORD: ${IKER_PASSWORD}
    container_name: TelegramBot
    restart: always
    hostname: yharnam
    env_file:
      - .env
    volumes:
      - ../Bot/:/usr/src/app/workspace
    stdin_open: true
    tty: true
    user: "jesus"
```

- **`build:`** context points to the current directory (`.`) where the Dockerfile resides.  
- **`args:`** pass the passwords from `.env` into the Docker build.  
- **`restart: always`** ensures the container restarts automatically if it stops.  
- **`env_file:`** specifies the `.env` file to load environment variables.  
- **`volumes:`** mounts your local `../Bot/` folder into the container at `/usr/src/app/workspace` so that changes to your bot code are reflected.

#### **Dockerfile**

```dockerfile
# Use Python base image
FROM python:3.12-slim-bookworm

WORKDIR /usr/src/app/workspace

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git curl sudo nano wget unzip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create users JESUS and IKER
ARG JESUS_PASSWORD
ARG IKER_PASSWORD
RUN useradd -ms /bin/bash jesus && \
    echo "jesus:${JESUS_PASSWORD}" | chpasswd && \
    usermod -aG sudo jesus && \
    useradd -ms /bin/bash iker && \
    echo "iker:${IKER_PASSWORD}" | chpasswd && \
    usermod -aG sudo iker

# Sudo privileges without password
RUN echo "jesus ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && \
    echo "iker ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && visudo -c

# Change ownership of workspace
RUN chown -R jesus:jesus /usr/src/app/workspace && \
    chown -R iker:iker /usr/src/app/workspace

# Use jesus as default user
USER jesus

# Start command to run the bot on container startup
CMD ["python", "/usr/src/app/workspace/main.py"]
```

---

## Running the Bot

Once your `.env` file is set:

1. **Build and start your container**  
   ```bash
   docker-compose up --build
   ```
   or run it in detached mode:
   ```bash
   docker-compose up --build -d
   ```
2. Docker Compose will build the image based on the **Dockerfile**, install dependencies, and run your `main.py`.

When you see `Bot is polling!` in the logs, your bot is live!

> **Tip**: If you run in detached mode (`-d`), you can view logs with:
> ```bash
> docker-compose logs -f
> ```

---

## Project Structure

Here's a simplified structure:

```
.
├── Docker/
|        ├── docker-compose.yml
|        ├── Dockerfile
|        ├── requirements.txt
├── Bot/
|       ├── .env                # Contains your API_KEY, BOT_USERNAME, and passwords
|       ├── main.py             # Main bot script
```

- **`requirements.txt`** lists Python dependencies (e.g., `python-telegram-bot`).
- **`main.py`** is the heart of the bot, containing commands and message handling.
- **`.env`** houses sensitive info (API key & credentials).

---

## Usage

### **1. Create Your Bot**
- Go to **BotFather** in Telegram, create a new bot, and copy the API Key.

### **2. Add the Bot’s Commands**
- In BotFather, use `/setcommands` to register new commands.  
  For example:
  ```
  start - Start the bot
  help - Get help
  custom - A custom command
  ```
  This helps Telegram show command suggestions to users.

### **3. Interact with the Bot**
- Open Telegram, search for your bot by its username.
- Click **Start** or type `/start`.
- Test out the commands:
  - **`/start`**  
  - **`/help`**  
  - **`/custom`**  
- Send random text messages or greetings to see how the bot responds. If in a group, don’t forget to mention the bot’s username if you want it to respond (`@YourBotUsername Hello!`).

### **4. Modify Responses**
- In `main.py`, check the `handle_response(text: str)` function. Add or modify conditions for different phrases to customize how your bot replies.

---

## **Current Capabilities**
This bot **works based on predefined responses**. It can:

✅ Greet users and say goodbye  
✅ Answer simple questions (`how are you?`)  
✅ Recognize morning/night greetings  
✅ Respond to gratitude (`thank you!`)  
✅ React to specific phrases  

Here’s how the response logic is structured:
```python
def handle_response(text: str):
    processed = text.lower()

    if "hello" in processed:
        return "¡Hola! ¿Cómo estás?"
    if "bye" in processed:
        return "¡Adiós! Espero verte pronto."
    
    return "No entiendo lo que quieres decir. 🤔"
```
🚀 **This is just the foundation. The next step is to upgrade it with AI!**

---

## **Future Plans: LLM Integration**
While predefined responses are great, they **limit the bot’s ability to truly engage in conversation**.  
The **next step** is integrating an **LLM** (Large Language Model) like:

- **OpenAI’s GPT (ChatGPT)**
- **Google’s Gemini**
- **Facebook’s LLaMA**
- **Local LLMs (e.g., Mistral, GPT4All)**

### **How will LLM Integration Work?**
Instead of matching predefined responses, the bot will:
1. **Receive a user’s message**
2. **Send it to an LLM API** (like OpenAI’s API or a locally hosted model)
3. **Get an intelligent response** and send it back to the user

#### **Example Integration with OpenAI API**
```python
import openai

def ask_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']
```

#### **Benefits of Using LLM**
✅ **More natural conversations**  
✅ **Ability to answer a wider range of questions**  
✅ **Support for multiple languages**  
✅ **Custom personalities and behavior**  

With LLM integration, this bot **will evolve from a simple rule-based chatbot into a true AI-powered assistant!** 🚀

---



## Troubleshooting

1. **Container Exits Immediately**  
   - Check if `main.py` has an infinite process (like `app.run_polling()`). If the script just finishes, the container will stop.  
   - Make sure you’re using the correct **`CMD`** in your Dockerfile.

2. **Bot Not Responding**  
   - Verify your **API_KEY** in `.env` is correct.  
   - Check container logs:  
     ```bash
     docker-compose logs -f
     ```
   - Ensure you configured BotFather commands properly.

3. **Permissions Issues**  
   - The Dockerfile sets up two users, `jesus` and `iker`. Make sure you’re running with the `jesus` user (as defined).  
   - Confirm you have the correct ownership or try removing `user: "jesus"` from `docker-compose.yml` if there are mounting issues.

4. **Token Invalid**  
   - Request a new token from BotFather if the current one is not working.  
   - Update `.env` and rebuild the container.

---

## License

This project does not specify a license by default. If you plan on sharing or contributing, please add a license (e.g., MIT, Apache 2.0) to let others know how they can use your code.

---

**Happy Bot Building!** If you have any questions or suggestions, feel free to open an issue or submit a pull request. Enjoy your new **Telegram Bot** in Docker!