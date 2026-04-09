# Thoma's Webstore

**CS178: Cloud and Database Systems — Project #1**
**Author:** Aidan Thoma
**GitHub:** AidanThoma

---

## Overview
- This is user storage website which allows users to add to their list to see what they all have in their cart. This solves the problem of people having to keep track of what itmes blong to who and makes this process more easily scaleable.
---

## Technologies Used

- **Flask** — Python web framework
- **AWS EC2** — hosts the running Flask application
- **AWS RDS (MySQL)** — relational database for inventory and objects
- **AWS DynamoDB** — non-relational database for user accounts
- **GitHub Actions** — auto-deploys code from GitHub to EC2 on push

---

## Project Structure

```
ProjectOne/
├── flaskapp.py          # Main Flask application — routes and app logic
├── dbCode.py            # Database helper functions (MySQL connection + queries)
├── creds_sample.py      # Sample credentials file (see Credential Setup below)
├── templates/
│   ├── home.html        # Landing page
│   ├── [other].html     # Add descriptions for your other templates
├── .gitignore           # Excludes creds.py and other sensitive files
└── README.md
```

---

## How to Run Locally

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. Install dependencies:

   ```bash
   pip3 install flask pymysql boto3
   ```

3. Set up your credentials (see Credential Setup below)

4. Run the app:

   ```bash
   python3 flaskapp.py
   ```

5. Open your browser and go to `http://127.0.0.1:8080`

---

## How to Access in the Cloud

The app is deployed on an AWS EC2 instance. To view the live version:

```
http://107.22.149.216:8080
```

_(Note: the EC2 instance may not be running after project submission.)_

---

## Credential Setup

This project requires a `creds.py` file that is **not included in this repository** for security reasons.

Create a file called `creds.py` in the project root with the following format (see `creds_sample.py` for reference):

```python
# creds.py — do not commit this file
host = "your-rds-endpoint"
user = "admin"
password = "your-password"
db = "your-database-name"
```

---

## Database Design

### SQL (MySQL on RDS)

<!-- Briefly describe your relational database schema. What tables do you have? What are the key relationships? -->

**Example:**

- `Inventory` — stores [ttems descriptions and price]; primary key is `ID`
- `Category` — stores different categories; foreign key links to `Inventory`

The JOIN query used in this project: <!-- describe it in plain English -->

### DynamoDB

<!-- Describe your DynamoDB table. What is the partition key? What attributes does each item have? How does it connect to the rest of the app? -->

- **Table name:** `Users`
- **Partition key:** `uID`
- **Used to:** keep track of names, emails, and what users have in their cart

---

## CRUD Operations

| Operation | Route      | Description    |
| --------- | ---------- | -------------- |
| Create    | `/remove_item_from_user_in_dynamo` | removes an item from a users list |
| Read      | `/get_user_from_dynamo` | grabs information from a single user based off their uID |
| Update    | `/update_user_in_dynamo` | allows user to change their name and email, but NOT their uID |
| Delete    | `/remove_item_from_user_in_dynamo` | allows a user to remove an item from their list |

---

## Challenges and Insights

<!-- What was the hardest part? What did you learn? Any interesting design decisions? -->
The hardest part of this was definetly doing a qeury that involved both my RDS and DynamoDB. For this I grab the item ID from the DynamoDB and do a query on the RDS database to grab what that item is. Defiently would be easier and more effiecient if I just stored the data when I named it, but I'm lazy.
---

## AI Assistance

<!-- List any AI tools you used (e.g., ChatGPT) and briefly describe what you used them for. Per course policy, AI use is allowed but must be cited in code comments and noted here. -->
I used Google Gemini to help me a lot with the RDS and Dynamo query which I listed above. I also used it in some of my HTML pages for some simple debugging.