import time
import thread
data = []
instrument = ""
timeSig = ""
keySig = ""
tempo = 0
j = 0
k = 0
majorKeys = ["C", "G", "D", "A", "E", "B", "Gb/F#", "Db", "Ab", "Eb", "Bb", "F"]
minorKeys = ["a", "e", "b", "f#", "c#", "g#", "eb/d#", "bb", "f", "c", "g", "d"]
midiCPerM = "0"
midiCPerMili = "0"
midiClockPer = "0"
bps = 0.0
bpmili = 0.0
thread_started = False
execution = "0"
midi_clocks = [0]
running = True
delete = 0
note = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
pitch = ""
numerator = ""
instruments = []
midi_type = 100
track_no = 0
instrument_said = False
line = [0, 0, 0]
h = 0
old_line = []
line_sorter = [()]
p_start = 0
p_end = 0
line_tog = False

with open("C:\Users\student\Desktop\FULL MIDI.txt") as f:
    data = f.read()
    f.close()
    data = data.replace(" ", "")
    data = data.replace("\n", ",newline,")
    data = data.split(',')
##    for i in data:
##        old_line = line
##        if i == "newline":
##            line.append(data[j-h:j])
##            h = 0
##            line_sorter.append((line, int(line[2])))
##        h += 1
##        j += 1
##    sorted(line_sorter, key=lambda a_line: a_line[-1])
##    print line_sorter[[1]]
    while running == True:
        j = 0
        delete = 0
        for i in data:
            if i == "newline":
                execution = data[j+2]
                track_no = data[j+1]
            def time_counter(clocks, i):
                    while running == True:
                        time.sleep(0.001)
                        clocks.append((float(midiCPerMili)+clocks[i]))
                        i += 1
                
            if thread_started != True:
                thread_started = True
                #try:
                thread.start_new_thread(time_counter, (midi_clocks, k, ))
                #except:
                    #print "Error: unable to start thread"
                
            #if int(execution) <= int(midi_clocks[len(midi_clocks)-1])

            
            if not (int(execution) > int(midi_clocks[len(midi_clocks)-1])):
                if i == "Header":
                    midi_type = int(data[j+1])
                if i == "Instrument_name_t":
                    instrument = data[j+1].replace('"', '')
                    instruments.append(instrument)
                if i == "Time_signature":
                    numerator = data[j+1]
                    timeSig = numerator + "/" + str(2**int(data[j+2]))
                    midiClockPer = data[j+3]
                    print "Time signature: " + timeSig
                if i == "Key_signature":
                    if data[j+2] == '"major"':
                        keySig = majorKeys[int(data[j+1])] + " Major"
                        print "Key signature: " + keySig
                    elif data[j+2] == '"minor"':
                        keySig = minorKeys[int(data[j+1])] + " Minor"
                        print "Key signature: " + keySig
                if i == "Tempo":
                    tempo = int((60000000/int(data[j+1]))+0.5)
                    print "Tempo: " + str(tempo) + " BPM"
                    bps = tempo / 60.0
                    bpmili = bps / 100.0
                    midiCPerM = str(int(midiClockPer) * (tempo*int(numerator)))
                    midiCPerMili = str(((float(midiClockPer)) * (bpmili * int(numerator))))
                    print "Midi Clocks per Milisecond: " + midiCPerMili

                if i == "Note_on_c":
                    pitch = str((int(data[j+2])/12) - 1)
                    if midi_type > 0:
                        if data[j+3] != "0":
                            print "Note on: " + note[int(data[j+2])%12] + pitch + " at " + instruments[int(track_no) - 2]
                        elif data[j+3] == "0":
                            print "Note off: " + note[int(data[j+2])%12] + pitch + " at " + instruments[int(track_no) - 2]
                    else:
                        if data[j+3] != "0":
                            print "Note on: " + note[int(data[j+2])%12] + pitch
                        elif data[j+3] == "0":
                            print "Note off: " + note[int(data[j+2])%12] + pitch
                elif i == "Note_off_c":
                    if midi_type > 0:
                        print "Note off: " + note[int(data[j+2])%12] + pitch + " at " + instruments[int(track_no) - 2]
                    else:
                        print "Note off: " + note[int(data[j+2])%12] + pitch

                if i == "End_track" and int(data[j-5]) == int(midi_clocks):
                    running = False  

                if i == "newline" and line_tog == True:
                    line_tog = False
                    p_end = j
                elif i == "newline" and line_tog == False:
                    line_tog = True
                    p_start = j
                
                print data[p_start:p_end]
                del data[p_start:p_end]
                #delete += 1
            #print int(midi_clocks[len(midi_clocks)-1])
            #if int(midi_clocks[len(midi_clocks)-1]) == 480:
            #    print "Hello!"
            #elif int(midi_clocks[len(midi_clocks)-1]) == 6000:
            #    print "Hello again."
            #print data[j]
            j += 1
            #h += 1
        #del data[0:delete - 4]
        #print data[0:delete - 4]
