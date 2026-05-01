# -*- coding: utf-8 -*-
import logging
import random
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core import utils as ask_utils

logger = logging.getLogger(__name__)

class BoraIntentHandler(AbstractRequestHandler):
    """Handler para o BoraIntent com respostas dinâmicas e voz Ricardo."""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("BoraIntent")(handler_input)

    def handle(self, handler_input):
        # Respostas motivacionais dinâmicas
        RESPONSES = [
            "Bora lá, vamos começar! A energia está alta e o sucesso nos espera.",
            "É hora de agir! Vamos transformar planos em realidade agora mesmo.",
            "Vamos nessa, sem parar! O momento de brilhar é este.",
            "Modo bora ativado! Nada pode nos deter hoje."
        ]
        
        # Reprompts para incentivar interação
        REPROMPTS = [
            "O que mais você quer fazer?",
            "Estou pronto para o próximo passo. O que deseja?",
            "Qual é a próxima missão?"
        ]
        
        speak_output = random.choice(RESPONSES)
        reprompt_text = random.choice(REPROMPTS)
        
        # Usando SSML com voz Ricardo
        ssml_speech = f'<speak><voice name="Ricardo">{speak_output}</voice></speak>'
        ssml_reprompt = f'<speak><voice name="Ricardo">{reprompt_text}</voice></speak>'
        
        return (
            handler_input.response_builder
                .speak(ssml_speech)
                .ask(ssml_reprompt)
                .response
        )
