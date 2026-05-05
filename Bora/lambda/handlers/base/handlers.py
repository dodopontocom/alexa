# -*- coding: utf-8 -*-
import logging
import ask_sdk_core.utils as ask_utils
from ask_sdk_core.dispatch_components import AbstractRequestHandler, AbstractExceptionHandler
from responses import gerar_ssml_ultra_tatico

logger = logging.getLogger(__name__)


class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        logger.info("=== EXECUTANDO LAUNCH REQUEST HANDLER ===")
        try:
            texto = "Modo Secreto ativado. Sistema pronto. O que deseja, comandante?"
            reprompt_texto = "Aguardando ordens."
            
            speak_output = gerar_ssml_ultra_tatico(texto)
            reprompt_output = gerar_ssml_ultra_tatico(reprompt_texto)
            
            logger.info(f"=== SSML GERADO COM SUCESSO ===")
            return (
                handler_input.response_builder
                    .speak(speak_output)
                    .ask(reprompt_output)
                    .set_should_end_session(False)
                    .response
            )
        except Exception as e:
            logger.error(f"Erro no LaunchRequestHandler: {str(e)}", exc_info=True)
            raise e


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
        speech = '<speak><voice name="Ricardo">Hmm, não entendi. Você pode dizer olá ou pedir ajuda. O que você gostaria?</voice></speak>'
        reprompt = '<speak><voice name="Ricardo">Desculpe, não entendi. Pode repetir?</voice></speak>'
        return handler_input.response_builder.speak(speech).ask(reprompt).response


class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        reason = handler_input.request_envelope.request.reason
        error = handler_input.request_envelope.request.error
        logger.info(f"=== SESSÃO ENCERRADA: motivo={reason} | erro={error} ===")
        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        intent_name = ask_utils.get_intent_name(handler_input)
        logger.warning("=== INTENT REFLECTOR ATIVADO: %s ===", intent_name)
        speak_output = f"Você acionou o intent {intent_name}."
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("O que mais você deseja fazer?")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        logger.error("=== EXCEPTION HANDLER ATIVADO ===", exc_info=True)
        logger.error(f"Tipo: {type(exception).__name__} | Mensagem: {str(exception)}")
        
        # Log do request que causou a falha
        request_type = handler_input.request_envelope.request.object_type
        logger.error(f"Request Type que falhou: {request_type}")
        
        speak_output = "Desculpe, comandante. Tive um erro interno no sistema tático. Tente novamente."
        return handler_input.response_builder.speak(speak_output).ask(speak_output).response
