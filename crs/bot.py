#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
logging.basicConfig(level=logging.CRITICAL)  # Ничего не пишем в консоль
logging.getLogger("httpx").setLevel(logging.WARNING)  # Отключаем HTTP-логи
# ----------------------------- НАСТРОЙКИ -----------------------------
# СЮДА ВСТАВЬТЕ СВОЙ ТОКЕН ОТ @BotFather
BOT_TOKEN = "7987583865:AAFbYXM3R90ViM_VfCiNiPogrxBm85aEWZg"

# Включим логирование для отладки
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# --------------------------- ТЕКСТЫ РАЗДЕЛОВ --------------------------

TEXTS = {
    "start": (
        "📱 *Добро пожаловать!*\n\n"
        "Я — бот-визитка проекта\n"
        "«*Инструмент для переноса и объединения онлайн-медиатек*»\n\n"
        "📍 Москва, 2026 г.\n\n"
        "Проект направлен на автоматизацию переноса "
        "структурированных медиаданных (музыки) "
        "между различными облачными сервисами.\n\n"
        "Используйте кнопки ниже, чтобы узнать подробности 👇"
    ),
    
    "about": (
        "*📌 О проекте*\n"
        "*Инструмент для переноса и объединения онлайн-медиатек*\n\n"
        "*Цель проекта:*\n"
        "Цель проекта — разработка программного обеспечения, "
        "автоматизирующего процесс переноса музыкальных данных "
        "между различными облачными сервисами с сохранением "
        "структуры метаданных.\n\n"
        "*Почему это важно:*\n"
        "Стриминговые платформы функционируют как закрытые экосистемы. "
        "Пользовательские данные (плейлисты, избранные треки, "
        "история прослушивания) привязаны к конкретному сервису "
        "и не могут быть напрямую перенесены в другую систему.\n\n"
        "*Основные задачи:*\n"
        "• Определить архитектуру инструмента и технических решений\n"
        "• Распределить задачи в группе\n"
        "• Разработать инструмент\n"
        "• Протестировать продукт"
    ),
    
    "problem": (
        "*⚠️ Проблематика проекта*\n\n"
        "Сегодня пользователи используют разные музыкальные платформы "
        "для прослушивания музыки и хранения плейлистов.\n"

        "При переходе с одного сервиса на другой часто люди не могут "
        "перености медиатеки и сохраненть любимые треки.\n\n"

        "*Основная проблема:* большинство платформ не поддерживают "
        "удобный перенос плейлистов и музыкальных данных между сервисами. "
        "Из-за этого пользователям приходится переносить музыку вручную, "
        "что занимает много времени и является неудобным. \n\n"
        
    ),
    
    "solution": (
        "*🛠 Описание приложения и его алгоритма*\n\n"
        "Приложение разработано на языке *Python* с использованием "
        "графического фреймворка *PySide6*, что обеспечивает "
        "удобный интерфейс и поддерживает работу"
        "с различными музыкальными сервисами.\n\n"
        "📂 *Структура проекта разделена на несколько частей:*\n"
        "• *Model* — работа с музыкальными сервисами;\n"
        "• *View* — интерфейс приложения;\n"
        "• *ViewModel* — обработка логики и команд.\n\n"
        "🚀 *Основной алгоритм работы:*\n"
        "1) Пользователь выбирает музыкальный сервис\n"
        "2) Выполняет авторизацию\n"
        "3) Выбирает плейлист или медиатеку\n"
        "4) Указывает сервис для переноса\n"
        "5) Запускает перенос данных\n\n"

        "📊 Во время переноса отображается "
        "статистика и прогресс выполнения."
    ),
    
    "team": (
        "👥 *Участники проекта*\n\n"

        "💻 *Разработчики*\n"
        "• Антоненко Тимофей Ильич — 251-366\n"
        "• Артамонов Ярослав Вадимович — 251-363\n"
        "• Богданов Тимофей Александрович — 251-361\n"
        "• Железнов Александр Денисович — 251-332\n"
        "• Коньков Павел Александрович — 251-332\n"
        "• Павленко Иван Константинович — 251-361\n"
        "• Рудаков Артём Евгеньевич — 251-325\n"
        "• Спиридонов Руслан Андреевич — 251-325\n"
        "• Трофимов Сергей Дмитриевич — 251-361\n"
        "• Шуваев Сергей Дмитриевич — 251-361\n\n"

        "🎨 *Дизайнеры*\n"
        "• Бибяева Анастасия Алексеевна — 251-361\n"
        "• Красильникова Мария Андреевна — 251-672\n"
        "• Трошина Татьяна Евгеньевна — 251-672\n"
        "• Хоркина Варвара Андреевна — 251-361\n"
        "• Зварыч Диана Евгеньевна — 251-332\n\n"

        "📝 *Составители пояснительной записки*\n"
        "• Волкова Полина Андреевна — 251-363\n"
        "• Галенко Маргарита Максимовна — 251-363\n"
        "• Жакупов Данияр Бисултанович — 251-332\n"
        "• Иванов Максим Сергеевич — 251-634\n"
        "• Кулешова Диана Алексеевна — 251-011\n"
        "• Улегина Полина Владимировна — 251-351\n"
        "• Шабурова Мария Александровна — 251-011\n\n"

        "📊 *Составители презентации*\n"
        "• Егорова Василиса Вячеславовна — 251-332\n"
        "• Чужбинина Светлана Николаевна — 251-011\n\n"

        "⏸ *Участники в заморозке*\n"
        "• Бардова Алина Дмитриевна — 251-332\n"
        "• Винокурова София Алексеевна — 251-363\n"
        "• Малахов Денис Евгеньевич — 251-332\n"
        "• Никифоров Вадим Владиславович — 251-361\n"
        "• Ползиков Никита Александрович — 251-332"
    ),
    
    "status": (
        "📈 *Статус разработки проекта*\n\n"

        "На текущий момент проект находится в активной стадии разработки, "
        "и основные ключевые этапы уже выполнены.\n\n"

        "✅ *Выполненные этапы:*\n\n"

        "• *Определена архитектура приложения*\n"
        "  Выбрана архитектура MVVM, которая разделяет проект на логические слои:\n"
        "  — Model (работа с данными и сервисами)\n"
        "  — View (пользовательский интерфейс)\n"
        "  — ViewModel (связующее звено и логика приложения)\n\n"

        "• *Выбран технологический стек проекта*\n"
        "  Подобраны основные технологии для реализации системы:\n"
        "  — Python как основной язык разработки\n"
        "  — PySide6 для создания графического интерфейса\n"
        "  — API музыкальных сервисов для взаимодействия с платформами\n\n"

        "• *Разработан основной инструмент проекта*\n"
        "  Реализована базовая логика переноса медиатек между сервисами:\n"
        "  — подключение к внешним API\n"
        "  — получение списка плейлистов\n"
        "  — обработка и сопоставление треков\n"
        "  — подготовка структуры для переноса данных\n\n"

        "• *Проведена работа над дизайном интерфейса*\n"
        "  — выполнен анализ существующих решений и конкурентов\n"
        "  — разработан пользовательский сценарий (user flow)\n"
        "  — определена структура экранов и навигации\n"
        "  — сформирован UI-kit (кнопки, стили, элементы интерфейса)\n"
        "  — проработан единый визуальный стиль проекта\n\n"

        "🔄 *Текущий этап:*\n\n"
        "  — Проведение тестирования системы\n"
        "  — Исправление найденных ошибок\n"
        "  — Улучшение стабильности и оптимизация работы приложения\n\n"

        "🚀 *Проект находится на стадии финальной доработки и подготовки к завершению.*"
    ),
    
    "help": (
        "*🆘 Помощь и контакты*\n\n"
        "По всем вопросам о проекте вы можете обратиться к разработчикам бота:\n\n"
        "Telegram: @iterationtools\n\n"
        "Доступные команды:\n"
        "/start — главное меню\n"
        "/about — о проекте\n"
        "/problem — описание проблематики\n"
        "/solution — алгоритм приложения\n"
        "/team — состав команды\n"
        "/status — статус разработки\n"
        "/help — эта справка"
    )
}

