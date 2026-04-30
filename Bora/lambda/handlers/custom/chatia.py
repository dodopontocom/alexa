# -*- coding: utf-8 -*-
import logging
import requests
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core import utils as ask_utils
from utils import call_ia_api

logger = logging.getLogger(__name__)


class ChatFinancesIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("ChatFinancesIntent")(handler_input)

    def handle(self, handler_input):
        try:
            # Dados centralizados da API
            IA_API_DATA = {
                "url": "https://api.vibecodia.com.br/chat",
                "timeout": 6,
                "max_response_length": 8000
            }
            
            # Pegar a transacao do usuário
            transacao = ask_utils.get_slot_value(handler_input, "transacao")
            if not transacao:
                transacao = "Olá, como você está?"
            else:
                transacao += ". Não esquecer de enviar o json completo"
            
            logger.info(f"transacao para IA: {transacao}")
            
            # Chamar API da IA (centralizada em utils)
            ia_response = call_ia_api(transacao, IA_API_DATA, persona="finances")
            
            # Limpar resposta - remover tudo após o início do JSON (primeiro '{')
            if '{' in ia_response:
                ia_response = ia_response.split('{')[0].strip()
            
            # Limitar tamanho da resposta
            if len(ia_response) > IA_API_DATA["max_response_length"]:
                ia_response = ia_response[:7900] + "... e isso é tudo por agora."
            
            return (
                handler_input.response_builder
                    .speak(f'<speak><voice name="Ricardo">{ia_response}</voice></speak>')
                    .ask(f'<speak><voice name="Ricardo">Quer adicionar outra transação?</voice></speak>')
                    .response
            )

        except Exception as e:
            logger.error(f"Erro no ChatFinancesIntent: {str(e)}")
            error_speech = "Desculpe, houve um problema ao conectar com a IA. Tente novamente."
            return (
                handler_input.response_builder
                    .speak(error_speech)
                    .ask("Que tal tentar outra transacao?")
                    .response
            )

    # usa call_ia_api do utils