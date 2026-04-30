import logging
import os
import boto3
from botocore.exceptions import ClientError
import requests


def call_ia_api(message: str, api_data: dict, persona: str = "alexa", instrucoes: str = "") -> str:
    """Central IA caller used by handlers.

    Returns a user-friendly string on errors, or the assistant reply on success.
    """
    logger = logging.getLogger(__name__)
    try:
        payload = {
            "persona": persona,
            "message": f"{message}\n{instrucoes}" if instrucoes else message
        }
        headers = {"Content-Type": "application/json"}

        logger.info(f"Chamando API IA: {api_data.get('url')}")
        response = requests.post(api_data["url"], json=payload, headers=headers, timeout=api_data.get("timeout", 6))

        if response.status_code == 200:
            data = response.json()
            assistant_reply = data.get("assistant_reply", "Não consegui gerar uma resposta.")
            # Optional token logging
            token_stats = data.get("token_stats") or data.get("tokenStats") or {}
            logger.info("IA tokens: %s", token_stats)

            # Truncate if needed
            max_len = api_data.get("max_response_length")
            if max_len and len(assistant_reply) > max_len:
                assistant_reply = assistant_reply[: max_len - 100] + "..."

            # Clean basic emojis that Alexa doesn't speak well
            for e in ("😊", "🎵", "✨"):
                assistant_reply = assistant_reply.replace(e, "")

            return assistant_reply.strip()
        else:
            logger.error("IA API error %s: %s", response.status_code, response.text)
            return "A IA está temporariamente indisponível."
    except requests.exceptions.Timeout:
        logger.error("Timeout calling IA API")
        return "A IA demorou muito para responder. Tente uma pergunta mais simples."
    except requests.exceptions.RequestException as e:
        logger.error("Connection error calling IA API: %s", str(e))
        return "Não consegui conectar com a IA no momento."
    except Exception as e:
        logger.error("Unexpected error calling IA API: %s", str(e))
        return "Houve um erro inesperado ao consultar a IA."


def create_presigned_url(object_name):
    """Generate a presigned URL to share an S3 object with a capped expiration of 60 seconds

    :param object_name: string
    :return: Presigned URL as string. If error, returns None.
    """
    s3_client = boto3.client('s3',
                             region_name=os.environ.get('S3_PERSISTENCE_REGION'),
                             config=boto3.session.Config(signature_version='s3v4',s3={'addressing_style': 'path'}))
    try:
        bucket_name = os.environ.get('S3_PERSISTENCE_BUCKET')
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=60*1)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response