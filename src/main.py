# imports
import speech_recognition as sr

# setup Recogniser and sources
r = sr.Recognizer()
# must be customized for all users / or made smhow automatic
mic = sr.Microphone(device_index=1)
dc = sr.Microphone(device_index=4)


def listenOnMic():
    # start listening on Mic
    with mic as source:
        print("Listening")
        audio = r.listen(source)
        googleInterpret(audio)


def googleInterpret(audio):
    # Google Interpret output
    try:
        print("Booglidú szerint ezt mondtad: " + r.recognize_google(audio, language='hu', pfilter=0))
    except sr.UnknownValueError:
        print("Booglidú nem érti mit vakerálsz..")
    except sr.RequestError as e:
        print("Booglidú nem volt elérhető; {0}".format(e))


def listenOnChat():
    # start listening on Chat
    with dc as source:
        print("Listening")
        audio = r.listen(source)
        googleInterpret(audio)


if __name__ == "__main__":
    # list audio devices
    print(sr.Microphone.list_microphone_names())

    # loop
    while True:
        listenOnMic()
        # TODO test chat input
        # listenOnChat()
