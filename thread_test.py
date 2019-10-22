import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time

class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width = self.vid.width, height = self.vid.height)
        self.canvas.pack()

        # Button that lets the user take a snapshot
        self.btn_snapshot=tkinter.Button(window, text="Snapshot", width=50, command=self.snapshot)
        self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()

        self.window.mainloop()

    def snapshot(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        if ret:
            cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def update(self):

        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
        self.window.after(self.delay, self.update)


class MyVideoCapture:

    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

         # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR to RGB
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

# Create a window and pass it to the Application object
App(tkinter.Tk(), "Tkinter and OpenCV")



'''from threading import Thread
from queue import Queue
import time

def thread1(threadname, q):
    #read variable "a" modify by thread 2
    while True:
        a = q.get()
        if a is None: return # Poison pill
        print(a)

def thread2(threadname, q):
    a = 0
    for _ in range(10):
        a += 1
        q.put(a)
        time.sleep(1)
    q.put(None) # Poison pill

queue = Queue()
thread1 = Thread( target=thread1, args=("Thread-1", queue) )
thread2 = Thread( target=thread2, args=("Thread-2", queue) )

thread1.start()
thread2.start()
thread1.join()
thread2.join()
'''


'''
    ////////*****  frame yakalama   ********/////////
    
    # bufferless VideoCapture
    class VideoCapture:
    
      def __init__(self, name):
        self.cap = cv2.VideoCapture(name)
        self.q = Queue.Queue()
        t = threading.Thread(target=self._reader)
        t.daemon = True
        t.start()
    
      # read frames as soon as they are available, keeping only most recent one
      def _reader(self):
        while True:
          ret, frame = self.cap.read()
          if not ret:
            break
          if not self.q.empty():
            try:
              self.q.get_nowait()   # discard previous (unprocessed) frame
            except Queue.Empty:
              pass
          self.q.put(frame)
    
      def read(self):
        return self.q.get()
    
    cap = VideoCapture(0)
    
    '''