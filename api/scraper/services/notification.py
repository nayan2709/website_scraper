class Notification:
    def __int__(self):
        pass

    @staticmethod
    def notify(message: dict):
        # todo can implement any other notification mechanism like email, sms, slack etc.
        #  for now we are just printing the message
        print(f"Notification to recipients: {message}")
