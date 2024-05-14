# imports
import speech_recognition as sr

# setup Recogniser and sources
r = sr.Recognizer()
r.energy_threshold = 600
r.dynamic_energy_threshold = True
# must be customized for all users / or made smhow automatic
mic = sr.Microphone(device_index=1)
dc = sr.Microphone(device_index=4)
# calibrate ambient threshold
print("Adjusting for ambient noise...")
with mic as source:
    r.adjust_for_ambient_noise(source)
print("Adjustment done")


def listenOnMic():
    # start listening on Mic
    with mic as Mic:
        audio = r.listen(source=Mic, timeout=None, phrase_time_limit=8, snowboy_configuration=None)
        callbackInterpret(audio)


def callbackInterpret(recognizer, audio):
    # Google Interpret output
    try:
        print("Booglidú szerint ezt mondtad: \n" + recognizer.recognize_google(audio, language='hu', pfilter=0))
    except sr.UnknownValueError:
        print("Booglidú nem érti mit vakerálsz..")
    except sr.RequestError as e:
        print("Booglidú nem volt elérhető; {0}".format(e))


def listenOnChat():
    # start listening on Chat
    with dc as source:
        audio = r.listen(source=source, timeout=None, phrase_time_limit=8, snowboy_configuration=None)
        # Should not be needed, but I leave it here in case...: r.adjust_for_ambient_noise(source, 0.5)
        callbackInterpret(audio)


if __name__ == "__main__":
    # list audio devices
    print(sr.Microphone.list_microphone_names())
    print("Listening In Background...")
    stop_listening = r.listen_in_background(mic, callbackInterpret, 8)
    # loop
    while True:
        pass
        # listenOnMic()
        # TODO test chat input
        # listenOnChat()
