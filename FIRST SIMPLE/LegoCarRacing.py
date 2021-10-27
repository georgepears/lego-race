# Import libraries
import RPi.GPIO as GPIO
import time
import os
import pygame

# Set LED GPIO pins
LEDRED = 13
LEDGREEN = 19
LEDBLUE = 26

# Set start button GPIO pin
STARTBTN = 6

# Set lane trigger GPIO pins
LANE1ON = 2
LANE1OFF = 3
LANE2ON = 4
LANE2OFF = 5

# Set 'lane timing' booleans
LANE1 = False
LANE2 = False

# Set 'lane ended' booleans
END1 = False
END2 = False

# Set 'allowed to start' boolean
ALLOWED = False

# Set lane time counters
COUNT1 = 0
COUNT2 = 0

# Set constant timer
timer = 0;

# Set up GPIO pins to board numbering
GPIO.setmode(GPIO.BCM)

# Set GPIO inputs for lane triggers and button
GPIO.setup(STARTBTN, GPIO.IN)
GPIO.setup(LANE1ON, GPIO.IN)
GPIO.setup(LANE1OFF, GPIO.IN)
GPIO.setup(LANE2ON, GPIO.IN)
GPIO.setup(LANE2OFF, GPIO.IN)
GPIO.setup(STARTBTN, GPIO.IN)

# Set GPIO outputs for LEDs
GPIO.setup(LEDGREEN, GPIO.OUT)
GPIO.output(LEDGREEN, GPIO.LOW)
GPIO.setup(LEDRED, GPIO.OUT)
GPIO.output(LEDRED, GPIO.LOW)
GPIO.setup(LEDBLUE, GPIO.OUT)
GPIO.output(LEDBLUE, GPIO.LOW)

# Startup message
print ("\n"*100)
print "Press the button to start a new race"

