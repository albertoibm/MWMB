from sys import argv
from piano.track import Track
fname = argv[1]

track = Track()
track.loadFile(fname)
track.writeTrackFile(fname+".trk")
