# WanderBot – Assignment Notes

 ## Assignment

 **Local Testing – WanderBot**

 **Module:** Implementing Structured Outputs with Strands and AgentCore

---

 ## 1\. Navigate to the Exercise Folder

 ### Command

```
cd "C:\Users\hp\Data Science and AI\AWS agentic engineer\work\Exercises\cd14763 C2 M4 Implementing Structured Outputs with Strands and AgentCore\Exercise"
```

 ### Status

 - [x] Exercise folder opened
- [x] Working directory verified

---

 ## 2\. Install Dependencies

 ### Command

```
pip install -r requirements.txt
```

 ### Status

 - [x] Dependencies installed

 ### Purpose

 Installs all Python packages required for the WanderBot exercise.

---

 ## 3\. Test Pydantic Hotel Validation

 ### Command

```
python -c "from starter import search_hotels; print(search_hotels('Barcelona', 200))"
```

 ### Purpose

 Tests the `search_hotels` function directly.

 This verifies that:

 - Hotel data is returned.
- Pydantic validates the hotel records.
- Invalid hotel records are skipped.
- The budget filter works correctly.

 ### Status

 - [x] Pydantic hotel validation tested

---

 ## 4\. Verify the Result

 ### Expected Result

```
Barceloneta Beach Hotel — $149/night
```

 Invalid hotel records should be skipped with Pydantic validation warnings.

 Expected total:

```
Total valid hotels: 1
```

 ### Verification

 - [x] Barceloneta Beach Hotel returned
- [x] Price is $149/night
- [x] Invalid hotel records skipped
- [x] Pydantic validation warnings observed
- [x] Total valid hotels = 1

---

 ## 5\. Run the AgentCore App Locally

 ### Command

```
python starter.py
```

 ### Status

 - [x] AgentCore application run locally

 ### Purpose

 Runs the WanderBot application locally so that the functionality can be tested without deploying it to AWS.

---

 ## 6\. AWS Deployment

 ### Command NOT Used

```
agentcore deploy
```

 ### Reason

 I did not use `agentcore deploy` because deployment creates resources in AWS and may incur AWS costs.

 For this assignment, local testing was sufficient.

 ### Status

 - [x] Local testing completed
- [x] AWS deployment intentionally skipped

---

 ## 7\. Overall Progress

 | Task | Status |
| --- | --- |
| Navigate to Exercise folder | ✅ Completed |
| Install dependencies | ✅ Completed |
| Test `search_hotels` | ✅ Completed |
| Test Pydantic validation | ✅ Completed |
| Verify hotel result | ✅ Completed |
| Run `starter.py` locally | ✅ Completed |
| Run `agentcore deploy` | ⏭️ Skipped intentionally |

---

 ## 8\. Key Learning

 ### Pydantic Validation

 Pydantic is used to validate structured hotel data and helps ensure that the returned data follows the expected schema.

 Invalid records can be identified and skipped instead of being passed through the application.

 ### Structured Outputs

 Structured outputs help ensure that application or agent responses follow a defined structure and schema.

 ### Local Testing

 Running the application locally is useful for development and testing before deploying resources to AWS.

 ### AWS Cost Awareness

 AWS deployment commands should be used carefully because they can create cloud resources and potentially generate charges.

 For development and testing, local execution can be used first when deployment is not required.

---

 ## 9\. Commands Used

 For quick reference:

```
cd "C:\Users\hp\Data Science and AI\AWS agentic engineer\work\Exercises\cd14763 C2 M4 Implementing Structured Outputs with Strands and AgentCore\Exercise"

pip install -r requirements.txt

python -c "from starter import search_hotels; print(search_hotels('Barcelona', 200))"

python starter.py
```

---

 ## 10\. Progress Log

 ### 2026-09-09

 #### Completed

 - [x] Navigated to the Exercise folder.
- [x] Installed the required dependencies.
- [x] Tested `search_hotels`.
- [x] Tested Pydantic hotel validation.
- [x] Verified the valid Barcelona hotel result.
- [x] Confirmed invalid hotel records are skipped.
- [x] Ran the AgentCore application locally.
- [x] Avoided AWS deployment to prevent unnecessary AWS resource usage and potential costs.

 #### Next Step

 Continue with the next task in the WanderBot assignment.

---

 ## 11\. Troubleshooting Log

 Use this section to record any errors and solutions encountered during the assignment.

 ### Issue

 **Problem:**

 _Add problem here._

 **Error message:**

```
_Add error message here._
```

 **Solution:**

 _Add solution here._

 **Result:**

 _Add result here._

---

 ## 12\. Future Notes

 Whenever I complete a new task, I will update this file with:

 - The date
- What I completed
- Commands used
- Expected result
- Actual result
- Errors encountered
- How the errors were fixed
- Important concepts learned
- Any AWS deployment decisions

 This file will serve as my documentation and progress tracker for the assignment.
