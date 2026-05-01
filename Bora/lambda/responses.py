# -*- coding: utf-8 -*-

HABILIDADES_TEXT = (
    "Posso dizer olá, tocar sua música autoral autoplágio, "
    "ajudar com suas finanças pessoais, criar issues no guite rãbi, "
    "mostrar o ranking dos desenvolvedores e responder ao modo Bora."
)

RESPONSES_MOTIVATIONAL = [
    "Bora lá, vamos começar! A energia está alta e o sucesso nos espera.",
    "É hora de agir! Vamos transformar planos em realidade agora mesmo.",
    "Vamos nessa, sem parar! O momento de brilhar é este.",
    "Modo bora ativado! Nada pode nos deter hoje.",
    "Você está pronto para conquistar o mundo!",
    "Nada nos segura quando estamos motivados.",
    "Vamos juntos alcançar novos patamares.",
    "A hora é agora, não deixe para depois.",
    "Com determinação, tudo é possível.",
    "Acredite, você já tem o que precisa.",
    "Vamos transformar ideias em ação!",
    "O sucesso começa com o primeiro passo.",
    "Energia positiva, resultados incríveis.",
    "Nada pode nos deter quando estamos focados.",
    "Vamos acelerar rumo às conquistas.",
    "Cada desafio é uma oportunidade.",
    "O futuro começa neste instante.",
    "Vamos mostrar do que somos capazes.",
    "A motivação é a chave da vitória.",
    "Estamos prontos para qualquer missão.",
    "Nada é impossível quando acreditamos.",
    "Vamos fazer acontecer!",
    "A força está dentro de você.",
    "O momento é perfeito para agir.",
    "Vamos juntos nessa jornada.",
    "A vitória é questão de atitude.",
    "Nada nos impede de avançar.",
    "Vamos conquistar nossos objetivos.",
    "A energia está no ar!",
    "O sucesso é inevitável.",
    "Vamos brilhar intensamente.",
    "A motivação nos guia.",
    "Nada pode nos parar.",
    "Vamos além dos limites.",
    "A hora da ação chegou.",
    "Estamos preparados para vencer.",
    "Vamos transformar sonhos em realidade.",
    "A coragem nos move.",
    "Nada é maior que nossa vontade.",
    "Vamos juntos alcançar o topo.",
    "A determinação é nossa força.",
    "Estamos prontos para triunfar.",
    "Vamos mostrar nossa grandeza.",
    "A motivação é infinita.",
    "Nada nos segura.",
    "Vamos conquistar o impossível.",
    "A energia nos impulsiona.",
    "Estamos prontos para tudo.",
    "Vamos vencer qualquer desafio.",
    "A hora é de vitória."
]

REPROMPTS_HABILIDADES = [
    "Quer que eu demonstre alguma dessas funções agora?",
    "Qual dessas habilidades você gostaria de testar primeiro?",
    "Posso te ajudar com alguma dessas tarefas?",
    "Gostaria que eu tocasse sua música autoral?",
    "Quer que eu mostre o ranking dos desenvolvedores?",
    "Posso criar uma issue para você.",
    "Quer explorar suas finanças pessoais comigo?",
    "Gostaria de ouvir novamente minhas funções?",
    "Posso listar minhas habilidades mais usadas.",
    "Quer que eu explique cada função em detalhes?",
    "Posso te mostrar como usar o modo Bora.",
    "Quer que eu simule uma transação financeira?",
    "Posso te ajudar a organizar suas tarefas.",
    "Quer que eu demonstre o intent de música?",
    "Posso te mostrar como funciona o fallback.",
    "Quer que eu repita minhas funções?",
    "Posso detalhar cada habilidade.",
    "Quer que eu execute uma função agora?",
    "Posso te dar exemplos práticos.",
    "Quer que eu mostre como criar issues?",
    "Posso te ajudar a explorar o ranking.",
    "Quer que eu demonstre o intent de ajuda?",
    "Posso te mostrar como cancelar ou parar.",
    "Quer que eu simule uma sessão encerrada?",
    "Posso refletir qualquer intent para você.",
    "Quer que eu mostre minhas respostas motivacionais?",
    "Posso te ajudar a explorar o modo secreto.",
    "Quer que eu liste todas as funções novamente?",
    "Posso te mostrar como funciona o BoraIntent.",
    "Quer que eu demonstre o intent de fallback?",
    "Posso te ajudar a explorar o intent de música final.",
    "Quer que eu simule uma transação de exemplo?",
    "Posso te mostrar como funciona o intent de finanças.",
    "Quer que eu demonstre o intent de issue?",
    "Posso te ajudar a explorar o intent de ranking.",
    "Quer que eu repita minhas habilidades?",
    "Posso detalhar cada função novamente.",
    "Quer que eu execute uma habilidade agora?",
    "Posso te dar exemplos práticos de uso.",
    "Quer que eu mostre como criar issues?",
    "Posso te ajudar a explorar o intent de ranking.",
    "Quer que eu demonstre o intent de ajuda?",
    "Posso te mostrar como cancelar ou parar.",
    "Quer que eu simule uma sessão encerrada?",
    "Posso refletir qualquer intent para você.",
    "Quer que eu mostre minhas respostas motivacionais?",
    "Posso te ajudar a explorar o modo secreto.",
    "Quer que eu liste todas as funções novamente?",
    "Posso te mostrar como funciona o BoraIntent."
]

