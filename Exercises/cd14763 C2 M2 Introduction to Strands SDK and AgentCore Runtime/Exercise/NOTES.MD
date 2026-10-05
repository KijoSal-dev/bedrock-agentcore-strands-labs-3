# AgentCore — Test Locally, Then Deploy

 ## Project Overview

 **Purpose:** Test the AgentCore application locally first, then deploy it when local testing is successful.

 The recommended workflow is:

 1. Install dependencies
2. Configure AgentCore
3. Run the application locally
4. Verify that it works
5. Deploy to AWS only after local testing is successful

---

 # Step 1 — Install Dependencies

 ## Command

```
pip install -r requirements.txt
```

 ## Purpose

 Installs the Python packages required by the project.

 ## Status

 - [ ] Dependencies installed successfully

 ## Notes

 If installation fails, check:

 - Python version
- Active virtual environment
- `requirements.txt`
- pip error messages

---

 # Step 2 — Configure AgentCore

 ## Command

```
agentcore configure
```

 ## Purpose

 Creates/configures the AgentCore project so that it can be run locally and later deployed.

 ## Status

 - [ ] AgentCore configuration completed

 ## Notes

 After configuration, check the project directory for the AgentCore configuration files created by the CLI.

---

 # Step 3 — Test the Application Locally

 ## Command

```
agentcore dev
```

 ## Purpose

 Runs the AgentCore application locally using the container environment.

 The local development environment allows the application to be tested on the laptop before deploying resources to AWS.

 ## Important

 `agentcore dev` does **not** require deployment to AWS.

 It runs the container locally and follows the same application code path intended for production.

 ## Status

 - [ ] Local AgentCore server started
- [ ] Application tested successfully
- [ ] No blocking errors observed

---

 # Local Testing Checklist

 Before deploying, verify:

 - [ ] Dependencies installed
- [ ] AgentCore configured
- [ ] `agentcore dev` starts successfully
- [ ] Application responds as expected
- [ ] No configuration errors
- [ ] No dependency errors
- [ ] No runtime errors
- [ ] Local testing completed successfully

---

 # Step 4 — Deploy

 ## Deployment

 Only deploy after local testing has been completed successfully.

 The deployment command should be run according to the deployment instructions provided by the project/course.

 ### Status

 - [ ] Local testing completed
- [ ] Deployment command identified
- [ ] Deployment completed

 ### Deployment Notes

 Record the deployment command and result here:

```
Deployment command:

_Result:_

_Notes:_
```

---

 # Commands Used

 ## Install dependencies

```
pip install -r requirements.txt
```

 ## Configure AgentCore

```
agentcore configure
```

 ## Run locally

```
agentcore dev
```

---

 # Key Learning

 ## Local Development

 `agentcore dev` allows the AgentCore application to run locally on the laptop.

 This means the application can be tested without deploying it to AWS first.

 ## Container-Based Testing

 The application runs in a container locally, helping provide a development environment that follows the same code path intended for production.

 ## Recommended Workflow

 The workflow for this project is:

```
Install dependencies
        ↓
Configure AgentCore
        ↓
Run locally with agentcore dev
        ↓
Test and fix issues
        ↓
Confirm everything works
        ↓
Deploy
```

---

 # Troubleshooting Log

 Use this section to document any problems encountered.

 ## Issue 1

 **Problem:**

 _Add problem here._

 **Command:**

```
_Add command here._
```

 **Error:**

```
_Add error message here._
```

 **Solution:**

 _Add solution here._

 **Result:**

 _Add result here._

---

 ## Issue 2

 **Problem:**

 _Add problem here._

 **Error:**

```
_Add error message here._
```

 **Solution:**

 _Add solution here._

 **Result:**

 _Add result here._

---

 # Progress Log

 ## Date: 2026-09-09

 ### Completed

 - [ ] Installed project dependencies
- [ ] Configured AgentCore
- [ ] Started local development environment
- [ ] Tested application locally
- [ ] Fixed any local issues
- [ ] Deployed application

 ### Notes

 _Add observations, errors, solutions, or important lessons here._

---

 # Project Status

 **Current status:** 🟡 In Progress

 **Testing approach:** Local container testing first

 **Local command:** `agentcore dev`

 **Deployment:** ⏳ Pending successful local testing

---

 # Future Updates

 Continue updating this file whenever work is done on the project.

 For each new step, record:

 - Date
- Command used
- Purpose of the command
- Expected result
- Actual result
- Errors encountered
- Solution
- Important lessons learned
- Deployment status

