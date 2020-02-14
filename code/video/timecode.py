"""

  Created by Ed on 2/12/2020
 """

framerate = 24

def timecode_to_frames(timecode):
    return sum(f * int(t) for f,t in zip((3600*framerate, 60*framerate, framerate, 1), timecode.split(':')))

print timecode_to_frames('15:41:08:02') - timecode_to_frames('15:41:07:00')
# returns 26

def frames_to_timecode(frames):
    return '{0:02d}:{1:02d}:{2:02d}:{3:02d}'.format(frames / (3600*framerate),
                                                    frames / (60*framerate) % 60,
                                                    frames / framerate % 60,
                                                    frames % framerate)

print frames_to_timecode(26)
# returns "00:00:01:02"