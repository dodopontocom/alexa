# -*- coding: utf-8 -*-
import logging
import random
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core import utils as ask_utils
from responses import (
    HABILIDADES_TEXT, 
    RESPONSES_MOTIVATIONAL, 
    REPROMPTS_HABILIDADES, 
    REPROMPTS_MOTIVACAO
)

logger = logging.getLogger(__name__)

class BoraIntentHandler(AbstractRequestHandler):
    """Handler evoluído para o BoraIntent usando slots e responses externo."""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("BoraIntent")(handler_input)

    def handle(self, handler_input):
        # Captura o slot tipoPergunta
        tipo_pergunta = ask_utils.get_slot_value(handler_input, "tipoPergunta")
        logger.info(f"BoraIntent acionado. Slot tipoPergunta: {tipo_pergunta}")

        # Lógica de resposta baseada no slot
        if tipo_pergunta == "habilidades":
            speak_output = f"Eu tenho várias funções interessantes! {HABILIDADES_TEXT}"
            reprompt_text = random.choice(REPROMPTS_HABILIDADES)
        elif tipo_pergunta == "motivação":
            speak_output = random.choice(RESPONSES_MOTIVATIONAL)
            reprompt_text = random.choice(REPROMPTS_MOTIVACAO)
        else:
            # Lógica padrão (aleatória entre os dois se o slot estiver vazio)
            if random.random() > 0.5:
                speak_output = f"Aqui estão minhas habilidades: {HABILIDADES_TEXT}"
                reprompt_text = random.choice(REPROMPTS_HABILIDADES)
            else:
                speak_output = random.choice(RESPONSES_MOTIVATIONAL)
                reprompt_text = random.choice(REPROMPTS_MOTIVACAO)

        # Usando SSML com voz Ricardo
        ssml_speech = f'<speak><voice name="Ricardo">{speak_output}</voice></speak>'
        ssml_reprompt = f'<speak><voice name="Ricardo">{reprompt_text}</voice></speak>'
        
        return (
            handler_input.response_builder
                .speak(ssml_speech)
                .ask(ssml_reprompt)
                .response
        )
