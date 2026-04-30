# -*- coding: utf-8 -*-
import logging
import os
import requests
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core import utils as ask_utils
from ask_sdk_dynamodb.adapter import DynamoDbPersistenceAdapter

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# GitHub Config
GITHUB_REPO = "dodopontocom/finances"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

# DynamoDB Config (Alexa Hosted já injeta essas variáveis automaticamente)
ddb_table_name = "c6b401b2-aa7e-4553-920c-9c38028afa07"
ddb_region = os.environ.get("DYNAMODB_REGION", "us-east-1")

persistence_adapter = DynamoDbPersistenceAdapter(
    table_name=ddb_table_name,
    create_table=False
)

class LeaderboardIntentHandler(AbstractRequestHandler):
    """Handler para mostrar ranking de devs baseado em issues fechadas"""
    
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("LeaderboardIntent")(handler_input)

    def handle(self, handler_input):
        try:
            # === Buscar issues fechadas no GitHub ===
            github_api = f"https://api.github.com/repos/{GITHUB_REPO}/issues?state=closed&per_page=50"
            headers = {
                "Authorization": f"token {GITHUB_TOKEN}",
                "Accept": "application/vnd.github+json"
            }
            r = requests.get(github_api, headers=headers)

            if r.status_code != 200:
                logger.error(f"❌ Erro ao buscar issues: {r.status_code} - {r.text}")
                speech = "Não consegui acessar o GitHub para calcular o ranking agora."
                return handler_input.response_builder.speak(speech).set_should_end_session(True).response

            issues = r.json()
            scores_temp = {}

            for issue in issues:
                if "closed_by" in issue and issue["closed_by"]:
                    author = issue["closed_by"]["login"]
                    scores_temp[author] = scores_temp.get(author, 0) + 10  # +10 pontos por issue

            # === Carregar e atualizar pontuação persistida no DynamoDB ===
            attributes_manager = handler_input.attributes_manager
            attributes_manager.persistence_adapter = persistence_adapter
            persistent_attributes = attributes_manager.persistent_attributes or {}

            for dev, pts in scores_temp.items():
                current = persistent_attributes.get(dev, 0)
                persistent_attributes[dev] = current + pts

            attributes_manager.persistent_attributes = persistent_attributes
            attributes_manager.save_persistent_attributes()

            # === Montar ranking Top 3 ===
            ranking = sorted(persistent_attributes.items(), key=lambda x: x[1], reverse=True)[:3]

            if not ranking:
                speech = "Ainda não encontrei issues fechadas para montar o ranking."
            else:
                speech = "Aqui está o ranking dos desenvolvedores: "
                for i, (dev, pts) in enumerate(ranking, 1):
                    speech += f"Em {i}º lugar, {dev} com {pts} pontos. "

            logger.info(f"🏆 Ranking gerado: {ranking}")

            return handler_input.response_builder.speak(speech).set_should_end_session(False).response

        except Exception as e:
            logger.error(f"❌ Erro no LeaderboardIntent: {str(e)}")
            speech = "Houve um erro ao montar o ranking dos desenvolvedores."
            return handler_input.response_builder.speak(speech).set_should_end_session(True).response
