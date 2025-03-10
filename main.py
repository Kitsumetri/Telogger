from src.telogger import Telogger, monitor
import time

tlogger = Telogger()

@monitor(
    name="MARKDOWN_TASK",
    parse_mode="MarkdownV2",
    telogger=tlogger
)
def markdown_task():
    time.sleep(1)
    print("Completed Markdown task")

@monitor(
    name="HTML_TASK",
    parse_mode="HTML",
    telogger=tlogger
)
def html_task():
    time.sleep(1)
    print("Completed HTML task")

def main():
    markdown_task()
    html_task()

if __name__ == "__main__":
    main()