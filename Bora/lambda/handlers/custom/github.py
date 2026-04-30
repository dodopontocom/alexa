# -*- coding: utf-8 -*-
import logging
import os
import requests
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core import utils as ask_utils
from utils import call_ia_api

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

GITHUB_REPO = "dodopontocom/finances"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

class ReportIssueIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("ReportIssueIntent")(handler_input)

    def handle(self, handler_input):
        try:
            # Configuração da API da IA
            IA_API_DATA = {
                "url": "https://api.vibecodia.com.br/chat",
                "timeout": 6,
                "max_response_length": 8000
            }

            # Captura do slot "relato"
            relato = ask_utils.get_slot_value(handler_input, "relato")
            logger.info(f"🔹 ReportIssueIntent acionado. Slot relato: {relato}")

            if not relato:
                speech = "Não consegui identificar o problema relatado. Pode repetir?"
                return handler_input.response_builder.speak(speech).set_should_end_session(False).response

            # Chama IA com persona "devops" (centralizada)
            analise = call_ia_api(
                relato,
                IA_API_DATA,
                persona="devops",
                instrucoes=(
                        "Forneça passos detalhados, incluindo grep, caminhos de arquivos, "
                        "verificação de seletor/propriedade e comandos exatos para aplicar mudanças "
                        "em cores, botões ou cards antes de sugerir alterações."
                )
            )

            logger.info(f"🔹 Análise IA gerada: {analise}")

            # Cria issue no GitHub
            issue_url = self.create_github_issue(relato, analise)
            if issue_url:
                speech = f"Issue criada com sucesso no Guite rãbi! Você pode verificar aqui: {issue_url}"
            else:
                speech = "Houve um problema ao criar a issue no Guite rãbi, mas a análise da IA foi gerada."

            return handler_input.response_builder.speak(speech).set_should_end_session(True).response

        except Exception as e:
            logger.error(f"❌ Erro no ReportIssueIntent: {str(e)}")
            speech = "Houve um erro inesperado ao processar seu relato."
            return handler_input.response_builder.speak(speech).set_should_end_session(True).response

    # usa call_ia_api do utils


    def create_github_issue(self, relato, analise):
        """Cria uma issue no GitHub com relato + análise"""
        try:
            github_api = f"https://api.github.com/repos/{GITHUB_REPO}/issues"
            headers = {
                "Authorization": f"token {GITHUB_TOKEN}",
                "Accept": "application/vnd.github+json"
            }
            data = {
                "title": f"Bug via Alexa: {relato[:50]}",
                "body": f"### Relato\n{relato}\n\n### Análise IA\n{analise}",
                "labels": ["alexa", "ai-analysis"]
            }
            r = requests.post(github_api, headers=headers, json=data)

            if r.status_code == 201:
                issue = r.json()
                logger.info(f"✅ Issue criada: {issue.get('html_url')}")
                return issue.get("html_url")
            else:
                logger.error(f"❌ Erro ao criar issue: {r.status_code} - {r.text}")
                return None
        except Exception as e:
            logger.error(f"❌ Erro create_github_issue: {str(e)}")
            return None
