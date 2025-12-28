# 31_GEMINI_CONTEXT_PACK.md

## Context Caching Structure

### The 20 .md Files (650K tokens)

Your existing 20 .md files are structured into 4 groups for optimal caching:

```
📁 CONTEXT_PACK (650K tokens total)
│
├─ 📂 business_analysis/ (250K tokens)
│  ├─ competitive_landscape.md
│  │  └─ Анализ конкурентов, рыночные ниши, конкурентные преимущества
│  ├─ market_trends_2025.md
│  │  └─ Актуальные тренды 2025, цифровизация, автоматизация, AI в бизнесе
│  ├─ revenue_analysis.md
│  │  └─ Как анализировать выручку, темпы роста, сезонность, маржинальность
│  ├─ growth_opportunities.md
│  │  └─ Где искать точки роста, новые каналы, масштабирование
│  ├─ risk_assessment.md
│  │  └─ Определение рисков, уязвимостей, угроз, contingency planning
│  └─ industry_benchmarks.md
│     └─ Стандарты по отраслям, метрики сравнения, KPIs
│
├─ 📂 sales_strategy/ (100K tokens)
│  ├─ value_proposition_framework.md
│  │  └─ Как строить ценностное предложение, benefits vs features
│  ├─ pain_point_mapping.md
│  │  └─ Техника определения болей компании, диагностика проблем
│  ├─ buyer_persona_analysis.md
│  │  └─ Профили ключевых лиц, принимающих решение, их интересы
│  ├─ objection_handling.md
│  │  └─ Ответы на стандартные возражения (цена, время, верификация)
│  └─ deal_closing_tactics.md
│     └─ Тактики закрытия сделок, скорость принятия, urgency, FOMO
│
├─ 📂 communication/ (150K tokens) ⭐ CRITICAL
│  ├─ tone_and_style_guide.md ⭐⭐ САМЫЙ ВАЖНЫЙ
│  │  └─ ТВОЙ СТИЛЬ:
│  │     - Прямолинейный (без лишних вежливостей)
│  │     - Данные-ориентированный (цифры, факты, результаты)
│  │     - Уверенный (как человек, который ЗНАЕТ решение)
│  │     - Предпринимательский (ты сам бизнесмен, не фрилансер)
│  │     - Конкретный (не общие фразы, только action items)
│  ├─ email_best_practices.md
│  │  └─ Структура email, length optimization, subject lines, CTAs
│  ├─ messaging_psychology.md
│  │  └─ Психология убеждения, мотивация, триггеры к действию
│  ├─ personalization_techniques.md
│  │  └─ Методы персонализации (без creepy feeling), как использовать данные
│  ├─ follow_up_sequences.md
│  │  └─ Последовательности писем, интервалы, escalation, когда отступать
│  └─ crisis_communication.md
│     └─ Как отвечать если ответ - отказ или игнор, de-escalation
│
└─ 📂 case_studies/ (100K tokens)
   ├─ case_study_level_group.md
   │  └─ Level Group: реальная проблема, какое решение внедрили, metrics
   ├─ case_study_cookpad.md
   │  └─ CookPad: как внедрили, что измеряли, конечные результаты
   └─ case_study_bitpapa.md
      └─ BitPapa: проблемы were, решение, рост выручки, расширение
```

### Why This Structure Works

| Параметр | Значение | Бенефит |
|----------|----------|----------|
| **Общий размер** | 650K токов | Вмещается в контекст Gemini 3 Pro (1M limit) |
| **Caching cost** | $0.20/M токов/ч | 75% экономия vs обычный input ($2/M) |
| **Cache TTL** | 24 часа | Актуальные данные, не устаревают в течение дня |
| **Refresh frequency** | 1 раз в 24 часа | Минимум перегруза, достаточно для обновления |
| **Cache hit rate** | ~95% (для batch) | Почти каждый запрос использует кэш из-за одинакового префикса |
| **Setup time** | 1 минута (один раз) | После создания кэша нужна только передача промпта |

---

## File Requirements & Format

### Storage Location

```
project_root/
└─ context_pack/
   ├─ business_analysis/
   │  ├─ competitive_landscape.md
   │  ├─ market_trends_2025.md
   │  ├─ revenue_analysis.md
   │  ├─ growth_opportunities.md
   │  ├─ risk_assessment.md
   │  └─ industry_benchmarks.md
   ├─ sales_strategy/
   │  ├─ value_proposition_framework.md
   │  ├─ pain_point_mapping.md
   │  ├─ buyer_persona_analysis.md
   │  ├─ objection_handling.md
   │  └─ deal_closing_tactics.md
   ├─ communication/
   │  ├─ tone_and_style_guide.md
   │  ├─ email_best_practices.md
   │  ├─ messaging_psychology.md
   │  ├─ personalization_techniques.md
   │  ├─ follow_up_sequences.md
   │  └─ crisis_communication.md
   └─ case_studies/
      ├─ case_study_level_group.md
      ├─ case_study_cookpad.md
      └─ case_study_bitpapa.md
```

