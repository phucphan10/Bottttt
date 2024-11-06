import time
from zlapi import ZaloAPI
from zlapi.models import *
from concurrent.futures import ThreadPoolExecutor
import threading
import os

thread = ThreadPoolExecutor(max_workers=20)

class FastHandleBot(ZaloAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_spamming = False
        self.spam_thread = None
        self.spam_lock = threading.Lock()
        self.user_id = "7711754660468580715"
        self.id = "206926747996821925"
        idbox = "5792782596696849162"
        self.image_urls = ["https://i.postimg.cc/hG1frCzc/IMG-4466.jpg"] * 1000  # 1000 ảnh giống nhau

    def onMessage(self, mid, author_id, message, message_object, thread_id, thread_type):
        thread.submit(self.onHandle, mid, author_id, message, message_object, thread_id, thread_type)
        print(f"Nhận tin nhắn: {message}")

    def spamImages(self, message_object, thread_id, thread_type):

        index = 0
        delay = 0.1  
        start_time = time.time()  

        while self.is_spamming and index < 1000:
            if index < len(self.image_urls):
                image_url = self.image_urls[index]
                self.send(
                    Message(image=image_url),
                    thread_id=thread_id,
                    thread_type=thread_type
                )
                index += 1
                time.sleep(delay)  

                elapsed_time = time.time() - start_time
                if elapsed_time > 100:  
                    break
            else:
                break
            if not self.is_spamming:
                break

    def onHandle(self, mid, author_id, message, message_object, thread_id, thread_type):
        self.markAsDelivered(mid, message_object.cliMsgId, author_id, thread_id, thread_type, message_object.msgType)
        self.markAsRead(mid, message_object.cliMsgId, author_id, thread_id, thread_type, message_object.msgType)
        
        if not isinstance(message, str):
            message = "[không phải là tin nhắn]"

        # Kiểm tra tin nhắn
        if message == "Menu":
            mention = Mention(author_id, length=7, offset=0)
            color = MessageStyle(style="color", color="00BFFF", offset=0, length=3000, auto_format=False)
            smallfont = MessageStyle(style="font", size="12", offset=0, length=3000, auto_format=False)
            style = MultiMsgStyle([color, smallfont])
            self.send(
                Message(
                    text="@member\n.Spam: spam ảnh 🤪\n.Stop: dừng spam", style=style, mention=mention
                ),
                thread_id=thread_id,
                thread_type=thread_type
            )
        elif message.startswith(".Spam"):
            with self.spam_lock:
                if not self.is_spamming:
                    self.is_spamming = True
                    if self.spam_thread is None or not self.spam_thread.is_alive():
                        self.spam_thread = threading.Thread(
                            target=self.spamImages,
                            args=(message_object, thread_id, thread_type)
                        )
                        self.spam_thread.start()
        elif message == ".Stop":
            with self.spam_lock:
                if self.is_spamming:
                    self.is_spamming = False
                    if self.spam_thread and self.spam_thread.is_alive():
                        self.spam_thread.join()
                    color = MessageStyle(style="color", color="00BFFF", offset=0, length=3000, auto_format=False)
                    smallfont = MessageStyle(style="font", size="12", offset=0, length=3000, auto_format=False)
                    style = MultiMsgStyle([color, smallfont])
                    mention = Mention(author_id, length=7, offset=0)
                    self.send(
                        Message(
                            text="@member Nó Sợ Rồi 🤪",
                            style=style, mention=mention
                        ),
                        thread_id=thread_id,
                        thread_type=thread_type
                    )

client = FastHandleBot(
    '</>', '</>',
    imei="dán",
    user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    session_cookies=("Dán")
)
client.listen()