# -*- coding: utf-8 -*-
import logging
import requests
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core import utils as ask_utils
from utils import call_ia_api
import datetime

logger = logging.getLogger(__name__)


class FinancesIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("FinancesIntent")(handler_input)

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
                now = datetime.datetime.utcnow()

                # Próximo mês (tratando dezembro -> janeiro do próximo ano)
                year = now.year + (1 if now.month == 12 else 0)
                month = 1 if now.month == 12 else now.month + 1

                # Define como dia 1, às 12:00 UTC
                due_date = datetime.datetime(year, month, 1, 12, 0, 0)

                # Formata no padrão ISO solicitado
                _dueDate = due_date.strftime("%Y-%m-%dT%H:%M:%S.000+00:00")

                transacao += ". Não esquecer de enviar o json completo. Com 'isPaid' false e as chaves 'date' e 'dueDate' sejam preenchidas com a data de vencimento como " + _dueDate
            
            logger.info(f"transacao para IA: {transacao}")
            
            # Chamar API da IA (centralizada em utils)
            ia_response = call_ia_api(transacao, IA_API_DATA, persona="finances_2")
            
            # Limpar resposta - remover tudo após o início do JSON (primeiro '{')
            if '{' in ia_response:
                ia_response = ia_response.split('{')[0].strip()
            
            # Limitar tamanho da resposta
            if len(ia_response) > IA_API_DATA["max_response_length"]:
                ia_response = ia_response[:7900] + "... e isso é tudo por agora."
            
            return (
                handler_input.response_builder
                    .speak(ia_response)
                    .ask("Quer adicionar outra transacao?")
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