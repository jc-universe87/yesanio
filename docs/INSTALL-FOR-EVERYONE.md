# Installing Yesanio — the friendly walkthrough

A patient, no-jargon guide for installing Yesanio on your own computer.

This guide is for you if you've used a computer for years for normal things — email, browsing, writing documents — but you've never installed something like Yesanio before, never opened a "terminal", and the words "container" and "Docker" don't mean anything to you yet.

That's completely fine. By the end of this guide, you'll have Yesanio running on your computer and you'll have learned a few new things along the way. None of it is hard. Some of it just looks unfamiliar.

---

## A note on honesty before we start

Installing Yesanio is not as easy as installing Microsoft Word. There is no "click the button, wait, done" experience yet. The reason is technical and worth understanding briefly: Yesanio is made of three small pieces of software that talk to each other, and getting them onto your computer requires a tool called Docker that orchestrates them. Docker itself is well-made and free, but installing it for the first time involves a few clicks that look unfamiliar — and on Windows, sometimes a small change to your computer's settings.

Here's the honest preview:

- **Time:** plan for 30 to 60 minutes the first time. Most of that is waiting for downloads.
- **Difficulty:** moderate but not technical. You'll be following written instructions exactly. No code to write.
- **What you'll need:** a reasonably modern computer (Windows 10/11, macOS, Linux, or a Chromebook from the last 5 years), an internet connection, and ~3 GB of free disk space.
- **What can go wrong:** mostly Docker installation issues. If you hit one, this guide tells you what it means and what to do.
- **When to ask for help:** if anything in this guide doesn't match what you see on screen and you can't tell why, that's a normal moment to ask a more technical friend or to file a question on Yesanio's GitHub page.

You're not stupid if you find any of this confusing. The first time anyone does this, it feels strange. The second time it's routine.

---

## What we'll do, in plain language

1. Install **Docker Desktop** — a free piece of software from a company called Docker, Inc. Think of it as a translator that lets your computer run Yesanio's three pieces.
2. Download Yesanio itself — a single zip file from the Yesanio website on GitHub.
3. Open a **terminal** — a window where you type commands instead of clicking buttons. Less scary than it sounds.
4. Type two short commands. One starts Yesanio. One waits.
5. Open Yesanio in your web browser at a special address: `http://localhost:6210`
6. Follow the welcome wizard inside Yesanio to set up your name, currency, and first month's plan.

That's it. The hard part is steps 1 and 2 the first time. After that you have Yesanio forever.

---

## Pick your platform

Click the heading that matches your computer:

