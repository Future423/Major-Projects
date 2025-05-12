# bridge.py
import otp 
import mysql.connector

global db_config

db_config = {
    "host": "sql12.freesqldatabase.com",  
    "user": "Enter your user",  
    "password": "Enter your password",  
    "database": "Enter your database",  
    "port": 3306  
} 
#access "https://github.com/Future423/Major-Projects/blob/main/PG_Hive/user_password_database.md" for knowing
#How to Get `user`, `password`, and `database` from freesqldatabase.com

# === OTP-related bridges ===
def send_otp_bridge(user_email):
    otp_code = otp.generate_and_send_otp(user_email)
    return otp_code  # return the generated OTP back to UI

def verify_otp_bridge(user_input_otp, real_otp):
    return user_input_otp == real_otp

# === Database status bridge ===
def check_database_status():

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        # If connected successfully
        cursor.close()
        conn.close()
        return "online"
    except mysql.connector.Error:
        return "offline"

def search_pg_bridge(state, city):

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM pg_list 
            WHERE state=%s AND city=%s 
            ORDER BY rent ASC
        """, (state, city))
        results = cursor.fetchall()
        cursor.close()
        conn.close()

        return results

    except mysql.connector.Error:
        return []

def login_bridge(username, password):
    global user_id
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE name=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        if user:
            user_id=user[0]
        else: 
            return None
        cursor.close()
        conn.close()

        return user  
    except mysql.connector.Error:
        return None

def register_user_bridge(username, email, password):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("INSERT INTO users (name, password, email) VALUES (%s, %s, %s)", 
                       (username, password, email)) 
        conn.commit()

        cursor.close()
        conn.close()
        return True
    except mysql.connector.Error:
        return False

def get_pgs_by_owner_bridge(user_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM pg_list WHERE user_id=%s
        """, (user_id,))
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    except mysql.connector.Error:
        return []

def delete_pg_bridge(pg_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM pg_list WHERE id = %s", (pg_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except mysql.connector.Error:
        return False

def update_pg_bridge(pg_id, updates: dict):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        set_clause = ', '.join([f"{column}=%s" for column in updates.keys()])
        values = list(updates.values())
        values.append(pg_id)

        sql = f"UPDATE pg_list SET {set_clause} WHERE id=%s"
        cursor.execute(sql, values)
        conn.commit()

        cursor.close()
        conn.close()
        return True
    except mysql.connector.Error:
        return False

def update_pg_in_db(pg_id, form_data):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    data = [
        form_data.get("Address", ""),    
        form_data.get("Rooms", ""),      
        form_data.get("Locality", ""),   
        "yes" if form_data.get("Nearby Market/grocery store", False) else "no",  
        form_data.get("Rent", ""),       
        form_data.get("Ac/cooler", ""),  
        form_data.get("Furniture", ""),  
        form_data.get("Category", ""),   
        form_data.get("Floor", ""),      
        form_data.get("Timing", ""),     
        form_data.get("Duration", ""),   
        form_data.get("Name", ""),       
        form_data.get("Contact No", ""), 
        form_data.get("State", ""),      
        form_data.get("City", ""), 
    ]

    cursor.execute("""
        UPDATE pg_list 
        SET address=%s, rooms=%s, locality=%s, market=%s, rent=%s, ac_cooler=%s, furniture=%s, category=%s, floor=%s, timing=%s, duration=%s, name=%s, contact=%s, state=%s, city=%s 
        WHERE id = %s
    """, (*data, pg_id))

    conn.commit()
    conn.close()


def add_pg_in_db(form_data):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    data = [
        form_data.get("Address", ""),           
        form_data.get("Rooms", ""),             
        form_data.get("Locality", ""),           
        "yes" if form_data.get("Nearby Market/grocery store", False) else "no", 
        form_data.get("Rent", ""),             
        form_data.get("Ac/cooler", ""),       
        form_data.get("Furniture", ""),         
        form_data.get("Category", ""),         
        form_data.get("Floor", ""),            
        form_data.get("Timing", ""),         
        form_data.get("Duration", ""),         
        form_data.get("Name", ""),              
        form_data.get("Contact No", ""),      
        form_data.get("State", ""),              
        form_data.get("City", ""),             
    ]

    # Insert into pg_list
    cursor.execute("""
        INSERT INTO pg_list (user_id, address, rooms, locality, market, rent, ac_cooler, furniture, category, floor, timing, duration, name, contact, state, city) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (user_id, *data))

    conn.commit()
    conn.close()
