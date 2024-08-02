import config


answer_texts = {
    'ru': {
        'main': """
Добро пожаловать! Kaba Bot - это доступ к передовым возможностями искусственного интеллекта! А также:

🌍 Бот популярен в разных странах мира.

🗂 Работа с файлами и изображениями, а скоро и с видео.

📈 Доступ только к самым последним версиям GPT, DALL-E и других моделей.

💵 Пополните на любую сумму, хоть равную стоимости бутылки воды, и начните пользоваться ботом.

✋ Ежедневно 5 бесплатных запросов.
""",
        'more': "Выберите опцию",
        'referral': """
📢 Реферальная программа
➖➖➖➖➖➖➖➖➖➖➖
🎉 Вы пригласили {} новых пользователей
💵 и получили за их траты ${}!
‍
📋 Условия: За каждого приглашенного пользователя вы получаете 10% от всех его расходов!
‍
🔗 Ваша реферальная ссылка:
{}
""",
        'settings': 'Настройки ИИ',
        'first_promt': '📝 Отправьте текст новых инструкций по ответу',
        'first_promt_ok': '✅ Теперь вы используете новые инструкций по ответу',
        'second_promt': '📝 Отправьте текст нового описания желаемого ответа',
        'second_promt_ok': '✅ Теперь вы используете новое описание желаемого ответа',
        'see_promts': """
📋 Текущие инструкции по ответу:
{}

📋 Текущее описание желаемого ответа:
{}
""",
        'set_default_promt': '✅ Значение промптов "Инструкции по ответу" и "Описание желаемого ответа" установлены по умолчанию',
        'info': 'Справочник',
        'token': """
🔤 Что такое токены в GPT
➖➖➖➖➖➖➖➖➖➖➖
Токены в GPT представляют собой единицы текста, которые могут быть символами, словами или частями слов. Рассмотрим пример фразы "Hello world!":

"Hello" разбивается на 1 токен: ["Hello"]
"world!" разбивается на 2 токена: ["world", "!"]

Таким образом, "Hello world!" состоит из 3 токенов.
""",
        'settings_ai': """
📋 Что такое настройки ИИ?
➖➖➖➖➖➖➖➖➖➖➖
Описание желаемого ответа — это четкие и конкретные указания, что требуется получить в ответе. Чем точнее описание, тем более релевантный и полезный будет результат.
‍
Инструкции по ответу — это набор правил и требований, которые языковая модель должна соблюдать при создании ответа. Эти инструкции помогают настроить модель на определенный стиль, формат и содержание ответа, чтобы удовлетворить запрос пользователя.
""",
        'usage_ai': """
🤖 Описание наших ИИ
➖➖➖➖➖➖➖➖➖➖➖
1. GPT-4o mini
📚 Легкая версия ИИ для повседневных задач.
🎯 Идеально для быстрых и несложных запросов. Может обрабатывать файлы.
💰 Токены для GPT-4o mini стоят примерно в 25 раз дешевле, чем для GPT-4o.

2. GPT-4o
📚 Мощная версия ИИ для сложных задач. 
🎯 Подходит для глубоких и детализированных запросов. Может обрабатывать файлы.

3. DALL·E 3
📚 ИИ для создания изображений.
""",
        'actual_ai': """
🔄 Мы принципиально используем только самые последние версии ИИ. Если новейшие версии недоступны, то не внедряем ИИ вовсе.
""",
        'bot_benefit': """
Оценка выгоды
➖➖➖➖➖➖➖➖➖➖➖
💸 Оплата в "Kaba Bot" осуществляется за токены.

🤔 Если вы ежедневно отправляете сотни больших запросов и ответов, выгоднее использовать ChatGPT с фиксированной подпиской.

💡 В остальных случаях, экономичнее использовать "Kaba Bot" с оплатой за токены.
""",
        'feedback_1': "🙏 Будем благодарны за обратную связь! Пока только в формате текста.",
        'feedback_2': "Благодарим за обратную связь!",
        'dialogue': "Выберите диалог",
        'inner_dialogue': """
Просто отправьте сообщение и ИИ вам ответит
⚙️ Настройки диалога:

• ИИ: {}
• Название: {}

🔧 При желании вы можете изменить настройки диалога.
""",
        'create_new_chat': """
⚙️ Настройки диалога по умолчанию:

• ИИ: {}
• Название: {}

🔧 При желании вы можете изменить настройки диалога.
""",
        'change_name_1': "📝 Введите новое название диалога (до 40 символов)",
        'change_name_2': "✅ Новое название диалога успешно применено",
        'change_model': "Выберите ИИ",
        'not_enough_money': "Недостаточно средств",
        'wallet': """
Кошелек
➖➖➖➖➖➖➖➖➖➖➖
💳 Баланс

На кошельке: ${}.
От реферальной программы: ${}.
➖➖➖➖➖➖➖➖➖➖➖
📊 Доступные токены

GPT-4o: {} токенов.
GPT-4o mini: {} токенов.
DALL·E 3: {} генераций.
➖➖➖➖➖➖➖➖➖➖➖
ℹ️ Не знаешь, что это значит? нажми на это 👇
/info 
/referral
""",
        'payment_1': 'Введите сумму в ₽',

    },
    'en': {

    }
}

btn_texts = {
    'ru': {
        'dialogue': 'Диалоги',
        'wallet': 'Кошелёк',
        'more': 'Ещё',
        'referral': 'Реферальная программа',
        'settings': 'Настройки ИИ',
        'info': 'Справочник',
        'feedback': 'Обратная связь',
        'back': 'Назад ⬅',
        'first_promt': 'Изменить инструкции по ответу',
        'second_promt': 'Изменить описание желаемого ответа',
        'see_promts': 'Увидеть текущие настройки',
        'set_default_promt': 'Установить по умолчанию',
        'token': 'Токены',
        'settings_ai': 'Настройки ИИ',
        'usage_ai': 'Используемые ИИ',
        'actual_ai': 'Актуальность ИИ',
        'bot_benefit': 'Выгода от использования бота',
        'create_new_chat': 'Создать',
        'change_name': 'Сменить название',
        'show_history': 'Показать историю',
        'del_d': 'Удалить диалог',
        'change_model': 'Сменить ИИ',
        'gpt-4o': 'GPT-4o (для сложных задач)',
        'gpt-4o-mini': 'GPT-4o mini (для повседневных задач)',
        'dall-e-3': 'DALL·E 3 (для создания изображений)',
        'payment_1': 'Пополнить банковской картой',
        'payment_2': 'Пополнить криптовалютой'
    },
    'en': {

    }
}