# Start timer loop
while True:

    # Go through loop every 0.02 seconds
    time.sleep(0.02)
    timer = timer + 0.02

    # If start button has been pressed, start race
    if (GPIO.input(STARTBTN) == GPIO.HIGH and ALLOWED == False):

        # Reset variables to make sure race start is ready 
        LANE1 = False
        LANE2 = False
        END1 = False
        END2 = False
        COUNT1 = 0
        COUNT2 = 0

        # Print message - new race started
        print "\n"*100
        print "New Race Started - Go on GREEN!"

        # Start playing THE CHAIN audio file
        pygame.mixer.init()
        pygame.mixer.music.load("TheChain.wav")
        pygame.mixer.music.play()
        
        # Start the LEDs - reset all colours to off
        GPIO.output(LEDRED, GPIO.LOW)
        GPIO.output(LEDGREEN, GPIO.LOW)
        GPIO.output(LEDBLUE, GPIO.LOW)

        # Long red flash
        GPIO.output(LEDRED, GPIO.HIGH)
        time.sleep(2)

        # Three quick red flashes
        GPIO.output(LEDRED, GPIO.LOW)
        time.sleep(0.4)
        GPIO.output(LEDRED, GPIO.HIGH)
        time.sleep(0.4)
        GPIO.output(LEDRED, GPIO.LOW)
        time.sleep(0.4)
        GPIO.output(LEDRED, GPIO.HIGH)
        time.sleep(0.4)
        GPIO.output(LEDRED, GPIO.LOW)
        time.sleep(0.4)
        GPIO.output(LEDRED, GPIO.HIGH)
        time.sleep(0.4)
        GPIO.output(LEDRED, GPIO.LOW)
        time.sleep(0.4)

        # Green until end of race
        GPIO.output(LEDGREEN, GPIO.HIGH)
        
        # Now enable the race start triggers, allowing car to be detected through the start line
        ALLOWED = True

    # Start lane 1 if lane 1 start is triggered and start button has been pressed
    if GPIO.input(LANE1ON) == GPIO.LOW and LANE1 == False and ALLOWED == True:
        LANE1 = True
        print "Lane 1 started"

    # Stop lane 1 if lane 1 stop is triggered but only if the lane has been started
    if GPIO.input(LANE1OFF) == GPIO.LOW and LANE1 == True:
            LANE1 = False
            END1 = True
            print "Lane 1 ended"
            ALLOWED = False

    # Add to the lane 1 timer if a race has been started
    if LANE1 == True:
        COUNT1 = COUNT1 + 0.02

    # Start lane 2 if lane 2 start is triggered and start button has been pressed
    if GPIO.input(LANE2ON) == GPIO.LOW and LANE2 == False and ALLOWED == True:
        LANE2 = True
        print "Lane 2 started"

    # Stop lane 2 if lane 2 stop is triggered but only if the lane has been started
    if GPIO.input(LANE2OFF) == GPIO.LOW and LANE2 == True:
            LANE2 = False
            END2 = True
            print "Lane 2 ended"
            ALLOWED = False

    # Add to the lane 2 timer if a race has been started
    if LANE2 == True:
        COUNT2 = COUNT2 + 0.02

    # If both lanes have finished, print scores and reset game
    if END1 == True and END2 == True:

        # Stop playing THE CHAIN
        pygame.mixer.music.fadeout(2000)

        # Print each lane's time and if lane 1 is faster, print lane 1 won
        if COUNT1 > COUNT2:
            print "\n"*100
            print "LANE 1 = ",COUNT1
            print "LANE 2 = ",COUNT2
            print "LANE 2 WON!"
            print "\nPress the button to start a new race..."

        # Print each lane's time and if lane 2 is faster, print lane 2 won
        elif COUNT2 > COUNT1:
            print "\n"*100
            print "LANE 1 = ",COUNT1
            print "LANE 2 = ",COUNT2
            print "LANE 1 WON!"
            print "\nPress the button to start a new race"

        ## Print each lane's time and if both lanes have the same time, print same times
        elif COUNT1 == COUNT2:
            print "\n"*100
            print "LANE 1 = ",COUNT1
            print "LANE 2 = ",COUNT2
            print "SAME TIMES!"
            print "\nPress the button to start a new race..."

        # Reset all variables ready for the next race    
        COUNT1 = 0
        COUNT2 = 0
        END1 = False
        END2 = False
        GPIO.output(LEDGREEN, GPIO.LOW)

    # If lane 1 finishes before lane 2 has started, reset the game
    if END1 == True and LANE2 == False:

        # Print message telling the user the race has stopped
        print "\n"*100
        print "RACE ENDED: \n   Lane 1 finished before lane 2 started"
        print "\nPress the button to start a new race"

        # Reset all variables ready for the next race
        COUNT1 = 0
        COUNT2 = 0
        END1 = False
        END2 = False
        LANE1 = False
        LANE2 = False
        ALLOWED = False

        # Turn off green LED
        GPIO.output(LEDGREEN, GPIO.LOW)

        # Stop playing THE CHAIN
        pygame.mixer.music.fadeout(2000)

    # If lane 2 finishes before lane 1 has started, reset the game
    if END2 == True and LANE1 == False:

        # Print message telling the user the race has stopped
        print "\n"*100
        print "RACE ENDED: \n   Lane 2 finished before lane 1 started"
        print "\nPress the button to start a new race"

        # Reset all variables ready for the next race
        COUNT1 = 0
        COUNT2 = 0
        END1 = False
        END2 = False
        LANE1 = False
        LANE2 = False
        ALLOWED = False

        # Turn off green LED
        GPIO.output(LEDGREEN, GPIO.LOW)

        # Stop playing THE CHAIN
        pygame.mixer.music.fadeout(2000)
        
        
    # If finish race has not been triggered after 20 seconds, reset the game
    if COUNT1 >= 20 or COUNT2 >= 20:

        # Print message telling the user the race has stopped
        print "\n"*100
        print "RACE ENDED: \n   No cars have finished the race"
        print "\nPress the button to start a new race"
        
        # Reset all variables ready for the next race
        COUNT1 = 0
        COUNT2 = 0
        END1 = False
        END2 = False
        LANE1 = False
        LANE2 = False
        ALLOWED = False

        # Turn off green LED
        GPIO.output(LEDGREEN, GPIO.LOW)

        # Stop playing THE CHAIN
        pygame.mixer.music.fadeout(2000)

        
        
        
        


        
    
    
    