### File Format Requirements

Each .md file must follow:

```markdown
# File Title
Краткое описание содержимого (1-2 строки)

## Section 1
Детальное описание...

## Section 2
...

## Key Takeaways (в конце каждого файла)
- Пункт 1
- Пункт 2
- Пункт 3
```

**Encoding:** UTF-8
**Line endings:** Unix (LF), not Windows (CRLF)
**File sizes:** 20-50KB per file (total ~650KB)

### Content Quality Standards

- **Authoritative**: Based on real business experience (Level Group, CookPad, BitPapa)
- **Actionable**: Every section should be applicable to companies in Russia
- **Data-driven**: Include metrics, benchmarks, real examples
- **Current**: Updated for 2025 business landscape (not 2024 practices)
- **Specific**: Avoid vague language ("improve", "better") — use concrete terms

---

## Cache Lifecycle Management

### Creation Phase (On Service Startup)

```python
def initialize_cache():
    """
    Called once on service startup (or daily).
    
    Steps:
    1. Load all 20 .md files from disk
    2. Validate file integrity (encoding, format, size)
    3. Combine into single context string
    4. Send to Gemini with explicit cache request
    5. Store cache name in memory
    6. Set expiry timer (24 hours)
    """
    
    print("📦 Initializing Gemini cache...")
    
    # Load files
    context_pack = load_all_context_files()
    
    # Validate
    if not validate_context_pack(context_pack):
        print("✗ Context pack validation failed")
        return False
    
    # Combine
    combined = combine_context_files(context_pack)
    
    # Create cache
    cache = gemini_client.create_cache(combined)
    
    # Store for reuse
    GLOBAL_CACHE = {
        "name": cache.name,
        "created_at": datetime.now(),
        "expires_at": datetime.now() + timedelta(hours=24),
        "size_tokens": 650000,
        "file_count": 20,
    }
    
    print(f"✓ Cache created: {cache.name}")
    return True
```

### Monitoring Phase (During Operation)

```python
def monitor_cache():
    """
    Check cache validity every 1 hour during operation.
    
    Checks:
    1. Is cache still valid (not expired)?
    2. Are any .md files modified?
    3. Is cache being used (cache hits > 0)?
    """
    
    # Check expiry
    time_left = (GLOBAL_CACHE["expires_at"] - datetime.now()).total_seconds() / 3600
    
    if time_left < 1:
        print(f"⚠️  Cache expires in {time_left:.2f} hours, will recreate")
        return
    
    print(f"✓ Cache valid for {time_left:.1f} more hours")
    
    # Check file modifications
    for filename in context_pack_filenames:
        file_mod_time = os.path.getmtime(f"context_pack/{filename}")
        if datetime.fromtimestamp(file_mod_time) > GLOBAL_CACHE["created_at"]:
            print(f"⚠️  File modified: {filename}")
            print("   Will recreate cache on next startup")
            return
    
    # Check cache hit rate
    if METRICS["cache_hits"] == 0:
        print("⚠️  Cache created but no hits yet (normal for first batch)")
    else:
        hit_rate = METRICS["cache_hits"] / METRICS["total_requests"] * 100
        print(f"✓ Cache hit rate: {hit_rate:.1f}%")
```

### Refresh Phase (Every 24 Hours or on File Change)

```python
def refresh_cache_if_needed():
    """
    Auto-refresh cache if:
    1. TTL expired (24 hours passed), or
    2. Any .md file was modified
    """
    
    # Check expiry
    if datetime.now() > GLOBAL_CACHE["expires_at"]:
        print("🔄 Cache TTL expired, recreating...")
        initialize_cache()
        return
    
    # Check file modifications
    for filename in context_pack_filenames:
        file_mod_time = os.path.getmtime(f"context_pack/{filename}")
        if datetime.fromtimestamp(file_mod_time) > GLOBAL_CACHE["created_at"]:
            print(f"🔄 File {filename} modified, recreating cache...")
            initialize_cache()
            return
    
    print("✓ Cache valid, no refresh needed")
```

### Shutdown Phase

