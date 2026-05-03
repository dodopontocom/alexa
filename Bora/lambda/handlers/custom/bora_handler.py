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
logger.setLevel(logging.DEBUG)

class BoraIntentHandler(AbstractRequestHandler):
    """Handler evoluído para o BoraIntent usando slots e responses externo."""
    def can_handle(self, handler_input):
        intent_name = ask_utils.get_intent_name(handler_input) if ask_utils.is_request_type("IntentRequest")(handler_input) else "N/A"
        is_bora = ask_utils.is_intent_name("BoraIntent")(handler_input)
        logger.debug("BoraIntentHandler can_handle: intent_recebido=%s | resultado=%s", intent_name, is_bora)
        return is_bora

    def handle(self, handler_input):
        session_id = handler_input.request_envelope.session.session_id
        logger.info("BoraIntent: iniciando handler | session_id=%s", session_id)
        
        try:
            # Captura o slot tipoPergunta
            tipo_pergunta = ask_utils.get_slot_value(handler_input, "tipoPergunta")
            
            # Tratamento para slots vazios/nulos
            slot_value = tipo_pergunta if tipo_pergunta else "VAZIO/NULO"
            logger.debug("Slot tipoPergunta capturado: %s", slot_value)

            # Lógica de resposta baseada no slot
            if tipo_pergunta == "habilidades":
                speak_output = f"Eu tenho várias funções interessantes! {HABILIDADES_TEXT}"
                reprompt_text = random.choice(REPROMPTS_HABILIDADES)
            elif tipo_pergunta == "motivação":
                speak_output = random.choice(RESPONSES_MOTIVATIONAL)
                reprompt_text = random.choice(REPROMPTS_MOTIVACAO)
            else:
                # Lógica padrão (aleatória entre os dois se o slot estiver vazio)
                logger.debug("BoraIntent: usando lógica padrão (aleatória)")
                if random.random() > 0.5:
                    speak_output = f"Aqui estão minhas habilidades: {HABILIDADES_TEXT}"
                    reprompt_text = random.choice(REPROMPTS_HABILIDADES)
                else:
                    speak_output = random.choice(RESPONSES_MOTIVATIONAL)
                    reprompt_text = random.choice(REPROMPTS_MOTIVACAO)

            # Usando SSML com voz Ricardo
            ssml_speech = f'<speak><voice name="Ricardo">{speak_output}</voice></speak>'
            ssml_reprompt = f'<speak><voice name="Ricardo">{reprompt_text}</voice></speak>'
            
            response = (
                handler_input.response_builder
                    .speak(ssml_speech)
                    .ask(ssml_reprompt)
                    .response
            )
            
            logger.debug("BoraIntent: response gerado com sucesso | speak_output=%s", speak_output[:50] + "...")
            return response

        except Exception:
            logger.exception("Erro inesperado no BoraIntent")
            # Retorna uma resposta amigável em vez de quebrar silenciosamente
            return (
                handler_input.response_builder
                    .speak("Desculpe, tive um problema ao processar seu pedido no modo bora.")
                    .response
            )
