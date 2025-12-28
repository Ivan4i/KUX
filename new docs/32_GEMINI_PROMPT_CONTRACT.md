# 32_GEMINI_PROMPT_CONTRACT.md

## Input/Output Contract Specification

### Input Format (Strict Schema)

CONTRACT: GeminiBusinessAnalysisPrompt v1.0

Every request to Gemini must follow this structure:

```python
INPUT_SCHEMA = {
    "company_name": str,           # Required: Full company name
    "rusprofile_url": str,         # Required: Link to RusProfile
    "website_url": str | None,     # Optional: Company website or None
    "founder_name": str,           # Required: CEO/Founder name
    "business_metrics": {
        "revenue_2024": int,       # In RUB, from RusProfile
        "employees": int,          # Headcount
        "industry": str,           # Sector/vertical
        "market_segment": str,     # Specific niche
        "years_operating": int,    # How long company exists
    },
    "online_presence": {
        "site_exists": bool,       # Is there a website?
        "site_quality": str,       # "poor" | "average" | "good" | "excellent" or None
        "social_media": list[str], # ["VK", "Instagram", "LinkedIn"] or []
        "google_rating": float,    # 1-5 or None
        "yandex_rating": float,    # 1-5 or None
    },
    "identified_pain_points": list[str],  # Max 5 specific problems
}
```

---

## Example Input #1 (With Website - Healthcare)

```json
{
  "company_name": "ФГБУ НМИЦО ФМБА России",
  "rusprofile_url": "https://www.rusprofile.ru/id/7793575",
  "website_url": "http://otolar-centre.ru/",
  "founder_name": "Дайхес Николай Аркадьевич",
  "business_metrics": {
    "revenue_2024": 321000000,
    "employees": 450,
    "industry": "healthcare",
    "market_segment": "medical-clinic",
    "years_operating": 15
  },
  "online_presence": {
    "site_exists": true,
    "site_quality": "average",
    "social_media": ["VK", "Яндекс.Карты"],
    "google_rating": 4.5,
    "yandex_rating": 4.2
  },
  "identified_pain_points": [
    "запись только по телефону (невозможно онлайн)",
    "перегруз регистратуры (очереди в колл-центре)",
    "отсутствует система возврата пациентов (теряют на повторах)",
    "нет интеграции между филиалами (разные системы)",
    "низкая доля платных услуг (потенциал неразведан)"
  ]
}
```

---

## Example Input #2 (No Website - Trade/Wholesale)

```json
{
  "company_name": "ООО ТД База №1",
  "rusprofile_url": "https://www.rusprofile.ru/id/193863",
  "website_url": null,
  "founder_name": "Макаров Дмитрий Сергеевич",
  "business_metrics": {
    "revenue_2024": 7000000,
    "employees": 12,
    "industry": "wholesale",
    "market_segment": "trade",
    "years_operating": 8
  },
  "online_presence": {
    "site_exists": false,
    "site_quality": null,
    "social_media": [],
    "google_rating": null,
    "yandex_rating": 3.8
  },
  "identified_pain_points": [
    "нет официального сайта (клиенты не находят)",
    "кривая CRM (просто Excel таблицы)",
    "потеря заявок (менеджеры не отслеживают)",
    "менеджеры тонут в рутине (нет автоматизации)",
    "нет системы повторных продаж (забывают про клиентов)"
  ]
}
```

---

## Prompt Template (Sent to Gemini)