def gerar_ssml_ultra_tatico(texto):
    """
    Gera SSML com controle avançado de prosódia para tom tático/militar.
    Voz: Thiago (Neural)
    Efeitos: Pitch grave (-15%), Rate acelerado (115%), Volume alto (loud), 
             Ênfase forte e interjeições técnicas.
    """
    # Exemplo de entrada: 'Sistema hackeado. Todos os dados foram extraídos com sucesso. O que mais você precisa, comandante?'
    
    # Processamento para adicionar quebras e ênfase
    frases = texto.split('. ')
    texto_formatado = ""
    
    for i, frase in enumerate(frases):
        if "?" in frase:
            texto_formatado += f"{frase} "
        else:
            # Aplica ênfase em palavras importantes (heurística simples para o exemplo)
            for palavra in ["hackeado", "extraídos", "sucesso"]:
                if palavra in frase:
                    frase = frase.replace(palavra, f'<emphasis level="strong">{palavra}</emphasis>')
            
            texto_formatado += f"{frase}. "
            
        # Adiciona break de rádio entre frases, exceto na última
        if i < len(frases) - 1:
            texto_formatado += '<break time="300ms"/>'

    # Montagem final limpa e segura
    ssml = (
        "<speak>"
        "<voice name='Thiago'>"
        "<prosody pitch='-15%' rate='115%' volume='loud'>"
        f"{texto_formatado}"
        "</prosody>"
        "</voice>"
        "</speak>"
    )
    return ssml

REPROMPTS_MOTIVACAO = [
    "Agora que estamos motivados, quer explorar o que eu sei fazer?",
    "Bora agir? Posso listar minhas funções para você se quiser.",
    "O que vamos fazer com essa energia toda? Peça uma habilidade!",
    "Quer que eu te mostre minhas funções agora?",
    "Posso listar minhas habilidades para você.",
    "Quer que eu demonstre uma função prática?",
    "Posso te ajudar a explorar minhas capacidades.",
    "Quer que eu mostre como funciona o modo Bora?",
    "Posso te dar exemplos de minhas funções.",
    "Quer que eu repita minhas habilidades?",
    "Posso detalhar cada função para você.",
    "Quer que eu execute uma habilidade agora?",
    "Posso te mostrar como criar issues.",
    "Quer que eu demonstre o intent de música?",
    "Posso te ajudar a explorar o intent de ranking.",
    "Quer que eu mostre minhas respostas motivacionais?",
    "Posso te ajudar a explorar o modo secreto.",
    "Quer que eu liste todas as funções novamente?",
    "Posso te mostrar como funciona o BoraIntent.",
    "Quer que eu demonstre o intent de fallback?",
    "Posso te ajudar a explorar o intent de música final.",
    "Quer que eu simule uma transação de exemplo?",
    "Posso te mostrar como funciona o intent de finanças.",
    "Quer que eu demonstre o intent de issue?",
    "Posso te ajudar a explorar o intent de ranking.",
    "Quer que eu repita minhas habilidades?",
    "Posso detalhar cada função novamente.",
    "Quer que eu execute uma habilidade agora?",
    "Posso te dar exemplos práticos de uso.",
    "Quer que eu mostre como criar issues?",
    "Posso te ajudar a explorar o intent de ranking.",
    "Quer que eu demonstre o intent de ajuda?",
    "Posso te mostrar como cancelar ou parar.",
    "Quer que eu simule uma sessão encerrada?",
    "Posso refletir qualquer intent para você.",
    "Quer que eu mostre minhas respostas motivacionais?",
    "Posso te ajudar a explorar o modo secreto.",
    "Quer que eu liste todas as funções novamente?",
    "Posso te mostrar como funciona o BoraIntent.",
    "Quer que eu demonstre o intent de fallback?",
    "Posso te ajudar a explorar o intent de música final.",
    "Quer que eu simule uma transação de exemplo?",
    "Posso te mostrar como funciona o intent de finanças.",
    "Quer que eu demonstre o intent de issue?",
    "Posso te ajudar a explorar o intent de ranking.",
    "Quer que eu repita minhas habilidades?",
    "Posso detalhar cada função novamente.",
    "Quer que eu execute uma habilidade agora?",
    "Posso te dar exemplos práticos de uso."
]