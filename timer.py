import time
import sys
from sys import stdout
from threading import Thread
from playsound import playsound

# A simple program that lets the user run a timer.
class AlarmSound(Thread):
    """Overall class to manage the sound of the alarm"""
    def __init__(self):
        Thread.__init__(self)
    
    def run(self):
        try:
            playsound('Alarm-ringtone.mp3')
        except IOError:
            print('\nSoundfile not found.')

class AlarmClock():
    """Manages the alarm clock."""
    def __init__(self):
        """Declare all the necessary variables."""
        self.timerEnd = 0
        self.timerStart = 0


    def getReadableTime(self, epoch):
        # Returns a readable string from epoch time in H-M
        return time.strftime('%H:%M', time.localtime(epoch))

    def getExactTimeLeft(self, epoch):
        # Returns a readable string from epoch time.
        if epoch <= 60.0:
            return time.strftime('%S', time.localtime(epoch))
        elif epoch < 3600.0:
            return time.strftime('%M:%S', time.localtime(epoch))
        elif epoch >= 3600.0:
            hours = time.strftime('%H', time.localtime(epoch))
            # Fixes a bug that for some reason adds 1 hour if %H is more than 1
            if int(hours) > 1:
                hours = int(hours) - 1
            return time.strftime(f"{hours}:%M:%S", time.localtime(epoch))


    def playAlarmSound(self):
        """Create a new thread and run the alarm sound."""
        alarmsound = AlarmSound()
        alarmsound.daemon = True
        alarmsound.start()
        input("Press 'Enter' to stop the alarm.")
        sys.exit()

    def setTimer(self):
        """Sets the timer for the alarm."""
        print("Set the timer with ((H)00,(M)00,(S)00):\n")
        while True:
            try:
                seconds = 0
                timer = input()
                splitTime = timer.split(',')
                if len(splitTime) > 3:
                    raise ValueError
                for index, split in enumerate(splitTime):
                    if index == 0:
                        seconds += int(split) * 3600
                        print('Adding hours.')
                    elif index == 1:
                        seconds += int(split) * 60
                        print('Adding minutes.')
                    elif index == 2:
                        seconds += int(split)
                        print('Adding seconds.')            
                print(seconds)
                break
            except KeyboardInterrupt:
                print('Done!\n')
                break
            except ValueError:
                print('Please enter the time as: ((H)00,(M)00,(S)00):\n')
        self.timerStart = time.time()
        self.timerEnd = self.timerStart + int(seconds)
    
    def runTimer(self):
        """Run the timer."""
        print(f"Timer will end: {self.getReadableTime(self.timerEnd)}")
        while time.time() < self.timerEnd:
            timeLeft = self.timerEnd - time.time() + 1
            if timeLeft > 1:
                print('\x1b[2K\r', "", end="\r")
                print(f"{self.getExactTimeLeft(timeLeft)}.", end="\r")
            time.sleep(1)
        # This clears the last line in the console. 
        print('\x1b[2K\r', "", end="\r")
        

if __name__ == '__main__':
    # Make an alarm instance and run it.
    alarm = AlarmClock()
    alarm.setTimer()
    alarm.runTimer()
    alarm.playAlarmSound()

