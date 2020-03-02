import speech_recognition as sr


class ConvertSpeechToText:
    def __init__(self, language):

        self.language = language
        self.message = None

    def voice_recording(self) -> str:
        r = sr.Recognizer()

        with sr.Microphone() as s:
            r.adjust_for_ambient_noise(s)

            print('Start recording')
            while True:
                audio = r.listen(s)
                speech = r.recognize_google(audio, language=self.language)

                print('Stop recording')
                self.message = speech
                break

        return self.message


if __name__ == '__main__':
    ConvertSpeechToText('en')
