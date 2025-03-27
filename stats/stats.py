import time
import sys

def yellow(text):
    gradient_output = ""
    start_color = (255, 255, 0)
    end_color = (0, 255, 0)

    for i, char in enumerate(text):
        ratio = i / len(text)
        r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
        g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
        b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
        gradient_output += f"\033[38;2;{r};{g};{b}m{char}"

    return gradient_output + "\033[0m"

class stats:
    def __init__(self, total):
        self.total = total
        self.current = 0
        self.found = 0
        self.start_time = time.time()
        self.last_update = 0
        self.update_interval = 0.01  

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def update(self, n=1, found=0):
        self.current += n
        self.found += found
        current_time = time.time()
        
        if current_time - self.last_update < self.update_interval:
            return
            
        self.last_update = current_time
        elapsed = current_time - self.start_time
        percentage = int(self.current * 100 / self.total)
        print(f"\033[38;2;255;255;255mchecking \033[38;5;4m(\033[38;2;255;255;255m{self.current}/{self.total}\033[38;5;4m) \033[38;5;4m[\033[38;2;255;255;255m{percentage}%\033[38;5;4m] \033[38;5;4mat \033[38;2;255;255;255m{elapsed:.1f}s", end="\r")
        sys.stdout.flush()

    def close(self):
        print()
