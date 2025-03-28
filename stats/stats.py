import time
import sys
import threading

class stats:
    def __init__(self, total):
        self.total = total
        self.current = 0
        self.found = 0
        self.start_time = time.time()
        self.last_update = 0
        self.update_interval = 0.01
        self.dot_count = 0
        self.last_dot_time = 0
        self.dot_delay = 0.15  
        self.running = True
        self.lock = threading.Lock()
        self.is_finished = False
        self.dots_thread = threading.Thread(target=self._animate_dots)
        self.dots_thread.daemon = True
        self.dots_thread.start()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def _animate_dots(self):
        while self.running:
            current_time = time.time()
            if current_time - self.last_dot_time >= self.dot_delay:
                with self.lock:
                    if not self.is_finished:
                        self.dot_count = (self.dot_count + 1) % 4
                    self.last_dot_time = current_time
                    dots = "." * self.dot_count
                    dots = dots.ljust(3)  
                    print("\033[K", end="")  
                    print(f"\033[38;2;255;255;255msearching{dots} \033[90m(\033[38;2;255;255;255m{self.current}/{self.total}\033[90m) \033[90m[\033[38;2;255;255;255m{int(self.current * 100 / self.total)}%\033[90m]", end="\r")
                    sys.stdout.flush()
            time.sleep(0.01)

    def update(self, n=1, found=0):
        with self.lock:
            self.current += n
            self.found += found

    def close(self):
        with self.lock:
            self.is_finished = True
            self.running = False
        if hasattr(self, 'dots_thread'):
            self.dots_thread.join()
        dots = "." * self.dot_count
        dots = dots.ljust(3)  
        percentage = int(self.current * 100 / self.total)
        print(f"\033[38;2;255;255;255mSearching{dots} \033[90m(\033[38;2;255;255;255m{self.current}/{self.total}\033[90m) \033[90m[\033[38;2;255;255;255m{int(self.current * 100 / self.total)}%\033[90m]")
