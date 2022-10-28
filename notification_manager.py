import smtplib
import os
import encodings


class NotificationManager:
    def __init__(self):
        self.message = ""
        self.list_of_messages = []
        self.MY_EMAIL = "dev.dmytro.rudikov@gmail.com"
        self.MY_PASSWORD = os.getenv("EMAIL_PASSWORD")

    def create_msg(self, deals_found):
        for deal in deals_found:
            if len(deal) == 5:
                self.message = f"Subject:Low price alert!" \
                               f"\n\nOnly £{deal['price']} " \
                               f"to fly from {deal['fly_from']} " \
                               f"to {deal['fly_to']}, " \
                               f"from {deal['date_from']} " \
                               f"to {deal['date_to']}.".encode("utf-8")
            else:
                self.message = f"Subject:Low price alert!" \
                               f"\n\nOnly £{deal['price']} " \
                               f"to fly from {deal['fly_from']} " \
                               f"to {deal['fly_to']}, " \
                               f"from {deal['date_from']} " \
                               f"to {deal['date_to']}." \
                               f"\nFlight has {len(deal) - 5} stop over, via {deal['stop_over']} city.".encode("utf-8")
        self.list_of_messages.append(self.message)

    def send_msg(self, members):
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=self.MY_EMAIL, password=self.MY_PASSWORD)
            for message in self.list_of_messages:
                for member in members:
                    connection.sendmail(
                        from_addr=self.MY_EMAIL,
                        to_addrs=member["email"],
                        msg=message
                    )

