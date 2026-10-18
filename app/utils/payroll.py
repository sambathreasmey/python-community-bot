import random
from datetime import date, datetime, time, timedelta, timezone

CAMBODIA_TIMEZONE = timezone(timedelta(hours=7), "Asia/Phnom_Penh")

_MESSAGE_TEMPLATES = (
    "🎉 សល់តែ {time} ទៀត ដល់ថ្ងៃបើកប្រាក់ខែហើយ! ចាំទៅជប់លៀងជាមួយក្រុមការងារ 🥂",
    "⏳ ចាំបន្តិចទៀត! {time} ទៀត ប្រាក់ខែចូលហើយ 🤑",
    "💵 រង់ចាំបន្តិចសិន! សល់តែ {time} ទៀត ដល់ថ្ងៃបើកប្រាក់ខែហើយ 🏦",
    "🕐 ត្រៀមខ្លួន! {time} ទៀត ប្រាក់ខែចូលហើយ 🥳",
    "💸 ជិតដល់ថ្ងៃបើកប្រាក់ខែហើយ! នៅសល់តែ {time} ទៀតប៉ុណ្ណោះ ✨",
    "🍻 សល់ {time} ទៀត បើកប្រាក់ខែរួច ទៅ Party ជាមួយក្រុម!",
    "🥳 រង់ចាំបន្តិច! {time} ទៀត បើកប្រាក់ខែហើយ 🎊",
    "💼 សល់ {time} ទៀត ចាំទៅទទួលប្រាក់ខែជាមួយមិត្តរួមការងារ! 🤝",
    "🌟 {time} ទៀតប៉ុណ្ណោះ! ប្រាក់ខែជិតចូលហើយ 💰",
    "🏦 ធនាគារកំពុងរង់ចាំ! {time} ទៀត ប្រាក់ខែចូលហើយ 😄",
)

_EMOTION_LINES = (
    (95, ("🔥 ជិតដល់ហើយ! តស៊ូតែបន្តិចទៀតទេ!", "🎯 ស្ទើរតែដល់គោលដៅហើយ!")),
    (80, ("😆 ជិតដល់ហើយ អត់ធ្មត់បានយ៉ាងល្អ!", "🥰 ចង់ Party ណាស់ហើយ!")),
    (60, ("🙂 ហួសពាក់កណ្ដាលផ្លូវហើយ!", "🌤️ ចាប់ផ្ដើមមើលឃើញពន្លឺនៃជ័យជំនះហើយ!")),
    (40, ("💪 កំពុងទៅមុខយ៉ាងល្អ បន្តដំណើរទៀត!", "🚶 ដើរបានពាក់កណ្ដាលហើយ!")),
    (20, ("😅 ចាប់ផ្ដើមទៅមុខហើយ បន្ថែមល្បឿនបន្តិចទៀត!", "☕ ក្រេបកាហ្វេមួយកែវ ហើយបន្តដំណើរ!")),
    (0, ("😴 ទើបតែចាប់ផ្ដើមទេ ផ្លូវនៅឆ្ងាយទៀត...", "🐢 ទៅមុខយឺតៗ ព្រោះទើបតែចាប់ផ្ដើម!")),
)


def _shift_month(month_start: date, offset: int) -> date:
    month_index = month_start.year * 12 + month_start.month - 1 + offset
    year, month_index = divmod(month_index, 12)
    return date(year, month_index + 1, 1)


def _adjust_weekend(payday: date) -> date:
    if payday.weekday() == 5:
        return payday - timedelta(days=1)
    if payday.weekday() == 6:
        return payday - timedelta(days=2)
    return payday


def _paydays_around(current_date: date) -> list[date]:
    month_start = current_date.replace(day=1)
    return [
        _adjust_weekend(_shift_month(month_start, offset).replace(day=day))
        for offset in (-2, -1, 0, 1)
        for day in (12, 26)
    ]


def _format_duration(delta: timedelta) -> str:
    total_seconds = int(delta.total_seconds())
    days, remainder = divmod(total_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    if days:
        return f"<b>{days}</b>ថ្ងៃ <b>{hours:02d}</b>ម៉ោង <b>{minutes:02d}</b>នាទី <b>{seconds:02d}</b>វិនាទី"
    if hours:
        return f"<b>{hours}</b>ម៉ោង <b>{minutes:02d}</b>នាទី <b>{seconds:02d}</b>វិនាទី"
    if minutes:
        return f"<b>{minutes}</b>នាទី <b>{seconds:02d}</b>វិនាទី"
    return f"<b>{seconds}</b>វិនាទី"


def build_payroll_message(now: datetime | None = None) -> str:
    if now is None:
        now = datetime.now(CAMBODIA_TIMEZONE)
    elif now.tzinfo is None:
        raise ValueError("now must include a timezone")
    else:
        now = now.astimezone(CAMBODIA_TIMEZONE)

    current_date = now.date()
    paydays = _paydays_around(current_date)

    if current_date in paydays:
        return (
            "🎉🎉 អបអរសាទរ! ថ្ងៃនេះជាថ្ងៃបើកប្រាក់ខែហើយ 💰\n"
            "សូមរីករាយជាមួយក្រុមការងារ 🥳🥂\n\n"
            "▓▓▓▓▓▓▓▓▓▓ 100% 🎆 ថ្ងៃនេះជាថ្ងៃរបស់អ្នកហើយ! 🎆"
        )

    previous_payday = max(day for day in paydays if day < current_date)
    next_payday = min(day for day in paydays if day > current_date)
    previous_payday_at = datetime.combine(
        previous_payday, time.min, tzinfo=CAMBODIA_TIMEZONE
    )
    next_payday_at = datetime.combine(next_payday, time.min, tzinfo=CAMBODIA_TIMEZONE)
    total_seconds = (next_payday_at - previous_payday_at).total_seconds()
    elapsed_seconds = (now - previous_payday_at).total_seconds()
    progress = max(0, min(100, int(elapsed_seconds / total_seconds * 100)))
    filled = round(progress / 10)
    progress_bar = f"{'▓' * filled}{'░' * (10 - filled)} {progress}%"
    emotion_line = next(
        random.choice(lines)
        for threshold, lines in _EMOTION_LINES
        if progress >= threshold
    )
    countdown = _format_duration(next_payday_at - now)
    message = random.choice(_MESSAGE_TEMPLATES).format(time=countdown)
    return f"{message}\n\n{progress_bar} {emotion_line}"
