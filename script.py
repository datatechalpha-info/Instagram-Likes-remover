import pandas as pd
import requests
from time import sleep
import time
import os

# --- SETUP ---
SESSIONID = 'your_sessionid
CSRF_TOKEN = 'your_csrf'

headers = {
    'User-Agent': 'Mozilla/5.0',
    'X-CSRFToken': CSRF_TOKEN,
    'Referer': 'https://www.instagram.com/',
    'X-Requested-With': 'XMLHttpRequest'
}

cookies = {
    'sessionid': SESSIONID,
    'csrftoken': CSRF_TOKEN
}

def shortcode_to_id(shortcode):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
    id = 0
    for char in shortcode:
        id = id * 64 + alphabet.index(char)
    return str(id)

def unlike_post(post_id):
    url = f"https://www.instagram.com/web/likes/{post_id}/unlike/"
    response = requests.post(url, headers=headers, cookies=cookies)
    if response.status_code == 200:
        print(f"✅ Unliked post {post_id}")
    else:
        print(f"❌ Failed to unlike {post_id} - Status code: {response.status_code}")
        print(response.text)

# --- Load CSV ---
csv_path = 'likes/posts_links.csv'
df = pd.read_csv(csv_path)

# Ensure 'visited' column exists
if 'visited' not in df.columns:
    df['visited'] = ''

# --- Process Each Post ---
count = 0
new_links = []

for index, row in df.iterrows():
    ptime = time.time()
    link = row['links']
    try:
        count += 1
        print(f"URL - {link}")
        shortcode = link.strip('/').split('/')[-1]
        post_id = shortcode_to_id(shortcode)
        unlike_post(post_id)
        sleep(2)

        # Mark as visited
        df.at[index, 'visited'] = link

        print(f"Processed {count} posts.")
        ctime = time.time() - ptime
        print(f"Time taken {ctime:.2f}")

    except Exception as e:
        print(f"Error processing {link}: {e}")

# Remove processed links
df = df[df['visited'] == '']  # Keep only unvisited rows
df.to_csv(csv_path, index=False)
print(f"Processed {count} posts.")
