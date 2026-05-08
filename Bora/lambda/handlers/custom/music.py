# -*- coding: utf-8 -*-
import logging
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core import utils as ask_utils
from ask_sdk_model.interfaces.audioplayer import (
    PlayDirective,
    PlayBehavior,
    AudioItem,
    Stream
)

logger = logging.getLogger(__name__)


class PlayAutoplagioIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("PlayAutoplagioIntent")(handler_input)

    def handle(self, handler_input):
        try:
            # Dados centralizados da música
            MUSIC_DATA = {
                "url": "https://atelie.vibecodia.com.br/autopl%C3%A1gio.mp3",
                "token": "autoplagio-track-001",
                "title": "Autoplágio",
                "artist": "Rodolfo Neto"
            }
            
            logger.info(f"Tocando música: {MUSIC_DATA['title']} - {MUSIC_DATA['artist']}")
            
            speak_output = "eu vou roubar algo de mim"

            # Criar a diretiva de reprodução com dados centralizados
            play_directive = PlayDirective(
                play_behavior=PlayBehavior.REPLACE_ALL,
                audio_item=AudioItem(
                    stream=Stream(
                        token=MUSIC_DATA["token"],
                        url=MUSIC_DATA["url"],
                        offset_in_milliseconds=0
                    ),
                    metadata={
                        "title": MUSIC_DATA["title"],
                        "subtitle": MUSIC_DATA["artist"]
                    }
                )
            )

            return (
                handler_input.response_builder
                    .speak(speak_output)
                    .add_directive(play_directive)
                    .set_should_end_session(True)
                    .response
            )

        except Exception as e:
            logger.error(f"Erro ao tocar música: {str(e)}")
            error_speech = "Desculpe, houve um problema ao tentar tocar a música."
            return handler_input.response_builder.speak(error_speech).response


class PlayAutoplagioFinalIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("PlayAutoplagioFinalIntent")(handler_input)

    def handle(self, handler_input):
        try:
            MUSIC_DATA = {
                "url": "https://atelie.vibecodia.com.br/autoplagio-versao-final.mp3",
                "token": "autoplagio-final-track-001",
                "title": "Autoplágio (Versão Final)",
                "artist": "Rodolfo Neto"
            }
            
            logger.info(f"Tocando música final: {MUSIC_DATA['title']}")
            
            speak_output = "finalmente, eu roubei algo de mim por completo"

            play_directive = PlayDirective(
                play_behavior=PlayBehavior.REPLACE_ALL,
                audio_item=AudioItem(
                    stream=Stream(
                        token=MUSIC_DATA["token"],
                        url=MUSIC_DATA["url"],
                        offset_in_milliseconds=0
                    ),
                    metadata={
                        "title": MUSIC_DATA["title"],
                        "subtitle": MUSIC_DATA["artist"]
                    }
                )
            )

            return (
                handler_input.response_builder
                    .speak(speak_output)
                    .add_directive(play_directive)
                    .set_should_end_session(True)
                    .response
            )

        except Exception as e:
            logger.error(f"Erro ao tocar música final: {str(e)}")
            error_speech = "Houve um problema ao tocar a versão final."
            return handler_input.response_builder.speak(error_speech).response
