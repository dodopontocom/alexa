# GUIA MESTRE DE VOZES E SSML - Alexa (PT-BR)

Este guia técnico detalha o uso avançado de Speech Synthesis Markup Language (SSML) para as vozes brasileiras da Alexa, permitindo criar interações mais expressivas, dinâmicas e menos robóticas.

## 1. Catálogo de Vozes Polly (PT-BR)

As vozes neurais da Amazon Polly oferecem alta naturalidade. Use a tag `<voice name="...">` para alternar entre elas.

| Voz | Gênero | Tipo | Tag SSML |
| :--- | :--- | :--- | :--- |
| **Camila** | Feminino | Neural | `<voice name="Camila">...</voice>` |
| **Vitória** | Feminino | Neural | `<voice name="Vitoria">...</voice>` |
| **Ricardo** | Masculino | Neural | `<voice name="Ricardo">...</voice>` |
| **Thiago** | Masculino | Neural | `<voice name="Thiago">...</voice>` |

## 2. Estilos de Fala (Speaking Styles)

O estilo de fala ajusta a entonação para contextos específicos. Use a tag `<amazon:domain>`.

| Estilo | Descrição | Exemplo SSML |
| :--- | :--- | :--- |
| **Conversacional** | Tom casual e natural. | `<amazon:domain name="conversational">Tudo bem por aqui!</amazon:domain>` |
| **News** | Entonação de apresentador de notícias. | `<amazon:domain name="news">As manchetes de hoje indicam...</amazon:domain>` |

## 3. Emoções e Intensidade

A tag `<amazon:emotion>` permite adicionar sentimentos à fala. Disponível para a voz padrão da Alexa em PT-BR.

| Emoção | Intensidade | Exemplo SSML |
| :--- | :--- | :--- |
| **Excited** (Animado) | `low`, `medium`, `high` | `<amazon:emotion name="excited" intensity="high">Uau! Você ganhou!</amazon:emotion>` |
| **Disappointed** (Decepcionado) | `low`, `medium`, `high` | `<amazon:emotion name="disappointed" intensity="medium">Ah, que pena. Tente de novo.</amazon:emotion>` |

## 4. Modos Especiais e Speechcons

Para criar "vibes" específicas como o modo adolescente ou sarcástico, combinamos `<prosody>` e Speechcons.

### Speechcons (Interjeições)
As Speechcons são palavras ou frases curtas ditas com entonação especial.
- **Tag**: `<say-as interpret-as="interjection">...</say-as>`
- **Exemplos PT-BR**: "tipo assim", "uau", "vixe", "caramba", "opa", "puxa vida".

### Simulando Modo Adolescente/Sarcástico
Combine pitch alto, rate acelerado e interjeições:
```xml
<speak>
    <prosody pitch="high" rate="fast">
        <say-as interpret-as="interjection">tipo assim</say-as>, 
        eu já sabia disso há séculos, tá?
    </prosody>
</speak>
```

## 5. Biblioteca de Sons (Audio Player)

Insira efeitos sonoros oficiais usando a tag `<audio>`.
- **Sintaxe**: `<audio src="soundbank://soundlibrary/[categoria]/[efeito]"/>`

| Categoria | Exemplo de Efeito | Caminho Completo |
| :--- | :--- | :--- |
| **Gameshow** | Resposta Positiva | `soundbank://soundlibrary/ui/gameshow/amzn_ui_sfx_gameshow_positive_response_01` |
| **SciFi** | Som de Computador | `soundbank://soundlibrary/scifi/amzn_sfx_scifi_computer_beep_01` |
| **Human** | Aplausos | `soundbank://soundlibrary/human/amzn_sfx_crowd_applause_01` |

## 6. Exemplo em Python (SSML Complexo)

Função para gerar uma resposta com múltiplas camadas de SSML:

```python
def get_sarcastic_whisper_response(mensagem):
    """
    Retorna uma string SSML misturando sussurro, 
    voz Polly específica e modo sarcástico.
    """
    ssml = (
        "<speak>"
            "<voice name='Vitoria'>"
                "<amazon:effect name='whispered'>"
                    "Vou te contar uma coisa..."
                "</amazon:effect>"
                "<break time='500ms'/>"
                "<prosody pitch='high' rate='110%'>"
                    "<say-as interpret-as='interjection'>tipo assim</say-as>, "
                    f"{mensagem}. "
                    "<amazon:emotion name='disappointed' intensity='low'>"
                        "Mas quem sou eu para julgar, né?"
                    </amazon:emotion>"
                "</prosody>"
            "</voice>"
        "</speak>"
    )
    return ssml

# Exemplo de uso:
# output = get_sarcastic_whisper_response("sua planilha de gastos está... interessante")
```

---
*Manual técnico de referência para Design de Voz Alexa PT-BR.*

## 7. Exemplo Ultra Tático (Thiago)

Abaixo, um exemplo de como o SSML tático é construído para a voz do Thiago, focando em autoridade e clareza militar.

### SSML Gerado
```xml
<speak>
    <voice name="Thiago">
        <prosody pitch="-15%" rate="115%" volume="loud">
            <say-as interpret-as="interjection">entendido</say-as>. 
            Sistema <emphasis level="strong">hackeado</emphasis>. 
            <break time="300ms"/>
            Todos os dados foram <emphasis level="strong">extraídos</emphasis> com <emphasis level="strong">sucesso</emphasis>. 
            <break time="300ms"/>
            O que mais você precisa, comandante?
            <say-as interpret-as="interjection">câmbio</say-as>.
        </prosody>
    </voice>
</speak>
```

### Características Técnicas
- **Pitch (-15%)**: Confere uma voz mais grave e imponente.
- **Rate (115%)**: Fala rápida e decisiva, típica de comunicações críticas.
- **Volume (loud)**: Máxima clareza para ambientes com ruído ou Echo Dots pequenos.
- **Breaks (300ms)**: Simula a cadência de rádio/satélite entre frases.
- **Emphasis (strong)**: Destaca os termos de ação e status.
