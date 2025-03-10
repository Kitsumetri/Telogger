from telogger import Telogger

def main():
    tlogger = Telogger(
        token="YOUR_BOT_TOKEN",
        chat_id="YOUR_CHAT_ID"
    )
    
    # Simple message sending
    tlogger.send_message("🔔 Basic usage test started!")
    
    # Send different message types
    tlogger.send_message("<b>HTML formatted message</b>")
    tlogger.send_message("*Markdown message*", parse_mode="MarkdownV2")

if __name__ == "__main__":
    main()