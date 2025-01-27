import speech_recognition as sr
import re
import json
import pyttsx3
from googletrans import Translator
import openai
import board
dir(board)
import busio
import gpiod
import time

from adafruit_servokit import ServoKit
#kit = ServoKit(channels=16,address=0x40)
#kit1= ServoKit(channels=16,address=0x41)
r = sr.Recognizer()
engine = pyttsx3.init()
model_engine = "gpt-3.5-turbo"

newVoiceRate = 145

using_stt = True
def emotions():
    print("KMS")

def get_user_input(prompt=None, lang: str = None):
    if using_stt:
        with sr.Microphone() as source:
            got_answer = False
            while not got_answer:
                if prompt != None:
                    say(prompt)
                try:
                    r.adjust_for_ambient_noise(source, duration=0.2)
                    if not lang:
                        lang = 'en'
                    answer = r.recognize_google(r.listen(source), language=lang)

                    got_answer = True

                except sr.UnknownValueError:
                    say("Google Speech Recognition could not understand audio. Please try again.")
                except sr.RequestError as e:
                    say("Could not request results from Google Speech Recognition service; {0}. Please try again".format(
                        e))
    else:
        if prompt != None:
            say(prompt)
        answer = input()
    print("got: " + answer)
    return answer


def say(text, lang=None):
    if lang:
        engine.setProperty('voice', lang)
    print(text)
    engine.say(text)
    engine.runAndWait()


def language_setter(first_language, second_language):
    should_stop = False
    langs = [first_language, second_language]
    codes = [get_language_code(first_language), get_language_code(second_language)]
    speaker: int = 0
    while not should_stop:
        speech_line = get_user_input(f"Person {speaker + 1}, you can talk:", lang=langs[speaker])

        translator = Translator()

        text_to_translate = translator.translate(speech_line, src=langs[speaker], dest=langs[1 - speaker])
        text_o = text_to_translate.text

        say(text_o, lang=codes[1 - speaker])

        res = re.findall(r'\w+', text_o)
        if (res[0] == 'end'):
            should_stop = True
        speaker = 1 - speaker


def listen_for_command():
    command = ""
    while command != "end":
        speech_line = get_user_input("Talk:")
        res = re.findall(r'\w+', speech_line)
        command = res[0]
        match command:
            case "search":
                say("Got that!")
                print(speech_line)

                say(ask_chatgpt(speech_line))

            case "hi":
                print("HI")
               # kit.servo[14].angle=180
               # time.sleep(2)
               # kit.servo[14].angle=90
               # kit.servo[12].angle = 80
               # time.sleep(2)
               # kit.servo[12].angle=90
                #time.sleep(1)
                #kit.servo[0].angle=180
               # kit.servo[1].angle=180
               # kit.servo[2].angle=180
               # kit.servo[3].angle=180
               # kit.servo[4].angle=180
            case "introduce yourself":
		       ## deshide  kit1.servo[1].angle=180
                say("Salut,numele meu este Cuza si sunt in fata dumneavoastra astazi pentru a ma prezenta.Sunt un robot umanoid printat in intregime 3d,scopul meu este de a ajuta omul in orice sarcina fie ca este interactionarea cu copii sau munca fizica,pot face orice,mainile si capul meu au o mobilitate impresionanta pentru a imita perfect actiunile unui om.De asemenea,sunt primul robot umanoid aprobat si sustinut de ministerul inovarii si al digitalizari,dar cel mai important,sunt construit de cei doi elevi ce se afla astazi langa mine.Va multumesc siva rog sa imi scuzati pronuntia,inca invat limba romana")

            case "translate":
                langs = []
                for word in res:
                    if get_language_code(word) != None:
                        langs.append(word)
                if len(langs) < 2:
                    say("Sorry, I didn't get your languages! Please try again.")
                else:
                    say(f"Translating from {langs[0]} to {langs[1]}!")
                    language_setter(langs[0], langs[1])
            case "end":
                say("closing down!")
            case _:
                say("Unknown command! please try again.")


def ask_chatgpt(question):
    print(question)
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        n=1,
        messages=[
            {"role": "system", "content": "You are a helpful assistant with exciting, interesting things to say."},
            {"role": "user", "content": question},
        ])
    message = response.choices[0]['message']
    return message['content']


supported_languages_info = json.load(open('supported_languages.json'))['text']


def get_language_code(language_name):
    for language in supported_languages_info:
        if language['language'].lower() == language_name.lower():
            return language['code']
    return None


def main():
    using_stt=True
    engine.setProperty('voice', "ro")
    engine.setProperty('rate', newVoiceRate)
    listen_for_command()


if __name__ == "__main__":
    should_use_stt = input("using vocal commands?(y/n)")
    if should_use_stt == "y":
        using_stt = True
    else:
        using_stt = False
    main()

