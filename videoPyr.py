from q import *
import cv2
import threading


outputDir = 'frames'
clipFileName = 'clip.mp4'
frameDelay = 42  # the answer to everything


def convert(queue1, queue2):
    count = 0                                                          # initialize frame count

    while True:
        inputFrame = queue1.dequeue()                                      # next frame

        if inputFrame == 'END':
            break

        print(f'Converting frame {count}\n')
        grayscaleFrame = cv2.cvtColor(inputFrame, cv2.COLOR_BGR2GRAY)
        queue2.enqueue(grayscaleFrame)

        count += 1


    q2.enqueue('END')

def extract(queue):
    global clipFileName
    count = 0
    vidcap = cv2.VideoCapture(clipFileName)
    success, image = vidcap.read()

    print(f'Reading frame {count} {success}\n')
    while success:
        queue.enqueue(image)                           # send frame to queue (replaces line 26 from demo)
        success, image = vidcap.read()
        print(f'Reading frame {count}')
        count += 1

    # Determine whether you are at the end of the file
    queue.enqueue('END')

def display(q):
    count = 0                                      # initializes frame count

    while True:
        frame = q.dequeue()                        # load the frame

        if frame == 'END':
            print("Last frame read.")
            break

        print(f'Displaying frame {count}\n')
        cv2.imshow('Video', frame)                 # Display frame in window "Video"


        if cv2.waitKey(frameDelay) and 0xFF == ord("q"):
            break

        count += 1

    # make sure we cleanup the windows, otherwise we might end up with a mess
    cv2.destroyAllWindows()

q1 = q()
q2 = q()

t1 = threading.Thread(target=extract, args=(q1,))
t2 = threading.Thread(target=convert, args=(q1, q2 ))
t3 = threading.Thread(target=display, args=(q2,))

t1.start()
t2.start()
t3.start()