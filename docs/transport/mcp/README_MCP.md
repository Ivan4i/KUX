# MCP Kit — Model Context Protocol Infrastructure

> Универсальная инфраструктура MCP для Claude Code for VS Code.
> Копируйте папку `mcp-kit/` в любой проект и получайте доступ ко всем интеграциям.

## 🚀 Быстрый старт

### 1. Установка

```bash
# Из корня проекта
bash mcp-kit/scripts/setup_mcp.sh
```

### 2. Настройка токенов

```bash
# Откройте файл с токенами
code mcp-kit/.env.local

# Заполните нужные токены (см. комментарии в файле)
```

### 3. Запуск VS Code с окружением

```bash
# Загрузите переменные окружения и откройте VS Code
source mcp-kit/.env.local && code .
```

### 4. Проверка конфигурации

```bash
bash mcp-kit/scripts/check_mcp.sh
```

---

## 📦 Структура

```
mcp-kit/
├── .mcp.json              # MCP конфигурация (копируется в корень проекта)
├── .env.example           # Шаблон переменных окружения
├── .env.local             # Ваши токены (НЕ коммитится!)
├── README_MCP.md          # Эта документация
├── mcp/
│   ├── saas-gateway/      # MCP-сервер для SaaS интеграций
│   │   ├── src/           # TypeScript исходники
│   │   ├── dist/          # Скомпилированный код
│   │   └── package.json
│   └── local/             # Локальные MCP утилиты (если нужны)
└── scripts/
    ├── setup_mcp.sh       # Установка зависимостей
    ├── check_mcp.sh       # Проверка конфигурации
    └── link_mcp_config.sh # Обновление корневого .mcp.json
```

---

## 🔧 Доступные MCP-серверы

### 1. SaaS Gateway (saas-gateway)

Единый MCP-сервер для всех SaaS-интеграций. Все операции **read-only**.

| Сервис | Tools | Статус |
|--------|-------|--------|
| GitHub | `github_list_repos`, `github_get_issue`, `github_search_issues` | ✅ Ready |
| Figma | `figma_get_file`, `figma_list_components` | ✅ Ready |
| Cloudflare | `cloudflare_list_zones`, `cloudflare_get_zone_details` | ✅ Ready |
| Vercel | `vercel_list_projects`, `vercel_get_project` | ✅ Ready |
| Notion | `notion_search_pages`, `notion_get_page` | ✅ Ready |
| Linear | `linear_list_issues`, `linear_get_issue` | ✅ Ready |
| Sentry | `sentry_list_projects`, `sentry_get_issue` | ✅ Ready |
| Cloudinary | `cloudinary_list_resources`, `cloudinary_get_resource` | ✅ Ready |
| Postman | `postman_list_collections`, `postman_get_collection` | ✅ Ready |
| Datadog | `datadog_list_dashboards`, `datadog_search_logs` | ✅ Ready |
| CloudWatch | `cloudwatch_describe_operations` | ⚠️ Describe only |
| ELK | `elk_list_indices`, `elk_search_logs` | ✅ Ready |
| Supabase | `supabase_list_projects`, `supabase_get_project`, `supabase_run_sql`, `supabase_get_api_keys` | ✅ Ready |
| MongoDB Atlas | `mongodb_list_organizations`, `mongodb_list_projects`, `mongodb_list_clusters`, `mongodb_get_cluster` | ✅ Ready |
| Box | `box_list_files` | 🔜 Stub |
| Canva | `canva_list_designs` | 🔜 Stub |
| Clarity | `clarity_get_dashboard` | 🔜 Stub |

### 2. Filesystem (filesystem)

Доступ к файловой системе проекта.

- **Команда**: `npx @modelcontextprotocol/server-filesystem`
- **Доступ**: только корень проекта и `.sandbox`
- **Безопасность**: нет доступа к `/` или `~`

### 3. Desktop Commander (desktop-commander)

Управление рабочим столом. **Отключен по умолчанию.**

```bash
# Включить:
ENABLEDESKTOPCOMMANDER=true
```

### 4. Browser Control (browser-control)

Управление браузером через Puppeteer. **Отключен по умолчанию.**

```bash
# Включить:
ENABLECHROMECONTROL=true
```

---

## 🔑 Настройка токенов

### Где получить токены

