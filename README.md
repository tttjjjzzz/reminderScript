# Email Reminder Script

A Python script that sends a reminder email via Gmail SMTP. Designed to run on a schedule using Windows Task Scheduler.

## Setup

### 1. Create a Gmail App Password

You need an App Password (not your regular Gmail password) to let the script send emails.

1. Go to [myaccount.google.com](https://myaccount.google.com)
2. **Security** > **2-Step Verification** — enable it if not already on
3. Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
4. Enter a name like `Reminder Script` and click **Create**
5. Copy the 16-character password (formatted as `xxxx xxxx xxxx xxxx`)

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy the example file and fill in your values:

```bash
cp .env.example .env
```

Edit `.env`:

| Variable | Description |
|---|---|
| `GMAIL_ADDRESS` | Your Gmail address (e.g. `you@gmail.com`) |
| `GMAIL_APP_PASSWORD` | The 16-character App Password from step 1 (spaces optional) |
| `RECIPIENT_EMAIL` | Email address to receive the reminder |
| `EMAIL_SUBJECT` | Subject line of the reminder email |
| `EMAIL_BODY` | Body text of the reminder email |

### 4. Test manually

```bash
python send_reminder.py
```

Check your inbox and `reminder.log` to confirm it worked.

## Windows Task Scheduler Setup

### Option A: GUI

1. Open Task Scheduler (`Win+R` > `taskschd.msc`)
2. Click **Create Task** in the right pane
3. **General tab**:
   - Name: `EmailReminder`
   - Select "Run whether user is logged on or not"
4. **Triggers tab** - click **New** for each time you want a reminder:
   - Set to "On a schedule" > Daily
   - Set your desired time (e.g. 10:00 AM)
   - Click OK, then repeat for additional times (e.g. 6:00 PM)
5. **Actions tab** - click **New**:
   - Action: Start a program
   - Program/script: full path to `python.exe` (run `where python` to find it)
   - Arguments: `send_reminder.py`
   - Start in: `C:\Users\Tiger\Documents\GitHub\reminderScript`
6. **Conditions tab**:
   - Uncheck "Start the task only if the computer is on AC power"
7. **Settings tab**:
   - Check "Allow task to be run on demand"
   - Set "If the task fails, restart every" to 5 minutes, up to 3 times
   - Set "Stop the task if it runs longer than" to 1 minute
8. Click OK and enter your Windows password when prompted

### Option B: PowerShell

```powershell
$action = New-ScheduledTaskAction `
    -Execute "C:\path\to\python.exe" `
    -Argument "send_reminder.py" `
    -WorkingDirectory "C:\Users\Tiger\Documents\GitHub\reminderScript"

$trigger1 = New-ScheduledTaskTrigger -Daily -At 10:00AM
$trigger2 = New-ScheduledTaskTrigger -Daily -At 6:00PM

$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 1) `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 5)

Register-ScheduledTask `
    -TaskName "EmailReminder" `
    -Action $action `
    -Trigger $trigger1, $trigger2 `
    -Settings $settings `
    -RunLevel Highest `
    -Description "Sends a reminder email via Gmail"
```

Replace `C:\path\to\python.exe` with the output of `where python`.

### Testing the scheduled task

1. Right-click the task in Task Scheduler > **Run**
2. Check `reminder.log` for output
3. "Last Run Result" should show `0x0` (success)

## Logs

The script writes to `reminder.log` in the project directory. Each run logs the timestamp, success/failure status, and any error details.
