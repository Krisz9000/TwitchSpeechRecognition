# imports
import time

# Libraries for successful interpretation, ...and of the Microphone
import speech_recognition as sr
from speech_recognition import AudioData

# setup Recogniser and sources
r = sr.Recognizer()
r.energy_threshold = 600
r.dynamic_energy_threshold = True
# must be customized for all users / or made smhow automatic
global mic
# might not work if not default device, TODO make a front-end for selecting it
mic = sr.Microphone(device_index=1)
global dc
global cachedAudioData
# calibrate ambient threshold
print("Adjusting for ambient noise...")
with mic as source:
    r.adjust_for_ambient_noise(source)
print("Adjustment done")


# Listening for the default input device (prob a mic), and automatically interpreting it in small segments
def listenOnMic():
    # start listening on Mic
    with mic as Mic:
        audio = r.listen(source=Mic, timeout=None, phrase_time_limit=8, snowboy_configuration=None)
        googleInterpret(r, audio)


# TODO caching bgrnd audio for simultaneous processing and listening on different threads
def callbackForBgListen(recognizer, audio):
    cachedAudioData = audio


# Function for writing a real-time audio output into a single, fix-ended audio file
def recordToFile(input):
    with input as source:
        audio = r.listen(source)

    with open("microphone-results.wav", "wb") as f:
        f.write(audio.get_wav_data())


# Function for passing an audio data to the Google Speech Interpreter
def googleInterpret(recognizer, audiodata):
    # Google Interpret output
    try:
        print("Booglidú szerint ezt mondtad: \n" + recognizer.recognize_google(audiodata, language='hu', pfilter=0))
    except sr.UnknownValueError:
        print("Booglidú nem érti mit vakerálsz..")
    except sr.RequestError as e:
        print("Booglidú nem volt elérhető; {0}".format(e))


# listening for Discord input || only works if VB/Audio driver configured properly, TODO bundle VBAudio
# TODO make front-end for selecting and configuring VBAudio Driver
def listenOnChat():
    # start listening on Chat
    # Only works if the stars and Gods want it so....  TODO need a menu where properly selectable
    dc = sr.Microphone(device_index=4)
    with dc as source:
        audio = r.listen(source=source, timeout=None, phrase_time_limit=6, snowboy_configuration=None)
        # Should not be needed, but I leave it here in case...: r.adjust_for_ambient_noise(source, 0.5)
        # googleInterpret(audio)
        try:
            print("Booglidú szerint ezt mondtad: \n" + r.recognize_google(audio, language='hu', pfilter=0))
        except sr.UnknownValueError:
            print("Booglidú nem érti mit vakerálsz..")
        except sr.RequestError as e:
            print("Booglidú nem volt elérhető; {0}".format(e))


# TODO Not comprehensible! Cleanup, too many angles for solutions right now.
if __name__ == "__main__":
    # list audio devices
    print(sr.Microphone.list_microphone_names())
    # set up cache
    # Trying to set up a multithreaded solution, where one thread is actively interpreting what a
    # second thread is actively listening to, that`s what the cache is for
    lastInterpretedAudioData: AudioData = None
    cachedAudioData: AudioData = None
    print("Listening In Background...")
    # setting up shut-down function || if called, stops bg listening
    stop_listening = r.listen_in_background(mic, callbackForBgListen, 8)
    # loop
    while True:
        if lastInterpretedAudioData != cachedAudioData:
            lastInterpretedAudioData = cachedAudioData
            print("setting new cache and interpreting..")
            googleInterpret(r, cachedAudioData)
            print("waiting for cache updates..")
            time.sleep(3)
        pass
        # listenOnMic()
        # TODO test chat input
        # listenOnChat()