| Сервис | URL | Рекомендуемые права |
|--------|-----|---------------------|
| GitHub | [Settings → Tokens](https://github.com/settings/tokens) | `repo:read`, `read:org` |
| Figma | [Developer Settings](https://www.figma.com/developers/api#access-tokens) | Personal Access Token |
| Cloudflare | [API Tokens](https://dash.cloudflare.com/profile/api-tokens) | `Zone:Read` |
| Vercel | [Account Tokens](https://vercel.com/account/tokens) | Read-only |
| Notion | [My Integrations](https://www.notion.so/my-integrations) | Read content |
| Linear | [API Settings](https://linear.app/settings/api) | Personal API Key |
| Sentry | [Auth Tokens](https://sentry.io/settings/account/api/auth-tokens/) | `project:read`, `org:read` |
| Cloudinary | [Console](https://cloudinary.com/console) | API Key/Secret |
| Postman | [API Keys](https://web.postman.co/settings/me/api-keys) | Read-only |
| Datadog | [API Keys](https://app.datadoghq.com/organization-settings/api-keys) | API Key + App Key |
| Supabase | [Access Tokens](https://supabase.com/dashboard/account/tokens) | Personal Access Token |
| MongoDB Atlas | [API Keys](https://cloud.mongodb.com/v2#/org/.../access/apiKeys) | Organization Read Only + IP Access List |

### Формат .env.local

```bash
# Минимальный набор для начала работы
GITHUBTOKEN=ghp_xxxxxxxxxxxx
FIGMATOKEN=figd_xxxxxxxxxxxx
CLOUDFLAREAPITOKEN=xxxxxxxxxx
VERCELTOKEN=xxxxxxxxxx
NOTIONTOKEN=secret_xxxxxxxxxxxx
```

---

## 🔄 Паттерн копирования в новый проект

### Шаг 1: Копирование

```bash
# Из исходного проекта
cp -r mcp-kit/ /path/to/new-project/
```

### Шаг 2: Установка

```bash
cd /path/to/new-project
bash mcp-kit/scripts/setup_mcp.sh
```

### Шаг 3: Настройка токенов

```bash
# Отредактируйте токены
nano mcp-kit/.env.local
# или
code mcp-kit/.env.local
```

### Шаг 4: Использование

```bash
source mcp-kit/.env.local && code .
```

Все пути в `.mcp.json` относительные — после копирования ничего править не нужно!

---

## 🔒 Безопасность

### Что коммитится

- ✅ `.mcp.json` — конфигурация без секретов
- ✅ `.env.example` — шаблон переменных
- ✅ `mcp/saas-gateway/src/` — исходный код

### Что НЕ коммитится

- ❌ `.env.local` — ваши токены
- ❌ `.env.*local` — любые локальные env файлы
- ❌ `*.secrets` — файлы с секретами
- ❌ `mcp/saas-gateway/dist/` — скомпилированный код
- ❌ `node_modules/` — зависимости

### Добавьте в .gitignore

```gitignore
# MCP secrets
.env.local
.env.*.local
*.secrets
mcp-kit/.env.local
mcp-kit/mcp/*/dist/
mcp-kit/mcp/*/node_modules/
```

---

## 📡 Fallback: OAuth (Вариант B)

Некоторые сервисы могут требовать OAuth вместо service tokens. В этом случае:

### Когда нужен OAuth

1. **Сервис не поддерживает API tokens** (например, некоторые функции Google)
2. **Требуется доступ к данным пользователя** (не service account)
3. **Токен короткоживущий** и требует refresh

### Подход для OAuth

1. **Развернуть OAuth-proxy сервер** — отдельный HTTP-сервер, который:
   - Обрабатывает OAuth callback
   - Хранит refresh tokens
   - Выдаёт access tokens по запросу

2. **Добавить HTTP MCP-сервер** вместо stdio:
   ```json
   {
     "oauth-service": {
       "url": "http://localhost:3100/mcp",
       "transport": "http"
     }
   }
   ```

3. **Workflow**:
   - Запустить OAuth-proxy
   - Пройти OAuth flow в браузере
   - MCP-сервер получает токены от proxy

### Пример структуры OAuth-proxy

```
mcp-kit/
└── mcp/
    └── oauth-proxy/        # HTTP MCP сервер с OAuth
        ├── server.ts       # Express + OAuth handlers
        ├── tokens.ts       # Token storage (encrypted)
        └── .env.oauth      # OAuth client credentials
```

**Примечание**: Реализация OAuth-proxy выходит за рамки базовой настройки. Создайте отдельный модуль при необходимости.

---

## 🛠 Добавление нового сервиса

### 1. Создайте файл сервиса

```bash
# mcp-kit/mcp/saas-gateway/src/services/myservice.ts
```

```typescript
import { createServiceClient } from '../utils/http-client.js';
import { getEnv } from '../utils/env.js';
import { logger } from '../utils/logger.js';

const API_URL = 'https://api.myservice.com/v1';

function getClient() {
  const token = getEnv('MYSERVICE_TOKEN');
  return createServiceClient(API_URL, {
    'Authorization': `Bearer ${token}`,
  });
}

export async function listItems(): Promise<unknown[]> {
  const client = getClient();
  logger.info('Fetching items from MyService');
  return client.get<unknown[]>('/items');
}
```

### 2. Добавьте tools в index.ts

```typescript
// В массив tools:
{
  name: 'myservice_list_items',
  description: 'List items from MyService',
  inputSchema: {
    type: 'object',
    properties: {},
    required: [],
  },
}

// В handleToolCall:
case 'myservice_list_items':
  return myservice.listItems();
```

### 3. Добавьте env в .env.example

```bash
# MyService
MYSERVICE_TOKEN=
```

### 4. Обновите checkServiceConfig

```typescript
// В utils/env.ts:
checkServiceConfig('MyService', ['MYSERVICE_TOKEN']),
```

### 5. Пересоберите

```bash
cd mcp-kit/mcp/saas-gateway && npm run build
```

---

## ❓ Troubleshooting

### MCP-сервер не запускается

```bash
# Проверьте, что gateway собран:
ls mcp-kit/mcp/saas-gateway/dist/index.js

# Пересоберите:
cd mcp-kit/mcp/saas-gateway && npm run build
```

### Токены не подхватываются

```bash
# Убедитесь, что загрузили env:
source mcp-kit/.env.local
echo $GITHUBTOKEN  # Должен показать токен

# Или запустите VS Code правильно:
source mcp-kit/.env.local && code .
```

### "Service not configured"

```bash
# Проверьте конфигурацию:
bash mcp-kit/scripts/check_mcp.sh

# Проверьте конкретную переменную:
echo $GITHUBTOKEN
```

### Ошибки сети/API

Проверьте логи MCP-сервера:
```bash
MCPLOGLEVEL=debug source mcp-kit/.env.local && code .
```

---

## 📝 Лицензия

MIT — используйте свободно в своих проектах.
