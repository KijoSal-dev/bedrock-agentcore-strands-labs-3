# WanderBot — Run Locally with AgentCore

 ## Project

 **Course/Module:** Building Agents with Bedrock AgentCore Function Calling\
 **Project:** WanderBot\
 **Purpose:** Configure and run the WanderBot AgentCore application locally on Windows using PowerShell.

 This file documents the setup, commands, results, troubleshooting, and important decisions made while working on this project.

---

 # Setup Checklist

 - [ ] Configure PATH for AgentCore CLI
- [ ] Navigate to the Exercise folder
- [ ] Verify AWS credentials
- [ ] Configure the AgentCore project
- [ ] Confirm `.bedrock_agentcore.yaml` was created
- [ ] Start the local AgentCore development server
- [ ] Test the locally running agent
- [ ] Record any errors and solutions

---

 # Step 1 — Fix PATH for AgentCore CLI

 ## Why?

 The AgentCore CLI was installed as a per-user Python package.

 Its `Scripts` directory therefore needs to be added to the PATH for the current PowerShell session so that commands such as `agentcore` can be recognized.

 ## Command

```
$env:Path += ";$env:APPDATA\Python\Python313\Scripts"
```

 ## Important

 This needs to be run **once in each new PowerShell window/session**.

 ## Status

 - [ ] PATH configured
- [ ] `agentcore` command recognized

 ## Verification

 Run:

```
agentcore --help
```

 If the command displays AgentCore CLI help, the PATH configuration is working.

---

 # Step 2 — Navigate to the Exercise Folder

 ## Command

```
cd "C:\Users\hp\Data Science and AI\AWS agentic engineer\work\Exercises\cd14763 C2 M2 Building Agents with Bedrock AgentCore Function Calling\Exercise"
```

 ## Purpose

 All AgentCore configuration commands should be executed from inside the Exercise folder.

 ## Verify Current Folder

```
pwd
```

 The path should point to:

```
C:\Users\hp\Data Science and AI\AWS agentic engineer\work\Exercises\cd14763 C2 M2 Building Agents with Bedrock AgentCore Function Calling\Exercise
```

 ## Status

 - [ ] Exercise folder opened
- [ ] Working directory verified

---

 # Step 3 — Verify AWS Credentials

 ## Why?

 This project uses AWS services through the course's Vocareum lab environment.

 The Vocareum credentials are temporary and may expire periodically.

 Before continuing, confirm that the current AWS credentials are still valid.

 ## Command

```
aws sts get-caller-identity
```

 ## Expected Result

 AWS should return information identifying the current AWS account/user/role.

 Example structure:

```
{
    "UserId": "...",
    "Account": "...",
    "Arn": "..."
}
```

 ## Status

 - [ ] AWS credentials verified
- [ ] `aws sts get-caller-identity` completed successfully

---

 # AWS Credential Troubleshooting

 If the following error appears:

```
InvalidClientTokenId
```

 the Vocareum lab credentials may have expired.

 ## Recovery Steps

 1. Go back to the course's Vocareum lab portal.
2. Obtain a fresh:
   - Access Key ID
   - Secret Access Key
   - Session Token
3. Update the AWS credentials file:

```
%USERPROFILE%\.aws\credentials
```

 4. Save the updated credentials.
5. Run the verification command again:

```
aws sts get-caller-identity
```

 Do not continue with AgentCore configuration until the AWS credentials are confirmed to be valid.

---

 # Step 4 — Configure the AgentCore Project

 ## Command

 Run this command from inside the Exercise folder:

```
agentcore configure -e starter.py -n WanderBot -dt container -rf requirements.txt --disable-memory --non-interactive
```

 ## What This Does

 This configures the WanderBot project for AgentCore.

 ### Parameters

 | Parameter | Meaning |
| --- | --- |
| `-e starter.py` | Specifies the application's entry point |
| `-n WanderBot` | Names the AgentCore application `WanderBot` |
| `-dt container` | Uses a container deployment/runtime configuration |
| `-rf requirements.txt` | Uses `requirements.txt` for Python dependencies |
| `--disable-memory` | Disables AgentCore memory for this exercise |
| `--non-interactive` | Runs configuration without interactive prompts |

 ## Expected Result

 The configuration should create:

```
.bedrock_agentcore.yaml
```

 inside the Exercise folder.

 ## Verify

 Run:

```
dir
```

 Look for:

```
.bedrock_agentcore.yaml
```

 ## Status

 - [ ] AgentCore project configured
- [ ] `.bedrock_agentcore.yaml` created
- [ ] Configuration completed successfully

---

 # Step 5 — Start the Local Development Server

 ## Command

