# Fluxos das Skills Alexa

Documentação técnica dos fluxos de dados e integrações das skills **Bora** e **Finances**.

## 1. Fluxo de Inteligência Artificial (Vibe Codia)
Utilizado para processar linguagem natural e gerar respostas dinâmicas ou analisar problemas.

```mermaid
sequenceDiagram
    participant U as Usuário
    participant A as Alexa Device
    participant L as Lambda (Python)
    participant U as utils.py (call_ia_api)
    participant IA as API Vibe Codia

    U->>A: "Alexa, adicione café 10 reais"
    A->>L: Envia Intent (ex: FinancesIntent)
    L->>U: Chama call_ia_api(message, persona)
    U->>IA: POST /chat (payload: message, persona)
    IA-->>U: Retorna JSON (assistant_reply)
    U->>U: Limpeza de Emojis e Truncamento
    U-->>L: Retorna texto limpo
    L-->>A: Speak(ia_response)
    A->>U: "Entendido, registrei sua transação..."
```

---

## 2. Fluxo de Integração GitHub (Issues & Ranking)
Utilizado para reportar problemas e calcular o ranking de desenvolvedores.

```mermaid
sequenceDiagram
    participant U as Usuário
    participant L as Lambda (Handlers)
    participant GH as GitHub API
    participant DB as DynamoDB (Persistence)

    rect rgb(200, 230, 255)
    Note over U, GH: Reportar Problema
    U->>L: "O cliente relatou erro no login"
    L->>GH: POST /issues (Usando GITHUB_TOKEN)
    GH-->>L: 201 Created
    L-->>U: "Issue criada com sucesso no GitHub"
    end

    rect rgb(230, 255, 200)
    Note over U, DB: Ranking de Devs
    U->>L: "Qual é o ranking dos desenvolvedores?"
    L->>GH: GET /issues?state=closed
    GH-->>L: Lista de Issues Fechadas
    L->>L: Calcula pontos (+10 por issue)
    L->>DB: Salva/Recupera Atributos Persistentes
    L-->>U: "O top 3 é: Rodolfo, DevA, DevB"
    end
```

---

## 3. Fluxo de Áudio (Music Player)
Utilizado para tocar músicas autorais armazenadas remotamente.

```mermaid
sequenceDiagram
    participant U as Usuário
    participant A as Alexa Device
    participant L as Lambda (music.py)
    participant S as Servidor de Áudio

    U->>A: "Alexa, tocar música autoral"
    L->>L: Define MUSIC_DATA (URL mp3)
    L->>A: Envia PlayDirective (AudioPlayer)
    A->>A: Speak(Efeito sussurro)
    A->>S: GET /autoplágio.mp3
    S-->>A: Stream de Áudio
    A->>U: Inicia reprodução da música
```

---

## 4. Fluxo de Deploy (CI/CD)
Automação de entrega via GitHub Actions.

```mermaid
graph TD
    A[Push para Main] --> B{GitHub Actions}
    B --> C[Setup Node & Python]
    B --> D[Configure ASK CLI]
    D --> E[Populate .env with MY_GITHUB_PAT]
    E --> F[ASK Deploy]
    F --> G[Alexa Hosted - CodeCommit]
    G --> H[Lambda Atualizado]
```
