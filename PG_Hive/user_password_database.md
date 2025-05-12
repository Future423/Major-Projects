
# 🔧 How to Get `user`, `password`, and `database` from freesqldatabase.com

Follow these steps to set up your free SQL database and retrieve the required credentials for your project.

---

## 📌 Step 1: Create an Account

1. Go to [https://www.freesqldatabase.com](https://www.freesqldatabase.com)
2. Click on **"Get Your Free Database"**
3. Fill in the required information (Email, Name, etc.)
4. Click on **"Create Database"**
5. Verify your email if asked.

---

## 📌 Step 2: Access Your Database Details

1. Once your account is created, log in to your dashboard.
2. Under **My SQL Databases**, you will see a table with details like:
   - **Database Name**
   - **User Name**
   - **Password**
   - **Host Name**
   - **Port**

---

## 📌 Step 3: Use the Credentials in Your Code

Replace the placeholder values in your database config like this:

```json
{
  "host": "sql12.freesqldatabase.com",
  "user": "your_actual_user",
  "password": "your_actual_password",
  "database": "your_actual_database",
  "port": 3306
}
```

Make sure to keep your password safe and avoid uploading it publicly.

---

## ✅ Sample Output (After Filling In)

```json
{
  "host": "sql12.freesqldatabase.com",
  "user": "sql12653539",
  "password": "qwerty123",
  "database": "sql12653539",
  "port": 3306
}
```

> **Note:** Replace the values with your own credentials.
