# imports
import speech_recognition as sr

# setup Recogniser
r = sr.Recognizer()


def main():
    print("Hello World")
    # start listening on Mic
    with sr.Microphone() as source:
        print("Listening")
        audio = r.listen(source)

    # Google Interpret output
    try:
        print("Google Speech Recognition thinks you said " + r.recognize_google(audio, language='hu'))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


if __name__ == "__main__":
    main()