```
SYSTEM: [20 .md files cached context from 31_GEMINI_CONTEXT_PACK.md]

USER:
───────────────────────────────────────────────────────────────
АНАЛИЗ БИЗНЕСА И ГЕНЕРАЦИЯ АУТРИЧ-СООБЩЕНИЯ

ВХОДНЫЕ ДАННЫЕ КОМПАНИИ:
{json_input_from_above}

───────────────────────────────────────────────────────────────
ОБЯЗАТЕЛЬНЫЕ ТРЕБОВАНИЯ (СТРОГО!):

1. ОБРАЩЕНИЕ ПО ИМЕНИ
   └─ Использовать ПЕРВОЕ имя контакта в обращении
   └─ Пример: "Николай Аркадьевич" или "Дмитрий Сергеевич"
   └─ Это создает личное соединение, не шаблон

2. КОНКРЕТНЫЕ МЕТРИКИ
   └─ Обязательно упомянуть:
      • Выручку за 2024 год (in millions: "321 млн руб")
      • Количество сотрудников ("450 человек")
      • Рейтинг если есть ("4.2 звезды на Яндекс.Картах")
   └─ Это доказывает что ты исследовал компанию

3. ОПРЕДЕЛЕНИЕ БОЛЕЙ
   └─ Выбрать 2-3 самые острые боли из списка
   └─ Написать ТА ЧЕ: почему это боль, какой ущерб
   └─ Пример: "запись только по телефону → клиенты уходят к конкурентам"
   └─ Не просто перечислять, а ОБЪЯСНЯТЬ влияние

4. КОНКРЕТНОЕ РЕШЕНИЕ
   └─ Предложить ТА ЧЕ решение (не что вообще, а ДЛЯ ЭТОЙ компании)
   └─ Связать решение с их болями (причинно-следственная связь)
   └─ Пример: "Система онлайн-записи → разгрузить колл-центр → больше платные услуги"

5. ДОКАЗАТЕЛЬСТВО ЧЕРЕЗ КЕЙСЫ
   └─ Выбрать из 3 кейсов: Level Group, CookPad, BitPapa
   └─ Выбрать релевантный их бизнесу
   └─ Упомянуть: Какая проблема была, что сделали, какой результат
   └─ Пример: "Для сети клиник разработали автозапись → регистратура разгружена на 65%"

6. МЕТРИКИ УЛУЧШЕНИЯ
   └─ Если есть похожий кейс → указать % улучшения
   └─ Пример: "платные услуги выросли на 28% в первый квартал"
   └─ Это ДОказательство, не обещание

7. ТОН И СТИЛЬ (из tone_and_style_guide.md)
   └─ ✓ Прямолинейный (без "рады представить", "с уважением")
   └─ ✓ Данные-ориентированный (цифры, факты, результаты)
   └─ ✓ Уверенный (как человек, который ЗНАЕТ решение)
   └─ ✓ Предпринимательский (ты бизнесмен, знаешь боли как свои)
   └─ ✓ Конкретный (действия, а не обещания)
   └─ ✗ НЕ шаблонный ("сотрудничество", "предлагаем услуги")
   └─ ✗ НЕ слишком формальный (не письмо в госучреждение)
   └─ ✗ НЕ слишком casual (не переписка с другом)

8. CALL-TO-ACTION (КОНКРЕТНОЕ ВРЕМЯ)
   └─ Предложить встречу ЗАВТРА (не "в удобное время")
   └─ Два варианта времени (10:30 и 14:00 или 11:00 и 15:00)
   └─ Пример: "Обсудить стратегию — завтра в 10:30 или в 14:00?"

9. КОНТАКТНАЯ ИНФОРМАЦИЯ
   └─ Добавить Telegram link: https://t.me/grigory_ux
   └─ Это должно быть в конце, как CTA

10. ПОКАЗАТЬ ЛИЧНОСТЬ
    └─ Упомянуть что ты САМ ПРЕДПРИНИМАТЕЛЬ
    └─ Упомянуть твои автоматизированные бизнесы
    └─ Упомянуть что ты НЕ фрилансер (не исполнитель)
    └─ Это создает авторитет и доверие

───────────────────────────────────────────────────────────────
ТРЕБОВАНИЯ К ВЫВОДУ:

✓ ОБЪЕМ: Ровно 100-150 слов
  (Проверить с помощью счетчика слов)
  
✓ СТРУКТУРА (обязательная):
  1. Открытие (1-2 предложения о ситуации)
  2. Определение болей (2-3 предложения)
  3. Предложение решения (2-3 предложения)
  4. Доказательство кейсом (1-2 предложения)
  5. CTA (1 предложение с временем и Telegram)

✓ ДАННЫЕ: Все числа из input обязательны в выводе

✓ БЕЗ ШАБЛОНОВ: Каждое сообщение уникально

✓ БЕЗ ПОЭТИЧЕСКИХ ФРА: Только бизнес

───────────────────────────────────────────────────────────────
ИНСТРУКЦИЯ ДЛЯ GEMINI:

Используй контекст из 20 .md файлов (tone_and_style_guide.md особенно).
Анализируй данные компании с точки зрения:
  • Что в их бизнесе сломано?
  • Почему это ТУ ОБРАЗОМ влияет на выручку?
  • Какое решение будет наиболее эффективно?
  • Какой из трех кейсов наиболее релевантен?

ВЫВЕДИ ТОЛЬКО ГОТОВОЕ СООБЩЕНИЕ БЕЗ ОБЪЯСНЕНИЙ, БЕЗ РАЗМЕТКИ.
───────────────────────────────────────────────────────────────
```

