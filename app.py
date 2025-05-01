from instabot import Bot
import shutil
import threading

# Clean old sessions
shutil.rmtree("config", ignore_errors=True)

# Initialize bot
bot = Bot()
logged_in = False

def run_bot_action_in_main_thread(func, *args, **kwargs):
    """Wrapper to ensure bot actions run in the main thread."""
    thread = threading.Thread(target=func, args=args, kwargs=kwargs)
    thread.start()
    thread.join()  # Wait for the thread to finish

def login(username, password):
    global logged_in
    try:
        bot.login(username=username, password=password)
        logged_in = True
        print("✅ Logged in successfully!")
    except Exception as e:
        print(f"❌ Login failed: {e}")
        return False
    return True

def follow(username_to_follow):
    try:
        bot.follow(username_to_follow)
        print(f"➕ Followed {username_to_follow}")
    except Exception as e:
        print(f"❌ Failed to follow {username_to_follow}: {e}")

def like(username_to_like, count):
    try:
        media_ids = bot.get_user_medias(username_to_like)
        for media in media_ids[:count]:
            bot.like(media)
            post_url = f"https://www.instagram.com/p/{media}/"
            print(f"❤️ Liked a post from @{username_to_like}: {post_url}")
    except Exception as e:
        print(f"❌ Failed to like posts: {e}")

def comment(username_to_comment, text, count):
    try:
        media_ids = bot.get_user_medias(username_to_comment)
        for media in media_ids[:count]:
            bot.comment(media, text)
            post_url = f"https://www.instagram.com/p/{media}/"
            print(f"💬 Commented on a post from @{username_to_comment}: {post_url}")
    except Exception as e:
        print(f"❌ Failed to comment: {e}")

def dm(users, message):
    try:
        success = bot.send_message(message, [u.strip() for u in users])
        if success:
            print(f"📩 Message sent to {', '.join(users)}")
        else:
            print(f"❌ Message failed (maybe blocked or no prior chat)")
    except Exception as e:
        print(f"❌ Failed to send message: {e}")

# Main program loop
def main():
    global logged_in
    while True:
        if not logged_in:
            username = input("Enter Instagram username: ")
            password = input("Enter Instagram password: ")
            if not login(username, password):
                continue
        
        action = input("Enter action (follow/like/comment/dm): ").strip().lower()

        if action == "follow":
            user_to_follow = input("Enter username to follow: ")
            follow(user_to_follow)

        elif action == "like":
            username_to_like = input("Enter username to like posts: ")
            count = int(input("Enter number of posts to like: "))
            like(username_to_like, count)

        elif action == "comment":
            username_to_comment = input("Enter username to comment on posts: ")
            text = input("Enter comment text: ")
            count = int(input("Enter number of posts to comment on: "))
            comment(username_to_comment, text, count)

        elif action == "dm":
            users = input("Enter usernames to send DM (comma separated): ").split(",")
            message = input("Enter message to send: ")
            dm(users, message)

        else:
            print("❌ Invalid action. Please choose from follow, like, comment, or dm.")

if __name__ == "__main__":
    main()