# ------------------------- КЛАВИАТУРЫ (кнопки) -------------------------

def get_main_keyboard():
    """Главная inline-клавиатура"""
    keyboard = [
        [InlineKeyboardButton("📌 О проекте", callback_data="about")],
        [InlineKeyboardButton("⚠️ Проблематика проекта", callback_data="problem")],
        [InlineKeyboardButton("🛠 Алгоритм приложения", callback_data="solution")],
        [InlineKeyboardButton("👥 Команда проекта", callback_data="team")],
        [InlineKeyboardButton("📊 Статус разработки", callback_data="status")],
        [InlineKeyboardButton("🆘 Помощь", callback_data="help")],
    ]
    return InlineKeyboardMarkup(keyboard)

# ------------------------ ОБРАБОТЧИКИ КОМАНД ---------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user = update.effective_user
    await update.message.reply_text(
        f"{TEXTS['start']}",
        parse_mode="Markdown",
        reply_markup=get_main_keyboard()
    )

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик /about"""
    await update.message.reply_text(
        TEXTS["about"],
        parse_mode="Markdown",
        reply_markup=get_main_keyboard()
    )

async def problem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик /problem"""
    await update.message.reply_text(
        TEXTS["problem"],
        parse_mode="Markdown",
        reply_markup=get_main_keyboard()
    )

async def solution(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик /solution"""
    await update.message.reply_text(
        TEXTS["solution"],
        parse_mode="Markdown",
        reply_markup=get_main_keyboard()
    )

async def team(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик /team"""
    await update.message.reply_text(
        TEXTS["team"],
        parse_mode="Markdown",
        reply_markup=get_main_keyboard()
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик /status"""
    await update.message.reply_text(
        TEXTS["status"],
        parse_mode="Markdown",
        reply_markup=get_main_keyboard()
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик /help"""
    await update.message.reply_text(
        TEXTS["help"],
        parse_mode="Markdown",
        reply_markup=get_main_keyboard()
    )

# ---------------------- ОБРАБОТЧИК НАЖАТИЙ КНОПОК -----------------------

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает нажатия на inline-кнопки"""
    query = update.callback_query
    await query.answer()  # убираем "часики" на кнопке
    
    callback_data = query.data
    
    if callback_data in TEXTS:
        await query.edit_message_text(
            text=TEXTS[callback_data],
            parse_mode="Markdown",
            reply_markup=get_main_keyboard()
        )
    else:
        await query.edit_message_text(
            text="❌ Раздел не найден. Используйте кнопки меню.",
            reply_markup=get_main_keyboard()
        )

# ----------------------------- ЗАПУСК БОТА -----------------------------

def main():
    """Запуск бота"""
    # Создаём приложение
    application = Application.builder().token(BOT_TOKEN).build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("about", about))
    application.add_handler(CommandHandler("problem", problem))
    application.add_handler(CommandHandler("solution", solution))
    application.add_handler(CommandHandler("team", team))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CommandHandler("help", help_command))

    # Регистрируем обработчик нажатий на кнопки
    application.add_handler(CallbackQueryHandler(button_callback))

    # Запускаем бота
    print("Бот запущен... Нажмите Ctrl+C для остановки")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
