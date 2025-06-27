import time
from threading import Thread

class QueueManager:
    def __init__(self):
        self.queue = []
        self.last_request_done = time.time() - 6000

    def add_to_queue(self, o):
        self.queue.append(o)

    def start(self):
        Thread(target=self.run).start()

    def run(self):
        while True:
            while self.queue:
                ct = time.time()
                if ct - self.last_request_done < 5 * 60:
                    time.sleep((5 * 60) - (ct - self.last_request_done))
                o = self.queue[0]
                o.start()
                try:
                    o.driver.quit()
                except:
                    pass
                self.queue.pop(0)
                self.last_request_done = time.time()
                print(f'Осталось заявок в очереди: {len(self.queue)}')
            time.sleep(0.1)
