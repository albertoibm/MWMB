chromatic = ["C","C#","D","Eb","E","F","F#","G","G#","A","Bb","B"]
def char2note(char):
    return 12*(1+int(char[-1]))+chromatic.index(char[:-1])
def note2char(note):
    return chromatic[note%12]+str(octave(note))
def octave(note):
    return note/12-1
def splitLine(line):
    fields = filter(None,line.replace('\t',' ').split(' '))
    return [int(fields[0]), float(fields[1]), char2note(fields[2]), int(fields[3]), float(fields[4])]