- [Windows 10 or Windows 11](#windows-10-or-windows-11)
- [Mac (macOS)](#mac-macos)
- [Linux (Ubuntu, Debian, Fedora, Mint, etc.)](#linux)
- [Chromebook (ChromeOS)](#chromebook)

Then continue from [Opening Yesanio for the first time](#opening-yesanio-for-the-first-time).

---

## Windows 10 or Windows 11

### Before you start: check your Windows version

Yesanio works on Windows 10 (64-bit, version 1903 or newer) and Windows 11. To check yours:

1. Press the **Windows key** on your keyboard, type "About your PC", and press Enter.
2. Scroll down to find **Edition** and **Version**. You want Windows 10 (any modern edition) or Windows 11.

If you have an older version of Windows (8, 7, or earlier), Docker Desktop won't install on your machine. You'd need to upgrade Windows first, which is a bigger project than this guide covers.

> **[Screenshot: the Windows "About" page showing Edition and Version highlighted]**

### Step 1 — Install Docker Desktop

1. In your web browser, go to: **https://www.docker.com/products/docker-desktop/**
2. Click the big **Download for Windows** button. A file called something like `Docker Desktop Installer.exe` will start downloading. It's about 700 MB, which can take a few minutes.

> **[Screenshot: the Docker.com download page with the Windows download button highlighted]**

3. When the download finishes, double-click the installer file (you'll find it in your Downloads folder).
4. The installer will ask permission to make changes to your computer — click **Yes**.
5. The Docker Desktop setup window appears. **Leave both checkboxes ticked** (one is about WSL 2, the other is about a desktop shortcut). Click **OK**.

> **[Screenshot: the Docker Desktop installer's initial configuration screen]**

6. Docker installs itself. This takes a few minutes. When it's done, it will say *"Installation succeeded"*. Click **Close**.

> **Inline help — if you see "WSL 2 installation is incomplete":** This means a feature called WSL2 isn't enabled on your Windows. Don't panic. Docker shows a link to the Microsoft instructions to enable it. The short version: open PowerShell as administrator (right-click the Start button, choose "Windows PowerShell (Admin)"), type `wsl --install`, press Enter, and restart your computer. Then re-run the Docker installer.

7. After installing, you may need to log out of Windows and back in (Windows will tell you if so).
8. Find Docker Desktop in your Start menu and open it.
9. The first time you open Docker Desktop, it shows a welcome screen and asks you to accept its licence terms. Read them, accept them. It may also ask you to sign in or create a Docker account — **you can skip this**. Click "Continue without signing in" or similar.

> **[Screenshot: Docker Desktop's first-launch welcome screen with the "Continue without signing in" option highlighted]**

10. Docker Desktop's main window opens. It shows a dashboard with various sections (Containers, Images, Volumes). You don't need to understand any of it. The important thing is: **Docker is now running in the background.** Look at your Windows system tray (the bottom-right corner of your screen, near the clock) — you should see a small whale icon. As long as that whale is there, Docker is alive.

> **Inline help — if Docker says "Docker Desktop starting…" forever:** This usually means a Windows feature called Hyper-V or Virtualisation isn't enabled in your computer's BIOS settings. This is a deeper change and varies by computer manufacturer. The honest advice here is to search the web for "enable virtualisation [your laptop model]" or ask a more technical friend. Once virtualisation is on, Docker starts in seconds.

### Step 2 — Download Yesanio

1. In your web browser, go to: **https://github.com/jc-universe87/yesanio/releases/latest**
2. Scroll down on that page to find a section called **Assets**.
3. Click on the file ending in `.zip` (it'll be named something like `yesanio-v2.5.7.zip`). It downloads to your Downloads folder.

> **[Screenshot: the GitHub Releases page with the zip file under "Assets" highlighted]**

4. Open your Downloads folder. Right-click the zip file and choose **Extract All...**. Choose where to extract — somewhere easy to find like your Desktop is fine. Click Extract.
5. A new folder called `yesanio` appears in the place you chose. Open it. You should see files including `docker-compose.yml`, `README.md`, and folders called `backend`, `frontend`, `docs`.

> **[Screenshot: Windows File Explorer showing the extracted yesanio folder with its contents visible]**

### Step 3 — Open a terminal in the yesanio folder

A "terminal" is a window where you type commands instead of clicking. Don't be intimidated — you're going to type two commands and that's it.

1. In File Explorer, navigate **into** the `yesanio` folder.
2. Click on the address bar at the top of the window (where it shows the path like `Desktop > yesanio`). It will turn into a text box.
3. Delete what's there, type **`powershell`**, and press Enter.
4. A blue or black window opens with text like `PS C:\Users\YourName\Desktop\yesanio>` followed by a blinking cursor. **This is the terminal.** It's already pointing at your yesanio folder, which is exactly what you want.

> **[Screenshot: a PowerShell window open at the yesanio folder location, ready for input]**

> **Inline help — if "powershell" doesn't work:** Some Windows versions need you to type `pwsh` instead. If neither works, hold Shift and right-click anywhere inside the yesanio folder (in empty space, not on a file), and choose **Open PowerShell window here** or **Open in Terminal**.

### Step 4 — Start Yesanio

In the terminal window, type this command exactly and press Enter:

```
docker compose up -d
```

(That's `docker`, then a space, then `compose`, then a space, then `up`, then a space, then `-d`.)

You'll see lines of text scrolling by — Docker is downloading Yesanio's three components from the internet (this takes 2-5 minutes the first time, depending on your internet speed) and then starting them. When it's done, you'll see something like:

```
[+] Running 4/4
 ✔ Network yesanio_default     Created
 ✔ Container yesanio-db        Started
 ✔ Container yesanio-backend   Started
 ✔ Container yesanio-frontend  Started
```

If you see all four green ticks, **Yesanio is now running**. Continue to [Opening Yesanio for the first time](#opening-yesanio-for-the-first-time).

> **Inline help — if you see "docker: command not found" or similar:** Docker Desktop isn't running. Open it from the Start menu, wait for the whale icon to settle in your system tray, then try the command again.

> **Inline help — if you see "port is already allocated":** Something else on your computer is using port 6210 or 6211. Most likely a previous attempt or another self-hosted tool. Skip ahead to the [Troubleshooting section](#when-something-goes-wrong) for the fix.

---

## Mac (macOS)

### Before you start

Yesanio works on macOS 11 (Big Sur) or newer. To check your version: click the Apple logo (top-left of your screen) → **About This Mac**. The version number is shown there. If yours is older, you'll need to update macOS first.

Both Apple Silicon Macs (M1/M2/M3) and Intel Macs work fine.

### Step 1 — Install Docker Desktop

1. In Safari, go to: **https://www.docker.com/products/docker-desktop/**
2. Click **Download for Mac**. The page asks whether you have an Apple chip (M1, M2, M3) or an Intel chip. To check yours: Apple logo → About This Mac → look at "Chip" or "Processor". Pick the matching button.
3. A file called `Docker.dmg` downloads (about 600 MB).

> **[Screenshot: the Docker.com Mac download page with the Apple Silicon and Intel options visible]**

4. Open Downloads, double-click `Docker.dmg`. A window opens showing the Docker icon and an Applications folder shortcut.
5. **Drag the Docker icon onto the Applications folder.** This installs it.

> **[Screenshot: the Docker DMG window with the drag-to-Applications instruction visible]**

6. Open your Applications folder, find **Docker**, and double-click it.
7. macOS will warn you: *"Docker is an application downloaded from the Internet. Are you sure you want to open it?"* Click **Open**.
8. Docker asks for your password to install some helper tools — type your Mac login password and click OK.
9. The first launch shows a welcome screen and asks you to accept the licence. Accept it. You can **skip the sign-in step** — click "Continue without signing in".

10. After a moment, Docker Desktop's main dashboard appears, and a small **whale icon** appears in your menu bar at the top-right of your screen. As long as that whale is there, Docker is running.

> **[Screenshot: macOS menu bar showing the Docker whale icon highlighted]**

> **Inline help — if Docker won't start:** macOS sometimes blocks Docker from running on first launch. Open System Settings → Privacy & Security, scroll to the "Security" section, and look for a message about Docker being blocked. Click **Allow** next to it.

### Step 2 — Download Yesanio

1. In Safari, go to: **https://github.com/jc-universe87/yesanio/releases/latest**
2. Scroll to the **Assets** section and click the `.zip` file.
3. The zip downloads to your Downloads folder. **Double-click it** — macOS automatically extracts it into a folder called `yesanio` next to the zip.

### Step 3 — Open a terminal in the yesanio folder

1. Open the **Terminal** app — press Cmd+Space (Spotlight search), type "terminal", press Enter.
2. Type this and press Enter (replacing `~/Downloads/yesanio` with the actual location if you extracted it elsewhere):

```
cd ~/Downloads/yesanio
```

> **Easier alternative:** in Terminal, type `cd ` (the letters c-d followed by a space), then drag the `yesanio` folder from Finder onto the Terminal window. Terminal automatically pastes the correct path. Press Enter.

3. The terminal prompt now ends with `yesanio %`, meaning you're "inside" the folder. 

### Step 4 — Start Yesanio

Type this command exactly and press Enter:

```
docker compose up -d
```

You'll see Docker downloading and starting components. After 2-5 minutes (first run), you should see four green ticks. Yesanio is now running. Continue to [Opening Yesanio for the first time](#opening-yesanio-for-the-first-time).

---

## Linux

This section is brief because most Linux users will already be comfortable with these steps. If you're on Linux and *not* comfortable with these steps, the same patience applies as elsewhere — read the Windows or Mac section above for the same flow conceptually.

### Step 1 — Install Docker

The right command depends on your distribution.

**Ubuntu / Debian / Mint:**
```
sudo apt update
sudo apt install -y docker.io docker-compose
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
```
Then log out and back in completely (not just close the terminal — fully sign out), so the group change takes effect.

> **A note on the package names:** Debian and Ubuntu ship `docker.io` (the daemon) and `docker-compose` (with a hyphen — the older command syntax). Yesanio works with both `docker compose` (with a space, modern) and `docker-compose` (with a hyphen, older), so use whichever your distro provides.

**Fedora:**
```
sudo dnf install -y docker docker-compose-plugin
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
```

**Arch:**
```
sudo pacman -S docker docker-compose
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
```

For other distributions, the official Docker install instructions at https://docs.docker.com/engine/install/ are reliable.

### Step 2 — Download Yesanio

```
cd ~
# Visit https://github.com/jc-universe87/yesanio/releases/latest in your browser to find the
# current version's filename, then download it. Example for v2.5.14:
wget https://github.com/jc-universe87/yesanio/releases/download/v2.5.14/yesanio-v2.5.14.zip
unzip yesanio-v2.5.14.zip
cd yesanio
```

(Replace `v2.5.7` with the actual current version if it's changed.)

### Step 3 — Start Yesanio

```
docker compose up -d
```

(On older Linux installs, use `docker-compose up -d` with a hyphen instead. Both work with Yesanio.)

Continue to [Opening Yesanio for the first time](#opening-yesanio-for-the-first-time).

---

## Chromebook

ChromeOS doesn't run Docker directly — it runs Docker inside a small Linux environment that ChromeOS provides. This works on most modern Chromebooks but not all. Let's check first.

### Before you start: is your Chromebook compatible?

1. Click the time in the bottom-right corner of your screen → click the gear icon (Settings).
2. In the search bar at the top, type **"Linux"**.
3. If you see a section called **"Linux development environment"** or **"Linux (Beta)"**, your Chromebook supports it. Continue.
4. If you don't see that section, your Chromebook either doesn't support Linux (older models, school-managed devices) or has it disabled by your administrator. You won't be able to install Yesanio on this device. Sorry — this isn't a writing problem; it's a hardware limit.

> **Performance note:** Yesanio runs three small servers inside Linux inside ChromeOS. Chromebooks with 4 GB of RAM will work but feel sluggish. 8 GB or more is much more comfortable.

### Step 1 — Enable Linux on your Chromebook

1. Settings → Linux development environment → click **Turn on**.
2. ChromeOS asks how much disk space to give Linux. The default (about 10 GB) is plenty for Yesanio. Click **Install**.
3. ChromeOS downloads the Linux environment and sets it up. This takes a few minutes.
4. When done, a black terminal window opens automatically. **This is the Linux terminal.** From now on, you'll type commands here.

### Step 2 — Install Docker inside Linux

In that Linux terminal, type these commands one at a time, pressing Enter after each, and waiting for each to finish before typing the next:

```
sudo apt update
sudo apt install -y docker.io docker-compose
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
```

(Note: it's `docker-compose` with a hyphen on Debian-based systems including Chromebook's Linux. Some online tutorials show `docker-compose-plugin` — that's a different package name from Docker's own repository, which Chromebook's Linux doesn't use.)

When the last command finishes, **fully restart the Linux container** so the docker group permission takes effect. Right-click the terminal app icon in the launcher → **Shut down Linux**. Wait a few seconds, then reopen the terminal app. (Just closing and reopening the terminal window isn't enough on Chromebook — the whole Linux environment needs to restart for the group change to apply.)

### Step 3 — Download Yesanio

In the Linux terminal:

```
cd ~
# Visit https://github.com/jc-universe87/yesanio/releases/latest in your browser to find the
# current version's filename, then download it. Example for v2.5.14:
wget https://github.com/jc-universe87/yesanio/releases/download/v2.5.14/yesanio-v2.5.14.zip
unzip yesanio-v2.5.14.zip
cd yesanio
```

### Step 4 — Start Yesanio

```
docker-compose up -d
```

(That's `docker-compose` with a hyphen, since Chromebook uses Debian's older Docker package. On Windows and Mac, the Docker Desktop install includes the newer `docker compose` with a space — both work the same way.)

Continue to [Opening Yesanio for the first time](#opening-yesanio-for-the-first-time).

> **Chromebook-specific note for opening Yesanio:** Recent ChromeOS versions automatically forward `localhost` from Linux to ChromeOS, so `http://localhost:6210` works in your normal Chrome browser. If it doesn't, try `http://penguin.linux.test:6210` instead — that's the ChromeOS-specific name for the Linux environment.

---

## Opening Yesanio for the first time

After `docker compose up -d` finishes successfully on any platform:

1. Wait about 10 seconds. (The database needs a moment to set itself up the first time.)
2. Open your normal web browser (Chrome, Firefox, Safari, Edge — any of them).
3. In the address bar, type: **`http://localhost:6210`** (and press Enter).

> **[Screenshot: Yesanio's welcome wizard in a browser, showing the first step "Welcome to Yesanio"]**

You should see Yesanio's welcome wizard. From here, the in-app guide takes over. The wizard walks you through:

1. A short introduction to what Yesanio is and the "pay yourself first" principle
2. Setting your name (shown on the Home page as "handled by [your name]")
3. Choosing your currency
4. Building your first plan (start from a template, or start blank)

After the wizard, you land on the Plan view. Build your first month's budget. Click **Save** when you're done. Then click **Home** in the top menu to see your household-facing summary.

That's it. **You've installed Yesanio.**

---

## Setting it up properly for your household

A few small but important things to do soon after installing.

### Change the default database passwords ⚠️

**Read this section even if you're only running Yesanio at home.** Yesanio ships with placeholder passwords deliberately named `yesanio_root_change_me` and `yesanio_app_change_me` — a self-documenting prompt that they should be changed.

For a Yesanio installation that only your family will ever use on your home network (and only you have access to the computer running it), the placeholders are acceptable. For anything broader — exposing Yesanio over Tailscale, sharing your home network with houseguests, running it on a small server you also use for other things — change them before saving any data.

To change them: in your `yesanio` folder, open `docker-compose.yml` in any text editor (Notepad on Windows, TextEdit on Mac, gedit on Linux). Search for the lines containing `_change_me` and replace those with passwords of your own choosing. Then in your terminal, in the yesanio folder:

```
docker compose down
docker compose up -d
```

> **Important:** if you've already created plans and goals, changing the database passwords does NOT delete your data — the database volume is preserved. But the *first* time you change the passwords (right after install, before saving anything), it's a much easier moment to do it.

### Make a backup

Yesanio includes a backup script. Run it occasionally — or better, schedule it to run automatically every night. To run it once:

```
bash backup.sh
```

A timestamped database dump appears in a `backups/` folder. Copy that file somewhere outside the Yesanio folder (a USB drive, a cloud storage folder, an external hard drive) for true peace of mind. **If you ever update Yesanio by deleting the folder and unzipping a new version, copy your backups out first** — they live inside the folder.

### Restoring from a backup

If something goes wrong and you need to restore from a backup file:

```
bash restore.sh ./backups/yesanio-backup-YYYY-MM-DD-HHMMSS.sql
```

(Replace the date in the filename with whichever backup you want to restore from.) The script prompts you to type "restore" to confirm — this is intentional, because restoring **replaces** all current data with whatever was in the backup. Once it finishes, restart Yesanio:

```
docker compose restart yesanio-backend
```

Open `http://localhost:6210` in your browser. Your data is back.

### How to keep Yesanio running

As long as Docker Desktop (Windows/Mac/Chromebook) is running, Yesanio runs in the background. You don't need to "open" Yesanio — just point your browser at `http://localhost:6210` whenever you want to use it.

If you restart your computer, Docker Desktop usually starts automatically with it, and Yesanio comes back automatically too. If you ever want to stop Yesanio (free up memory), in the terminal in your yesanio folder:

```
docker compose down
```

To start it again later:

```
docker compose up -d
```

---

## How to update Yesanio when a new version is released

When a new version of Yesanio comes out, you'll want to update — for new features and bug fixes. Updating is safe: your data is in a separate Docker volume that survives updates.

The four-step update flow:

1. **Download the new version's zip** from the same place as before: https://github.com/jc-universe87/yesanio/releases/latest

2. **Stop the current Yesanio.** In a terminal in your existing yesanio folder:
   ```
   docker compose down
   ```

3. **Replace the files.** Delete (or rename, for safety) the existing `yesanio` folder, then extract the new zip in the same location. The new folder will have the same name.

4. **Start the new version.** In a terminal in the new folder:
   ```
   docker compose build --no-cache yesanio-backend
   docker compose up -d
   ```

Wait ~10 seconds. Open `http://localhost:6210` in your browser. The new version is running and your data is intact.

> **If you customised your `docker-compose.yml`** (e.g. changed default passwords, changed ports), back that file up before deleting the old folder and copy your changes into the new `docker-compose.yml` before the build/up step.

---

## When something goes wrong

Sorted by what you're seeing.

### "I can't reach localhost:6210 in my browser"

- **Wait 30 more seconds.** First-time database setup can be slow.
- **Check Docker is running.** Look for the whale icon in your system tray (Windows) or menu bar (Mac). If it's not there, open Docker Desktop from your Start menu / Applications.
- **Check the containers actually started.** In the yesanio terminal, type `docker compose ps`. You should see three containers (yesanio-db, yesanio-backend, yesanio-frontend) all with status "Up" or "running". If any are missing or restarting, type `docker compose logs` and read the last few screens of output for clues.

### "Port is already allocated" when running `docker compose up`

Something else on your computer is using port 6210 or 6211. Either close the other thing, or change Yesanio's ports. To change ports: open `docker-compose.yml` in a text editor, find the lines like `"6210:6210"` and change the first number (the part *before* the colon) to something free, e.g. `"7210:6210"`. Then `docker compose up -d`. You'd then open `http://localhost:7210` instead.

### "WSL 2 installation is incomplete" (Windows)

This means a Windows feature called WSL2 isn't installed. Open PowerShell as administrator (right-click Start → "Windows PowerShell (Admin)"), type `wsl --install`, press Enter, restart your computer when prompted. Then re-run the Docker installer.

### "Docker Desktop is starting…" forever (Windows)

Usually means hardware virtualisation isn't enabled in your computer's BIOS. The fix varies by manufacturer — search the web for "enable virtualisation [your laptop model]" or ask a more technical friend. The change is in BIOS, not Windows, so you'll restart your computer and press a key like F2 or Delete during boot to enter the BIOS menu. The setting is usually called "Intel VT-x", "AMD-V", or "Virtualisation Technology". Enable it, save, exit. Docker should start in seconds after.

### "Permission denied" when running docker (Linux)

You haven't logged out and back in since adding yourself to the `docker` group. Log out completely (not just close the terminal — fully sign out and back in), or restart your computer. Then `docker compose up -d` will work without sudo.

### Yesanio loads but the page is broken or shows JavaScript errors

Hard-refresh the browser: **Ctrl+Shift+R** on Windows/Linux, **Cmd+Shift+R** on Mac. If that doesn't fix it, try the page in an incognito/private window to rule out browser extensions.

### My data disappeared after an update

It hasn't, almost certainly. The data is in a Docker volume called `yesanio_db_data` that persists across updates. Common cause of "my data disappeared" is connecting to a fresh install at a different port number by mistake, or having two yesanio folders and starting the wrong one. Verify with `docker volume ls` — you should see `yesanio_db_data` listed.

If you really did lose data and you have a backup file from `backup.sh`, restoring it requires a database command. This is the moment to ask for help on GitHub — restoration involves a single command but it's worth getting right rather than guessing.

### Anything not on this list

Open https://github.com/jc-universe87/yesanio/issues and click **New issue**. In the issue, please include:

1. What you were trying to do
2. What you typed
3. What happened (the exact error message — copy-paste it, don't paraphrase)
4. Your operating system and version
5. The output of `docker compose ps` and `docker compose logs --tail=30`

The more specific you are, the more likely you are to get a fast helpful answer.

---

## You did it

If you got Yesanio running and your first plan saved, you've done something most people would say was "too technical for me". You followed instructions, you installed software, you used a terminal, and you have a working self-hosted budgeting tool to show for it. That's a real accomplishment.

The rest is using Yesanio for what it's for: planning your household's money carefully, month by month, with the boring bills handled and the important things you're saving for set aside on day one.

Welcome.
