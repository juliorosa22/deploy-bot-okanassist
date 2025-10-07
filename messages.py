MESSAGES = {
    "en": {
        "welcome_authenticated": (
            "👋 *Hello {name}!*\n\n"
            "How can I help you today? You can track expenses, manage reminders, and view summaries.\n\n"
            "Type /help for examples!"
        ),
        "register_start": ("🚀 *Welcome to OkanAssist AI Registration!*\n\n"
            "I need a few details to create your account.\n\n"
            "📧 *Please enter your email address:*\n"
            "(This will be used to link your account)\n\n"
            "Type /cancel to stop registration anytime."
        ),
        "validate_email": ("❌ Please enter a valid email address.\n"
                          "Example: your.email@example.com"),
        "register_first_name": ( "✅ Email: {email}\n\n"
            "👤 *What's your first name?*\n"
            "(Press /skip to use: {first_name})"
        ),
        "register_last_name": ( "👤 *What's your last name?*\n"
            "(Press /skip to continue)"
        ),
        "register_timezone": ( "🕒 *What is your timezone?*\n\n"
            "You can say things like `I'm from New York`, `London`, `pacific time`, or `GMT+2`.\n\n"
            "This is crucial for reminders to be accurate."
        ),
        "register_confirmation": ("📋 *Please confirm your details:*\n\n"
            "📧 Email: {email}\n"
            "👤 Name: {first_name}"
            ),
        "register_confirmation_with_timezone": ("\n🌐 Language: {language}\n"
            "🕒 Timezone: {timezone}  _(I will interpret this automatically)_\n\n"
            "Type /confirm to create your account.\n\n\n"
            "Type /cancel to start over."
        ),
        
        "invalid_confirmation": "❌ Invalid response. Please type /confirm to create your account or /cancel to start over.",
        "register_cancelled": "❌ Registration cancelled. You can start over anytime by typing /register.",
        "payment_success": "✅ Payment successful! You now have premium access. Type /profile to check your status.",
        "payment_failure": "❌ Payment failed or was cancelled. Please try again with /upgrade or contact support if the issue persists.",
        "generic_error": "❌ An error occurred. Please try again later or contact support if the issue persists.",
        "support_prompt": ("🛠️ *Support Mode*\n\n"
            "Please describe your issue in detail. Your message will be sent directly to our support team.\n\n"
            "Type /cancel to exit support mode."
        ),
        "support_message": ("💬 *Support Request Received*\n\n"
            "Thank you for reaching out! Our support team will get back to you as soon as possible.\n\n"
            "In the meantime, you can also visit our FAQ page or check out /help for more information."
        ),
        "help_message": """
            🤖 *OkanAssist Bot Help*

            *💰 Transactions*
            You can manage your finances just by talking to me!

            • *Log transactions:* "Spent $25 on lunch", "Received $3000 salary"
            • *Get summaries:* "Show my spending this month", "What's my income for last week?"
            • *Generate PDF reports:* "I need a report for January", "Generate a PDF of my transactions from last month"

            *⏰ Reminders*
            Organize your life with smart reminders.

            • *Create reminders:* "Remind me to pay bills tomorrow at 3pm"
            • *View reminders:* "Show my urgent reminders", "What are my tasks for today?"
            • *Complete reminders:* "Mark today reminders as completed", "Clear last week's reminders", "Clear all reminders"

            *📄 Document Processing*
            • Send a photo of a receipt to automatically log an expense.
            • Send a PDF bank statement for bulk transaction import.

            *🎯 Commands*
            /start - Get started or log in
            /register - Create your account
            /help - Show this help message
            /upgrade - Get unlimited access
            /profile - View your profile

            
            Just talk to me naturally - I understand! 🎉
    """,
        "generic_downtime": "⚠️ The service is currently experiencing issues. Please try again later or contact support if the issue persists.",
        "user_not_found": "🔐 User not found. Please register first by typing /register.\n",
        "profile_info": (
                            "👤 *Your Profile*\n\n"
                            "📧 Email: {email}\n"
                            "👤 Name: {name}\n"
                            "🌐 Language: {language}\n"
                            "💰 Currency: {currency}\n"
                            "⏰ Timezone: {timezone}\n"
                            "🔗 WebApp URL: {webapp_url}\n"
                            "⭐ Premium: {premium_status}\n"
                        ),
        "manage_url": "🔗 [Manage your subscription here]({url})",
        "commands": {
            "start": {"name": "start", "description": "Start using the assistant"},
            "register": {"name": "register", "description": "Register your account"},
            "help": {"name": "help", "description": "Get help and examples"},
            "balance": {"name": "balance", "description": "View financial summary"},
            "reminders": {"name": "reminders", "description": "Show pending reminders"},
            "profile": {"name": "profile", "description": "View your profile"},
            "upgrade": {"name": "upgrade", "description": "Upgrade to Premium"},
            "support": {"name": "support", "description": "Contact customer support"},
        },
        "generic_maintenance": "⚠️ This feature is currently under maintenance. Please try again later.",
        "upgrade_link_generation": "⏳ Generating your personal upgrade link, please wait...\n",
        "portal_return": "🔗 *Welcome back to OkanAssist!*\n\nYou have successfully returned from the portal. How can I assist you today?\n\nType /help for examples!"
    },
    "es": {
        "welcome_authenticated": (
            "👋 ¡*Hola {name}!*\n\n"
            "¿Cómo puedo ayudarte hoy? Puedes registrar gastos, gestionar recordatorios y ver resúmenes.\n\n"
            "Escribe /help para ver ejemplos."
        ),
        "welcome_unauthenticated": (
            "👋 ¡*Bienvenido a OkanAssist!* Tu asistente financiero personal.\n\n"
            "Uso IA para ayudarte a registrar tus finanzas sin esfuerzo. Esto es lo que puedes hacer:\n\n"
            "💸 *Registra Transacciones:* Solo di 'gasté $15 en el almuerzo' o 'recibí $500 de salario'.\n"
            "📸 *Procesa Documentos:* Envíame una foto de un recibo o un extracto bancario en PDF.\n"
            "⏰ *Crea Recordatorios:* Dime 'recuérdame pagar la factura de internet el viernes'.\n"
            "📊 *Obtén Resúmenes:* Pide tus informes de gastos o ingresos semanales.\n\n"
            "Para desbloquear estas funciones, por favor crea tu cuenta escribiendo /register."
        ),
        "register_start": ("🚀 *¡Bienvenido al Registro de OkanAssist AI!*\n\n"
            "Necesito algunos detalles para crear tu cuenta.\n\n"
            "📧 *Por favor, introduce tu dirección de correo electrónico:*\n"
            "(Esto se utilizará para vincular tu cuenta)\n\n"
            "Escribe /cancel para detener el registro en cualquier momento."
        ),
        "validate_email": ("❌ Por favor, introduce una dirección de correo electrónico válida.\n"
                          "Ejemplo: tu.email@ejemplo.com"),
        "register_first_name": ( "✅ Email: {email}\n\n"
            "👤 *¿Cuál es tu nombre?*\n"
            "(Presiona /skip para usar: {first_name})"
        ),
        "register_last_name": ( "👤 *¿Cuál es tu apellido?*\n"
            "(Presiona /skip para continuar)"
        ),
        "register_timezone": ( "🕒 *¿Cuál es tu zona horaria?*\n\n"
            "Puedes decir cosas como `Soy de Madrid`, `Londres`, `hora del Pacífico` o `GMT+2`.\n\n"
            "Esto es crucial para que los recordatorios sean precisos."
        ),
        "register_confirmation": ("📋 *Por favor confirma tus datos:*\n\n"
            "📧 Email: {email}\n"
            "👤 Nombre: {first_name}"
            ),
        "register_confirmation_with_timezone": ("\n🌐 Idioma: {language}\n"
            "🕒 Zona horaria: {timezone}  _(Lo interpretaré automáticamente)_\n\n"
            "Escribe /confirm para crear tu cuenta.\n\n\n"
            "Escribe /cancel para empezar de nuevo."
        ),
        "invalid_confirmation": "❌ Respuesta inválida. Por favor escribe /confirm para crear tu cuenta o /cancel para empezar de nuevo.",
        "register_cancelled": "❌ Registro cancelado. Puedes empezar de nuevo en cualquier momento escribiendo /register.",
        "payment_success": "✅ ¡Pago exitoso! Ahora tienes acceso premium. Escribe /profile para ver tu estado.",
        "payment_failure": "❌ El pago falló o fue cancelado. Por favor intenta de nuevo con /upgrade o contacta soporte si el problema persiste.",
        "generic_error": "❌ Ocurrió un error. Por favor intenta más tarde o contacta soporte si el problema persiste.",
        "support_prompt": ("🛠️ *Modo Soporte*\n\n"
            "Por favor describe tu problema en detalle. Tu mensaje será enviado directamente a nuestro equipo de soporte.\n\n"
            "Escribe /cancel para salir del modo soporte."
        ),
        "support_message": ("💬 *Solicitud de Soporte Recibida*\n\n"
            "¡Gracias por contactarnos! Nuestro equipo de soporte te responderá lo antes posible.\n\n"
            "Mientras tanto, puedes visitar nuestra página de preguntas frecuentes o consultar /help para más información."
        ),
        "help_message": """
            🤖 *Ayuda del Bot OkanAssist*

            *💰 Transacciones*
            ¡Puedes gestionar tus finanzas simplemente hablando conmigo!

            • *Registrar transacciones:* "Gasté $25 en el almuerzo", "Recibí $3000 de salario"
            • *Obtener resúmenes:* "Muéstrame mis gastos de este mes", "¿Cuáles fueron mis ingresos de la semana pasada?"
            • *Generar informes en PDF:* "Necesito un informe de enero", "Genera un PDF de mis transacciones del mes pasado"

            *⏰ Recordatorios*
            Organiza tu vida con recordatorios inteligentes.

            • *Crear recordatorios:* "Recuérdame pagar las facturas mañana a las 3pm"
            • *Ver recordatorios:* "Muéstrame mis recordatorios urgentes", "¿Cuáles son mis tareas para hoy?"
            • *Completar recordatorios:* "Marcar los recordatorios de hoy como completados", "Eliminar los recordatorios de la semana pasada", "Eliminar todos los recordatorios"

            *📄 Procesamiento de Documentos*
            • Envía una foto de un recibo para registrar un gasto automáticamente.
            • Envía un extracto bancario en PDF para importar transacciones en bloque.

            *🎯 Comandos*
            /start - Empezar o iniciar sesión
            /register - Crear tu cuenta
            /help - Mostrar este mensaje de ayuda
            /upgrade - Obtener acceso ilimitado
            /profile - Ver tu perfil


            ¡Solo háblame de forma natural, yo te entiendo! 🎉
    """,
        "generic_downtime": "⚠️ El servicio está experimentando problemas. Por favor intenta más tarde o contacta soporte si el problema persiste.",
        "user_not_found": "🔐 Usuario no encontrado. Por favor regístrate primero escribiendo /register.\n",
        "profile_info": (
                            "👤 *Tu Perfil*\n\n"
                            "📧 Email: {email}\n"
                            "👤 Nombre: {name}\n"
                            "🌐 Idioma: {language}\n"
                            "💰 Moneda: {currency}\n"
                            "⏰ Zona horaria: {timezone}\n"
                            "🔗 URL de WebApp: {webapp_url}\n"
                            "⭐ Premium: {premium_status}\n"
                        ),
        "manage_url": "🔗 [Gestiona tu suscripción aquí]({url})",
        
        "commands": {
            "start": {"name": "start", "description": "Comienza a usar el asistente"},
            "register": {"name": "register", "description": "Registra tu cuenta"},
            "help": {"name": "help", "description": "Obtén ayuda y ejemplos"},
            "balance": {"name": "balance", "description": "Ver resumen financiero"},
            "reminders": {"name": "reminders", "description": "Mostrar recordatorios pendientes"},
            "profile": {"name": "profile", "description": "Ver tu perfil"},
            "upgrade": {"name": "upgrade", "description": "Mejorar a Premium"},
            "support": {"name": "support", "description": "Contactar soporte"},
        },
        "generic_maintenance": "⚠️ Esta función está actualmente en mantenimiento. Por favor intenta más tarde.",
        "upgrade_link_generation": "⏳ Generando tu enlace personal de mejora, por favor aguarde...\n",
        "portal_return": "🔗 *Bienvenido de vuelta a OkanAssist!*\n\nHas regresado exitosamente del portal. ¿Cómo puedo asistirte hoy?\n\nEscribe /help para ver ejemplos."
    },
    "pt": {
        "welcome_authenticated": (
            "👋 *Olá {name}!*\n\n"
            "Como posso te ajudar hoje? Você pode registrar despesas, gerenciar lembretes e ver resumos.\n\n"
            "Digite /help para ver exemplos."
        ),
        "welcome_unauthenticated": (
            "👋 *Bem-vindo ao OkanAssist!* Seu assistente financeiro pessoal.\n\n"
            "Eu uso IA para te ajudar a controlar suas finanças sem esforço. Veja o que você pode fazer:\n\n"
            "💸 *Monitore Transações:* Apenas diga 'gastei R$15 no almoço' ou 'recebi R$500 de salário'.\n"
            "📸 *Processe Documentos:* Envie-me a foto de um recibo ou um extrato bancário em PDF.\n"
            "⏰ *Crie Lembretes:* Diga-me 'lembre-me de pagar a conta de internet na sexta-feira'.\n"
            "📊 *Obtenha Resumos:* Peça seus relatórios de gastos ou receitas semanais.\n\n"
            "Para desbloquear esses recursos, por favor, crie sua conta digitando /register."
        ),
        "register_start": ("🚀 *Bem-vindo ao Registro do OkanAssist AI!*\n\n"
            "Preciso de alguns detalhes para criar sua conta.\n\n"
            "📧 *Por favor, insira seu endereço de e-mail:*\n"
            "(Isso será usado para vincular sua conta)\n\n"
            "Digite /cancel para parar o registro a qualquer momento."
        ),
        "validate_email": ("❌ Por favor, insira um endereço de e-mail válido.\n"
                          "Exemplo: seu.email@exemplo.com"),
        "register_first_name": ( "✅ Email: {email}\n\n"
            "👤 *Qual é o seu primeiro nome?*\n"
            "(Digite /skip para usar: {first_name})"
        ),
        "register_last_name": ( "👤 *Qual é o seu sobrenome?*\n"
            "(Digite /skip para continuar)"
        ),
        "register_timezone": ( "🕒 *Qual é o seu fuso horário?*\n\n"
            "Você pode dizer coisas como `Sou de São Paulo`, `Lisboa`, `horário do Pacífico` ou `GMT+2`.\n\n"
            "Isso é crucial para que os lembretes sejam precisos."
        ),
        "register_confirmation": ("📋 *Por favor, confirme seus dados:*\n\n"
            "📧 Email: {email}\n"
            "👤 Nome: {first_name}"
            ),
        "register_confirmation_with_timezone": ("\n🌐 Idioma: {language}\n"
            "🕒 Fuso horário: {timezone}  _(Vou interpretar automaticamente)_\n\n"
            "Digite /confirm para criar sua conta.\n\n\n"
            "Digite /cancel para começar novamente."
        ),
        "invalid_confirmation": "❌ Resposta inválida. Por favor, digite /confirm para criar sua conta ou /cancel para começar novamente.",
        "register_cancelled": "❌ Registro cancelado. Você pode começar novamente a qualquer momento digitando /register.",
        "payment_success": "✅ Pagamento realizado com sucesso! Agora você tem acesso premium. Digite /profile para ver seu status.",
        "payment_failure": "❌ O pagamento falhou ou foi cancelado. Por favor, tente novamente com /upgrade ou entre em contato com o suporte se o problema persistir.",
        "generic_error": "❌ Ocorreu um erro. Por favor, tente novamente mais tarde ou entre em contato com o suporte se o problema persistir.",
        "support_prompt": ("🛠️ *Modo Suporte*\n\n"
            "Por favor, descreva seu problema em detalhes. Sua mensagem será enviada diretamente para nossa equipe de suporte.\n\n"
            "Digite /cancel para sair do modo suporte."
        ),
        "support_message": ("💬 *Solicitação de Suporte Recebida*\n\n"
            "Obrigado por entrar em contato! Nossa equipe de suporte responderá o mais breve possível.\n\n"
            "Enquanto isso, você pode visitar nossa página de FAQ ou consultar /help para mais informações."
        ),
        "help_message": """
            🤖 *Ajuda do Bot OkanAssist*

            *💰 Transações*
            Você pode gerenciar suas finanças apenas conversando comigo!

            • *Registrar transações:* "Gastei R$25 no almoço", "Recebi R$3000 de salário"
            • *Obter resumos:* "Mostre meus gastos deste mês", "Qual foi minha receita da semana passada?"
            • *Gerar relatórios em PDF:* "Preciso de um relatório de janeiro", "Gere um PDF das minhas transações do mês passado"

            *⏰ Lembretes*
            Organize sua vida com lembretes inteligentes.

            • *Criar lembretes:* "Lembre-me de pagar as contas amanhã às 15h"
            • *Ver lembretes:* "Mostre meus lembretes urgentes", "Quais são minhas tarefas para hoje?"
            • *Concluir lembretes:* "Marcar os lembretes de hoje como concluídos", "Limpar os lembretes da semana passada", "Limpar todos os lembretes"

            *📄 Processamento de Documentos*
            • Envie uma foto de um recibo para registrar uma despesa automaticamente.
            • Envie um extrato bancário em PDF para importação de transações em massa.

            *🎯 Comandos*
            /start - Começar ou fazer login
            /register - Criar sua conta
            /help - Mostrar esta mensagem de ajuda
            /upgrade - Obter acesso ilimitado
            /profile - Ver seu perfil

            Apenas fale comigo naturalmente - eu entendo! 🎉
    """,
        "generic_downtime": "⚠️ O serviço está enfrentando problemas. Por favor, tente novamente mais tarde ou entre em contato com o suporte se o problema persistir.",
        "user_not_found": "🔐 Usuário não encontrado. Por favor, registre-se primeiro digitando /register.\n",
        "profile_info": (
                            "👤 *Seu Perfil*\n\n"
                            "📧 Email: {email}\n"
                            "👤 Nome: {name}\n"
                            "🌐 Idioma: {language}\n"
                            "💰 Moeda: {currency}\n"
                            "⏰ Fuso horário: {timezone}\n"
                            "🔗 URL da WebApp: {webapp_url}\n"
                            "⭐ Premium: {premium_status}\n"
                        ),
        "manage_url": "🔗 Gerencie sua assinatura aqui: {url}",
        "commands": {
            "start": {"name": "start", "description": "Comece a usar o assistente"},
            "register": {"name": "register", "description": "Registre sua conta"},
            "help": {"name": "help", "description": "Obtenha ajuda e exemplos"},
            "balance": {"name": "balance", "description": "Ver resumo financeiro"},
            "reminders": {"name": "reminders", "description": "Mostrar lembretes pendentes"},
            "profile": {"name": "profile", "description": "Ver seu perfil"},
            "upgrade": {"name": "upgrade", "description": "Atualizar para Premium"},
            "support": {"name": "support", "description": "Contatar suporte"},
        },
        "generic_maintenance": "⚠️ Este recurso está atualmente em manutenção. Por favor, tente novamente mais tarde.",
        "upgrade_link_generation": "⏳ Gerando seu link pessoal de upgrade, por favor aguarde...\n",
        "portal_return": "🔗 *Bem-vindo de volta ao OkanAssist!*\n\nVocê retornou com sucesso do portal. Como posso te ajudar hoje?\n\nDigite /help para ver exemplos."
    }
}


def get_message(key: str, lang: str, **kwargs) -> str:
    """Gets a translated message, falling back to English."""
    lang_short = lang.split('-')[0] if lang else 'en'
    
    # Fallback to 'en' if language or key is not found
    messages = MESSAGES.get(lang_short, MESSAGES['en'])
    message_template = messages.get(key, MESSAGES['en'].get(key, "Message key not found."))
    
    return message_template.format(**kwargs)