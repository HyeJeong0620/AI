import threading
import time
from queue import Queue
def data_generator(queue):
    for i in range(10):
        time.sleep(1) # 데이터 생성에 시간이 조금 걸린다고 가정
        queue.put(i) # 데이터를 큐에 삽입
        print(f"Data {i} generated and sent.")
        
def data_consumer(queue):
    while True:
        data = queue.get() # 데이터를 큐에서 받아옴
        if data is None: # None 데이터를 받으면 종료
            break
        print(f"Data {data} received and processed.")
        
# 큐 생성
data_queue = Queue()

# 쓰레드 생성
generator_thread = threading.Thread(target=data_generator, args=(data_queue,))
consumer_thread = threading.Thread(target=data_consumer, args=(data_queue,))

# 쓰레드 시작
generator_thread.start()
consumer_thread.start()

# 쓰레드 종료 대기
generator_thread.join()
data_queue.put(None) # 소비자 쓰레드에 종료 신호 전달
consumer_thread.join()

print("Data processing complete.")
