# -*- coding: utf-8 -*-
import logging
import ask_sdk_core.utils as ask_utils
from ask_sdk_core.dispatch_components import AbstractRequestHandler, AbstractExceptionHandler

logger = logging.getLogger(__name__)


class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speak_output = '<speak><amazon:effect name="whispered">Ativando modo alternativo ultra secreto da Nasa</amazon:effect></speak>'
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("O que você gostaria de fazer agora?")
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = "Você pode me pedir para dizer olá, ou tocar sua música autoral. O que deseja?"
        return handler_input.response_builder.speak(speak_output).ask(speak_output).response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        speak_output = "Até logo!"
        return handler_input.response_builder.speak(speak_output).response


class FallbackIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        speech = "Hmm, não entendi. Você pode dizer olá ou pedir ajuda. O que você gostaria?"
        reprompt = "Desculpe, não entendi. Pode repetir?"
        return handler_input.response_builder.speak(speech).ask(reprompt).response


class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = f"Você acionou o intent {intent_name}."
        return handler_input.response_builder.speak(speak_output).response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        logger.error("=== EXCEPTION HANDLER ATIVADO ===")
        logger.error(f"Tipo da exceção: {type(exception).__name__}")
        logger.error(f"Mensagem da exceção: {str(exception)}")
        logger.error("Stacktrace completo:", exc_info=True)
        
        speak_output = "Desculpe, tive um problema ao processar sua solicitação. Tente novamente."
        return handler_input.response_builder.speak(speak_output).ask(speak_output).response
