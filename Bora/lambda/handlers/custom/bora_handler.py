# -*- coding: utf-8 -*-
import logging
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core import utils as ask_utils

logger = logging.getLogger(__name__)

class BoraIntentHandler(AbstractRequestHandler):
    """Handler para o BoraIntent."""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("BoraIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = "Bora lá, vamos começar! A energia está alta e o sucesso nos espera."
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .set_should_end_session(False)
                .response
        )
