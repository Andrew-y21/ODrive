import time

class timer:
    def __init__(self, return_function, time_delay):
        self.current_time = 0
        self.delay_seconds = time_delay
        self.return_funtion = return_function
        self.start_time = None
        self.timer_running = False

    def start_timer(self):
        self.start_time = time.perf_counter()
        self.timer_running = True


        while self.timer_running == True:
            elapsed_time = time.perf_counter - self.start_time
            if elapsed_time >= self.delay_seconds:
                self.return_funtion = True
                

            
                


