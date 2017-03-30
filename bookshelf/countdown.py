import time

t = 120
def main(t):
    while t:
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, '\r')
        time.sleep(1)
        t -= 1
    print('Goodbye!\n\n\n\n\n')
	
main(t)