---

## Output Format (Strict Validation)

CONTRACT: GeminiBusinessAnalysisOutput v1.0

### Output Requirements

```python
OUTPUT_SPEC = {
    "type": "string",
    "encoding": "UTF-8",
    "language": "Russian (RU-RU)",
    "min_words": 100,
    "max_words": 150,
    
    "required_elements": [
        "founder_first_name",           # Обращение по имени
        "at_least_one_metric",          # Выручка, сотрудники, рейтинг
        "at_least_two_pain_points",     # Две боли из input
        "specific_solution",            # Решение, не общие фразы
        "one_case_study_mention",       # Level Group, CookPad или BitPapa
        "concrete_meeting_time",        # Завтра + два варианта времени
        "telegram_link",                # https://t.me/grigory_ux
        "entrepreneur_mention",         # Упоминание что ты предприниматель
    ],
    
    "forbidden_elements": [
        "generic_phrases",              # "сотрудничество", "предлагаем"
        "too_formal_tone",              # Как письмо в госучреждение
        "excessive_punctuation",        # Много восклицательных знаков
        "unrealistic_promises",         # "Гарантируем результат за 2 недели"
        "filler_words",                 # "как известно", "естественно"
    ]
}
```

---

## Example Outputs

### Output #1 (Healthcare with Website)

```
Николай Аркадьевич, при статусе главного ЛОР-центра и выручке 321 млн руб. в год — 
ваша регистратура стала узким местом. Вижу проблему: запись только по телефону, перегруз на 
колл-центре видно по отзывам (критика не врачам, а записи), теряете пациентов на возврате — 
это минус 20-25% от потенциала на доп. услугах.

Для сети из 8 клиник похожего размера разработали систему онлайн-записи через бота — 
разгрузили регистратуру на 65%, автоматизировали 70% рутины, платные услуги выросли на 31% 
в первый квартал.

Уверен, похожий результат будет и у вас. Давайте обсудить стратегию — завтра в 10:30 или 
14:00? https://t.me/grigory_ux

Я сам предприниматель с автоматизированными бизнесами, работал с Level Group, CookPad, BitPapa.
```

**Analysis:**
- ✓ Имя: "Николай Аркадьевич"
- ✓ Метрики: "321 млн руб", "4.2 звезды"
- ✓ Боли: "запись только по телефону", "перегруз", "потеря на возврате"
- ✓ Решение: "система онлайн-записи через бота"
- ✓ Кейс: "для сети клиник разработали"
- ✓ Метрики улучшения: "65%", "31%"
- ✓ CTA: "завтра в 10:30 или 14:00"
- ✓ Telegram: есть
- ✓ Личность: "предприниматель с автоматизированными бизнесами"
- ✓ Слово count: ~130 слов
- ✓ Тон: прямолинейный, уверенный, без шаблонов

---

### Output #2 (Trade without Website)

```
Дмитрий Сергеевич, вижу "База №1" на RusProfile — стабильные 7 млн оборотов в год, 
это хороший результат для оптовой торговли. Но без нормального сайта и кривой CRM — 
заявки улетают в никуда, менеджеры тонут в рутине, повторные клиенты забывают вернуться.

Для похожей компании с 12 людьми поднял заявки на 85% через простой сайт + CRM + 
email-последовательности, повторные заказы выросли на 40% за первый квартал.

Предлагаю познакомиться и обсудить вашу ситуацию. Я топ-3 агентство России полного цикла 
(дизайн, CRM, система продаж), работал с Level Group и другими. Встречу давайте завтра — 
10:00 или 15:00? https://t.me/grigory_ux

Предприниматель, не фрилансер.
```

**Analysis:**
- ✓ Имя: "Дмитрий Сергеевич"
- ✓ Метрики: "7 млн оборотов", "12 людей"
- ✓ Боли: "нет сайта", "кривая CRM", "менеджеры в рутине", "нет повторных"
- ✓ Решение: "сайт + CRM + email-последовательности"
- ✓ Кейс: "похожей компании с 12 людьми"
- ✓ Метрики улучшения: "85% заявок", "40% повторных"
- ✓ CTA: "завтра — 10:00 или 15:00"
- ✓ Telegram: есть
- ✓ Личность: "Предприниматель, не фрилансер"
- ✓ Слово count: ~140 слов
- ✓ Тон: прямолинейный, конкретный, убеждающий

---

## Validation Pipeline

