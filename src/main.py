# imports
import time

import speech_recognition as sr
from speech_recognition import AudioData

# setup Recogniser and sources
r = sr.Recognizer()
r.energy_threshold = 600
r.dynamic_energy_threshold = True
# must be customized for all users / or made smhow automatic
global mic
mic = sr.Microphone(device_index=1)
global dc
global cachedAudioData
# calibrate ambient threshold
print("Adjusting for ambient noise...")
with mic as source:
    r.adjust_for_ambient_noise(source)
print("Adjustment done")


def listenOnMic():
    # start listening on Mic
    with mic as Mic:
        audio = r.listen(source=Mic, timeout=None, phrase_time_limit=8, snowboy_configuration=None)
        googleInterpret(r, audio)


# TODO caching bg audio
def callbackForBgListen(recognizer, audio):
    cachedAudioData = audio


def recordToFile(input):
    with input as source:
        audio = r.listen(source)

    with open("microphone-results.wav", "wb") as f:
        f.write(audio.get_wav_data())


def googleInterpret(recognizer, audiodata):
    # Google Interpret output
    try:
        print("Booglidú szerint ezt mondtad: \n" + recognizer.recognize_google(audiodata, language='hu', pfilter=0))
    except sr.UnknownValueError:
        print("Booglidú nem érti mit vakerálsz..")
    except sr.RequestError as e:
        print("Booglidú nem volt elérhető; {0}".format(e))


def listenOnChat():
    # start listening on Chat
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


if __name__ == "__main__":
    # list audio devices
    print(sr.Microphone.list_microphone_names())
    # set up cache
    lastInterpretedAudioData: AudioData = None
    cachedAudioData: AudioData = None
    print("Listening In Background...")
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
