from plyer import notification


def show_notification(message="", title="Notification"):
    notification.notify(
        title=title,
        message=message,
        timeout=0,
    )


def notify_when_done(total_loop, total_scrape, total_seconds):
    message = f"""Total loop: {total_loop}
Successful: {total_scrape}    -{round(total_scrape/total_loop*100, 1)}%-
Time used: {total_seconds}s"""
    show_notification(title="Scraping completed", message=message)

    print("___________________________")
    print(message)
    print("‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")


if __name__ == '__main__':
    message = f"""Total loop: 10
Successful: 8    -80.0%-
Time used: 90.56s"""
    show_notification(message)