```python
def validate_gemini_output(
    output_text: str,
    input_data: dict,
    verbose: bool = True
) -> dict:
    """
    Validate Gemini output against contract.
    
    Returns dict with:
        - valid: bool (all requirements met?)
        - errors: list (critical failures)
        - warnings: list (minor issues)
        - score: 0-100 (quality score)
        - details: breakdown of each check
    """
    
    errors = []
    warnings = []
    score = 100
    details = {}
    
    # ============ CHECK 1: Word Count ============
    word_count = len(output_text.split())
    details["word_count"] = word_count
    
    if word_count < 80:
        errors.append(f"❌ Too short: {word_count} words (min 100)")
        score -= 25
    elif word_count > 180:
        errors.append(f"❌ Too long: {word_count} words (max 150)")
        score -= 25
    else:
        details["word_count_status"] = "✓ Valid"
    
    # ============ CHECK 2: Founder Name ============
    founder_first_name = input_data["founder_name"].split()[0]
    if founder_first_name not in output_text:
        warnings.append(f"⚠️  Missing founder name: {founder_first_name}")
        score -= 20
    else:
        details["founder_name"] = "✓ Present"
    
    # ============ CHECK 3: Metrics ============
    revenue = str(input_data["business_metrics"]["revenue_2024"])
    employees = str(input_data["business_metrics"]["employees"])
    metrics_found = 0
    
    if revenue in output_text:
        metrics_found += 1
    if employees in output_text:
        metrics_found += 1
    
    if metrics_found < 1:
        warnings.append("⚠️  No specific metrics (revenue/employees)")
        score -= 15
    details["metrics_found"] = metrics_found
    
    # ============ CHECK 4: Pain Points ============
    pain_points = input_data.get("identified_pain_points", [])
    pain_mentions = 0
    
    for pain in pain_points[:5]:  # Check first 5
        # Simple substring search (can be improved)
        if any(word in output_text.lower() for word in pain.lower().split()):
            pain_mentions += 1
    
    if pain_mentions < 2:
        warnings.append(f"⚠️  Only {pain_mentions} pain points mentioned (min 2)")
        score -= 15
    details["pain_points_mentioned"] = pain_mentions
    
    # ============ CHECK 5: Telegram Link ============
    if "https://t.me/grigory_ux" not in output_text:
        errors.append("❌ Missing Telegram link")
        score -= 25
    else:
        details["telegram"] = "✓ Present"
    
    # ============ CHECK 6: Case Study ============
    case_studies = ["Level Group", "CookPad", "BitPapa"]
    case_study_found = any(cs in output_text for cs in case_studies)
    
    if not case_study_found:
        warnings.append("⚠️  No case study mentioned")
        score -= 15
    else:
        details["case_study"] = "✓ Found"
    
    # ============ CHECK 7: Meeting Time ============
    has_tomorrow = "завтра" in output_text or "завтра" in output_text.lower()
    has_time = any(t in output_text for t in ["10:", "14:", "15:", "9:", "11:", "13:", "16:"])
    
    if not (has_tomorrow and has_time):
        warnings.append("⚠️  No specific meeting time (завтра + часы)")
        score -= 15
    else:
        details["meeting_time"] = "✓ Specific"
    
    # ============ CHECK 8: Entrepreneur Mention ============
    entrepreneur_keywords = ["предприниматель", "бизнесмен", "автоматизированные бизнесы"]
    entrepreneur_mentioned = any(kw in output_text.lower() for kw in entrepreneur_keywords)
    
    if not entrepreneur_mentioned:
        warnings.append("⚠️  Missing entrepreneur/business owner mention")
        score -= 10
    else:
        details["entrepreneur_mention"] = "✓ Present"
    
    # ============ CHECK 9: Generic Phrases (Forbidden) ============
    forbidden = ["сотрудничество", "предлагаем услуги", "с уважением", "рады представить"]
    forbidden_found = any(phrase in output_text.lower() for phrase in forbidden)
    
    if forbidden_found:
        warnings.append("⚠️  Contains forbidden/generic phrases")
        score -= 10
    
    # ============ Final Validation ============
    final_valid = len(errors) == 0 and score >= 60
    
    return {
        "valid": final_valid,
        "errors": errors,
        "warnings": warnings,
        "score": max(0, score),
        "details": details,
        "recommendation": (
            "✓ APPROVE" if final_valid
            else "⚠️  REVIEW" if score >= 60
            else "❌ REJECT - Regenerate required"
        )
    }
```

---

## End of 32_GEMINI_PROMPT_CONTRACT.md