```
agentcore dev
```

 ## Purpose

 Starts the AgentCore development environment locally.

 The terminal should remain open while the development server is running.

 ## Important

 **Do not close this PowerShell window.**

 The window is hosting the local agent.

---

 # Step 6 — Open a Second PowerShell Window

 Once:

```
agentcore dev
```

 is running successfully:

 1. Keep the first PowerShell window open.
2. Open a second PowerShell window.
3. Use the second window for subsequent commands/testing.

 The first terminal is the local AgentCore server.

 The second terminal is used to interact with or test the running application.

 ## Status

 - [ ] `agentcore dev` started successfully
- [ ] First PowerShell window left running
- [ ] Second PowerShell window opened

---

 # Current Project Structure

 The Exercise folder should contain files similar to:

```
Exercise/
│
├── starter.py
├── requirements.txt
├── .bedrock_agentcore.yaml
└── notes.md
```

 Additional files may be created by AgentCore during the development process.

---

 # Commands Used So Far

 ## PATH

```
$env:Path += ";$env:APPDATA\Python\Python313\Scripts"
```

 ## Navigate to Exercise

```
cd "C:\Users\hp\Data Science and AI\AWS agentic engineer\work\Exercises\cd14763 C2 M2 Building Agents with Bedrock AgentCore Function Calling\Exercise"
```

 ## Check AWS credentials

```
aws sts get-caller-identity
```

 ## Configure AgentCore

```
agentcore configure -e starter.py -n WanderBot -dt container -rf requirements.txt --disable-memory --non-interactive
```

 ## Start local development server

```
agentcore dev
```

---

 # Important Concepts Learned

 ## AgentCore CLI

 The AgentCore CLI provides commands for configuring and running AgentCore applications.

 ## Local Development

 `agentcore dev` allows the application to be developed and tested locally before considering deployment.

 ## AgentCore Configuration

 The `.bedrock_agentcore.yaml` file stores the configuration required by the AgentCore development environment.

 ## Entry Point

 The `starter.py` file is specified as the application entry point using:

```
-e starter.py
```

 ## Requirements

 The project's Python dependencies are supplied through:

```
requirements.txt
```

 ## Memory

 Memory is disabled for this exercise using:

```
--disable-memory
```

 ## AWS Credentials

 The Vocareum lab provides temporary AWS credentials. These credentials can expire, so AWS identity should be verified before troubleshooting AgentCore commands.

---

 # Troubleshooting Log

 Use this section whenever an error occurs.

 ## Issue 1 — AgentCore command not recognized

 ### Error

```
agentcore : The term 'agentcore' is not recognized...
```

 ### Possible Cause

 The AgentCore CLI Scripts directory is not on the current PowerShell PATH.

 ### Solution

 Run:

```
$env:Path += ";$env:APPDATA\Python\Python313\Scripts"
```

 Then verify:

```
agentcore --help
```

 ### Result

 _Add result here._

---

 ## Issue 2 — AWS InvalidClientTokenId

 ### Error

```
InvalidClientTokenId
```

 ### Possible Cause

 Vocareum AWS credentials have expired.

 ### Solution

 Refresh the credentials from the course lab portal and update:

```
%USERPROFILE%\.aws\credentials
```

 Then run:

```
aws sts get-caller-identity
```

 ### Result

 _Add result here._

---

 # Progress Log

 ## 2026-09-09

 ### Completed

 - [ ] Configured PowerShell PATH
- [ ] Navigated to the WanderBot Exercise folder
- [ ] Verified AWS credentials
- [ ] Configured AgentCore
- [ ] Created `.bedrock_agentcore.yaml`
- [ ] Started `agentcore dev`
- [ ] Opened second PowerShell window
- [ ] Tested the local WanderBot agent

 ### Notes

 _Add any observations or results here._

---

 # Next Steps

 Continue documenting the project here.

 For every new step, record:

 - The command used
- Why the command was used
- Expected result
- Actual result
- Whether the step succeeded
- Any errors encountered
- How the error was fixed
- Important concepts learned

---

 # Project Status

 **Current status:** 🟡 In Progress

 **Environment:** Windows / PowerShell

 **Agent:** WanderBot

 **Entry point:** `starter.py`

 **Runtime configuration:** Container

 **Memory:** Disabled

 **Dependencies:** `requirements.txt`

 **Local server:** `agentcore dev`

 **AWS deployment:** Not documented yet

---

 # Notes

 This `notes.md` file is the running documentation for the WanderBot project.

 The goal is to keep a clear record of what has been completed so that the project can be resumed later without having to remember every setup command or troubleshooting step.

