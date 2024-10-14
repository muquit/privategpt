import sys
import time
import threading

########################################################################
# A busy indicator with braille characters.
# Adapted from ollam golang source:
#  https://github.com/ollama/ollama/blob/main/progress/spinner.go
# muquit@muquit.com Oct-11-2024 
########################################################################


class BrailleSpinner:
    def __init__(self, message=""):
        self.parts = [
            "⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"
        ]
        self.message = message
        self.started = None
        self.running = False
        self.thread = None

    def set_message(self, message):
        self.message = message

    def start(self):
        self.running = True
        self.started = time.time()  # Reset the start time here
        self.thread = threading.Thread(target=self._spin)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        sys.stdout.write('\r' + ' ' * (len(self.message) + 2) + '\r')
        sys.stdout.flush()

    def _spin(self):
        while self.running:
            for part in self.parts:
                if not self.running:
                    break
                elapsed = time.time() - self.started
                minutes, seconds = divmod(int(elapsed), 60)
                time_str = f"{minutes:02d}:{seconds:02d}"
                output = f"\r{part} {self.message} {time_str}"
                sys.stdout.write(output)
                sys.stdout.flush()
                time.sleep(0.1)

def new_spinner(message=""):
    spinner = Spinner(message)
    spinner.start()
    return spinner
