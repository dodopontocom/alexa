# -*- coding: utf-8 -*-
import logging
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do .env
load_dotenv()
import ask_sdk_core.utils as ask_utils
import random
import json
from pathlib import Path
from datetime import datetime
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard

# Import handlers from the refactored package
from handlers.base.handlers import (
    LaunchRequestHandler,
    HelpIntentHandler,
    CancelOrStopIntentHandler,
    FallbackIntentHandler,
    SessionEndedRequestHandler,
    IntentReflectorHandler,
    CatchAllExceptionHandler,
)

# CUSTOM HANDLERS
from handlers.custom.music import PlayAutoplagioIntentHandler
from handlers.custom.chatia import ChatFinancesIntentHandler
from handlers.custom.github import ReportIssueIntentHandler
from handlers.custom.issueleader import ClosedIssuesCountIntentHandler

# Configurar logging mais detalhado
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Adicionar logging de inicialização
logger.info("=== INICIANDO SKILL BUILDER ===")

sb = SkillBuilder()
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# CUSTOMS AQUI
sb.add_request_handler(PlayAutoplagioIntentHandler())
sb.add_request_handler(ChatFinancesIntentHandler())
sb.add_request_handler(ReportIssueIntentHandler())
sb.add_request_handler(ClosedIssuesCountIntentHandler())

sb.add_request_handler(IntentReflectorHandler())
sb.add_exception_handler(CatchAllExceptionHandler())

logger.info("✓ Todos os handlers registrados")

lambda_handler = sb.lambda_handler()

logger.info("=== SKILL INICIALIZADA COM SUCESSO ===")