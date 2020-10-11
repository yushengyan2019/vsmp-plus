#!/usr/bin/python
# -*- coding:utf-8 -*-
import argparse, os, time, sys, random
import ffmpeg

# set path to ffmpeg
os.environ['PATH'] += os.pathsep + '/usr/local/bin/'

def time_to_play(total_frames, increment, delay):
    # find out how many frames will display
    frames = total_frames/increment

    print('%d out of %d frames will display' % (frames, total_frames))

    # frames * delay = total minutes to play
    total = (frames * delay)/60

    result = ()
    if(total / 1440 > 1):
        result = (total/1440, 'days')
    elif(total / 60 > 1):
        result = (total/60, 'hours')
    else:
        result = (total, 'minutes')

    print('Video will take %f %s to fully play' % result)



def check_mp4(value):
    if not value.endswith('.mp4'):
        raise argparse.ArgumentTypeError("%s should be an .mp4 file" % value)
    return value

# parse the arguments
parser = argparse.ArgumentParser(description='VSMP Settings')
parser.add_argument('-f', '--file', type=check_mp4, required=True,
    help="File to grab screens of")
parser.add_argument('-d', '--delay',  default=120,
    help="Delay between screen updates, in seconds")
parser.add_argument('-i', '--increment',  default=4,
    help="Number of frames skipped between screen updates")
parser.add_argument('-s', '--start', default=1,
    help="Start at a specific frame")

args = parser.parse_args()

# setup some helpful variables
dir_path = os.path.dirname(os.path.realpath(__file__)) # full path to the directory of this script
video_name = os.path.splitext(os.path.basename(args.file))[0] # video name, no ext

# create the tmp directory if it doesn't exist
tmpDir = os.path.join(dir_path, 'tmp')
if (not os.path.exists(tmpDir)):
    os.mkdir(tmpDir)

# check if we have a "save" file
currentPosition = float(args.start)
saveFile = os.path.join(tmpDir,video_name + '.txt')
if( os.path.exists(saveFile)):
    try:
        f = open(saveFile)
        for line in f:
            currentPosition = float(line.strip())
        f.close()
    except:
        print('error opening save file')

print('Analyzing %s' % args.file)
print('Starting Frame: %s, Frame Increment: %s, Delay between updates: %s' % (args.start, args.increment, args.delay))
print('')

# Check how many frames are in the movie
frameCount = int(ffmpeg.probe(args.file)['streams'][0]['nb_frames'])

# find total time to play entire movie
print('Entire Video:')
time = time_to_play(frameCount, float(args.increment), float(args.delay))
print('')


# find time to play what's left
print('Remaining Video:')
time = time_to_play(frameCount - currentPosition, float(args.increment), float(args.delay))
print('')

# figure out how many 'real time' minutes per hour
print('Minutes of Film Displayed Breakdown:')
secondsPerIncrement = float(args.increment)/30
framesPerSecond = secondsPerIncrement/float(args.delay) # this is how many "seconds" of film actually shown per second of realtime

minutesPerHour = (framesPerSecond * 60)
print('Assuming 30fps total video is %f minutes long' % (frameCount/30/60))
print('%f minutes of film per hour' % (minutesPerHour))
print('%f minutes of film per day' % (minutesPerHour * 24))

exit()