```python
def cleanup_on_shutdown():
    """
    Called when service shuts down.
    
    Actions:
    1. Log final cache metrics
    2. Mark cache for cleanup (optional)
    3. Close connections
    """
    
    final_metrics = {
        "total_requests": METRICS["total_requests"],
        "cache_hits": METRICS["cache_hits"],
        "cache_hit_rate": METRICS["cache_hits"] / METRICS["total_requests"] * 100,
        "total_cost": METRICS["total_cost"],
        "uptime_hours": (datetime.now() - SERVICE_START_TIME).total_seconds() / 3600,
    }
    
    print("📊 Final cache metrics:")
    for key, value in final_metrics.items():
        print(f"  {key}: {value}")
```

---

## Storage & Cost Optimization

### Storage Calculation

```
Files loaded: 20 .md files
Average file size: ~32.5 KB
Total text size: ~650 KB

Token conversion: 1 KB of text ≈ 1 token (rough estimate)
Total tokens: ~650K tokens

Gemini cache storage pricing:
- $0.20 per 1M tokens per hour

Cost if cache stored 24 hours:
= 650K tokens × $0.20/M tokens × 24 hours / 1M
= 650 × 0.20 × 24 / 1000
= $3.12 per day

BUT: Cost amortized across all requests!

If 100 companies processed in 24 hours:
= $3.12 / 100 = $0.031 per company ✓

If 1000 companies processed:
= $3.12 / 1000 = $0.0031 per company ✓✓
```

### Comparison: With vs Without Caching

**Scenario: Processing 1000 companies in one day**

**WITHOUT CACHING:**
```
Each request:
- Input: 650K tokens (context) + 150 tokens (prompt) = 650.15K
- Output: ~100 tokens (avg message)
- Cost per request: (650.15K × $2 + 100 × $12) / 1M = $1.30

Total for 1000: 1000 × $1.30 = $1,300
```

**WITH EXPLICIT CACHING:**
```
Cache creation (one-time):
- 650K input tokens × $0.20/M = $0.13

Each request (reuse cache):
- Cached: 650K × $0.20/M = $0.13
- Fresh input: 150 tokens × $2/M = $0.0003
- Output: 100 tokens × $12/M = $0.0012
- Cost per request: $0.1303

Total for 1000: (0.13 + 1000 × 0.1303) = $130.43 (90% savings!)
```

---

## Integration with Gemini API

### How Cached Context Gets Sent

```python
# Step 1: Create cache (one-time, happens in __init__)
cache = client.caches.create(
    model="gemini-3-pro",
    config={
        "display_name": "business-analysis-context-pack",
        "contents": [
            {
                "parts": [{"text": combined_20_files}]  # 650K tokens
            }
        ]
    }
)
# cache.name = "projects/ABC/caches/XYZ123"


# Step 2: Use cache for each company analysis
response = client.models.generate_content(
    model="gemini-3-pro",
    contents="Analyze Company XYZ...",  # Fresh prompt only
    config={
        "cached_content": cache.name,  # Reference cache (not re-upload)
    }
)
# Result: 650K from cache (cheap) + prompt tokens (cheap) = total ~$0.13
```

**Key insight:** The 650K tokens are sent to Gemini ONCE. Every subsequent request just references the cache name, not the content itself.

---

## Performance Metrics

### What Gets Cached

```
FROM GEMINI USAGE METADATA:

prompt_token_count = 150 (just the prompt for new company)
cache_read_input_token_count = 650,000 (from cache)
cache_creation_input_token_count = 0 (already created)
candidates_token_count = 100 (output message)

Cost calculation:
- Cached input: 650,000 × $0.20 = $0.13
- Fresh input: 150 × $2 = $0.0003
- Output: 100 × $12 = $0.0012
- TOTAL: $0.1303 per request
```

### Monitoring Dashboard Metrics

```python
METRICS = {
    "cache_hit_rate": {
        "description": "% of requests using cached content",
        "target": ">90%",
        "formula": "cache_hits / total_requests * 100",
    },
    "cache_efficiency": {
        "description": "% of input tokens from cache vs fresh",
        "target": ">85%",
        "formula": "cache_tokens / (cache_tokens + fresh_tokens) * 100",
    },
    "avg_cost_per_message": {
        "description": "Average cost per generated message",
        "target": "<$0.15",
        "formula": "total_cost / message_count",
    },
    "cache_reuse_count": {
        "description": "How many times cache used before refresh",
        "target": ">100 requests",
        "formula": "requests_with_cache_hit",
    },
    "ttft_latency": {
        "description": "Time to first token (milliseconds)",
        "target": "<500ms",
        "formula": "measured in response metadata",
    },
}
```

---

## End of 31_GEMINI_CONTEXT_PACK.md