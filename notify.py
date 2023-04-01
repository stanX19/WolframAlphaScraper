from plyer import notification


def show_notification(message="", title="Notification"):
    notification.notify(
        title=title,
        message=message,
        timeout=0,
    )


def notify_when_done(total_loop, total_scrape, total_time):
    message = f"Total loop: {total_loop}\nTotal Successful Scrape: {total_scrape}\nTime used: {total_time}"
    show_notification(title="Scraping completed", message=message)


if __name__ == '__main__':
    show_notification("hello world!")
