import { useState, useEffect } from 'react'
import toast from 'react-hot-toast'
import { Button } from '@/components/common/Button'
import {
  RiSaveLine,
  RiRefreshLine,
  RiCheckboxCircleFill,
  RiCloseCircleFill,
  RiEyeLine,
  RiEyeOffLine,
  RiSettingsLine,
  RiRobot2Line,
  RiKeyLine,
  RiTelegramLine,
  RiDatabase2Line,
  RiNotionLine,
} from '@remixicon/react'
import {
  getSettings,
  getConfigStatus,
  updateIntegrationSettings,
  updateBehaviorSettings,
  testNotionConnection,
  testTelegramConnection,
} from '@/services/api'

interface ConfigStatus {
  integrations: {
    notion: { configured: boolean; api_key: boolean; database_id: boolean }
    telegram: { configured: boolean; bot_token: boolean; chat_id: boolean }
    puter: { configured: boolean; api_key: boolean }
  }
  env_file_exists: boolean
}

export function SettingsPage() {
  const [isLoading, setIsLoading] = useState(true)
  const [isSaving, setIsSaving] = useState(false)
  const [configStatus, setConfigStatus] = useState<ConfigStatus | null>(null)

  // Integration settings
  const [notionApiKey, setNotionApiKey] = useState('')
  const [notionDatabaseId, setNotionDatabaseId] = useState('')
  const [telegramBotToken, setTelegramBotToken] = useState('')
  const [telegramChatId, setTelegramChatId] = useState('')
  const [puterApiKey, setPuterApiKey] = useState('')
  const [puterApiUrl, setPuterApiUrl] = useState('https://api.puter.ai/v1')
  const [puterModel, setPuterModel] = useState('claude-sonnet-4.5')

  // Behavior settings
  const [minTypingDelay, setMinTypingDelay] = useState(50)
  const [maxTypingDelay, setMaxTypingDelay] = useState(150)
  const [minActionDelay, setMinActionDelay] = useState(500)
  const [maxActionDelay, setMaxActionDelay] = useState(2000)
  const [typoProbability, setTypoProbability] = useState(0.03)
  const [typoFixProbability, setTypoFixProbability] = useState(0.8)
  const [maxMessagesPerHour, setMaxMessagesPerHour] = useState(20)
  const [maxMessagesPerDay, setMaxMessagesPerDay] = useState(100)
  const [cooldownAfterBatch, setCooldownAfterBatch] = useState(30)

  // UI state
  const [showNotionKey, setShowNotionKey] = useState(false)
  const [showTelegramToken, setShowTelegramToken] = useState(false)
  const [showPuterKey, setShowPuterKey] = useState(false)
  const [testingNotion, setTestingNotion] = useState(false)
  const [testingTelegram, setTestingTelegram] = useState(false)

  // Load settings
  useEffect(() => {
    loadSettings()
  }, [])

  const loadSettings = async () => {
    try {
      setIsLoading(true)
      const [settings, status] = await Promise.all([
        getSettings(),
        getConfigStatus(),
      ])

      // Integration settings
      if (settings.integrations.notion_api_key) {
        setNotionApiKey(settings.integrations.notion_api_key)
      }
      if (settings.integrations.notion_database_id) {
        setNotionDatabaseId(settings.integrations.notion_database_id)
      }
      if (settings.integrations.telegram_bot_token) {
        setTelegramBotToken(settings.integrations.telegram_bot_token)
      }
      if (settings.integrations.telegram_chat_id) {
        setTelegramChatId(settings.integrations.telegram_chat_id)
      }
      if (settings.integrations.puter_api_key) {
        setPuterApiKey(settings.integrations.puter_api_key)
      }
      if (settings.integrations.puter_api_url) {
        setPuterApiUrl(settings.integrations.puter_api_url)
      }
      if (settings.integrations.puter_default_model) {
        setPuterModel(settings.integrations.puter_default_model)
      }

      // Behavior settings
      setMinTypingDelay(settings.behavior.min_typing_delay_ms)
      setMaxTypingDelay(settings.behavior.max_typing_delay_ms)
      setMinActionDelay(settings.behavior.min_action_delay_ms)
      setMaxActionDelay(settings.behavior.max_action_delay_ms)
      setTypoProbability(settings.behavior.typo_probability)
      setTypoFixProbability(settings.behavior.typo_fix_probability)
      setMaxMessagesPerHour(settings.behavior.max_messages_per_hour)
      setMaxMessagesPerDay(settings.behavior.max_messages_per_day)
      setCooldownAfterBatch(settings.behavior.cooldown_after_batch_min)

      setConfigStatus(status)
    } catch (error) {
      console.error('Error loading settings:', error)
      toast.error('Не удалось загрузить настройки')
    } finally {
      setIsLoading(false)
    }
  }

  const handleSaveIntegrations = async () => {
    try {
      setIsSaving(true)
      await updateIntegrationSettings({
        notion_api_key: notionApiKey,
        notion_database_id: notionDatabaseId,
        telegram_bot_token: telegramBotToken,
        telegram_chat_id: telegramChatId,
        puter_api_key: puterApiKey,
        puter_api_url: puterApiUrl,
        puter_default_model: puterModel,
      })
      toast.success('Настройки интеграций сохранены')
      // Reload config status
      const status = await getConfigStatus()
      setConfigStatus(status)
    } catch (error) {
      console.error('Error saving integrations:', error)
      toast.error('Не удалось сохранить настройки интеграций')
    } finally {
      setIsSaving(false)
    }
  }

  const handleSaveBehavior = async () => {
    try {
      setIsSaving(true)
      await updateBehaviorSettings({
        min_typing_delay_ms: minTypingDelay,
        max_typing_delay_ms: maxTypingDelay,
        min_action_delay_ms: minActionDelay,
        max_action_delay_ms: maxActionDelay,
        typo_probability: typoProbability,
        typo_fix_probability: typoFixProbability,
        max_messages_per_hour: maxMessagesPerHour,
        max_messages_per_day: maxMessagesPerDay,
        cooldown_after_batch_min: cooldownAfterBatch,
      })
      toast.success('Настройки поведения сохранены')
    } catch (error) {
      console.error('Error saving behavior:', error)
      toast.error('Не удалось сохранить настройки поведения')
    } finally {
      setIsSaving(false)
    }
  }

  const handleTestNotion = async () => {
    try {
      setTestingNotion(true)
      const result = await testNotionConnection()
      if (result.success) {
        toast.success(result.message)
      } else {
        toast.error(result.message)
      }
    } catch (error) {
      console.error('Notion test error:', error)
      toast.error('Не удалось проверить подключение к Notion')
    } finally {
      setTestingNotion(false)
    }
  }

  const handleTestTelegram = async () => {
    try {
      setTestingTelegram(true)
      const result = await testTelegramConnection()
      if (result.success) {
        toast.success(result.message)
      } else {
        toast.error(result.message)
      }
    } catch (error) {
      console.error('Telegram test error:', error)
      toast.error('Не удалось проверить подключение к Telegram')
    } finally {
      setTestingTelegram(false)
    }
  }

  const StatusBadge = ({ configured }: { configured: boolean }) => (
    <span
      className={`inline-flex items-center gap-1 px-2 py-0.5 text-xs font-medium rounded-full ${
        configured
          ? 'bg-success-100 text-success-700'
          : 'bg-warning-100 text-warning-700'
      }`}
    >
      {configured ? (
        <>
          <RiCheckboxCircleFill className="w-3 h-3" />
          Настроено
        </>
      ) : (
        <>
          <RiCloseCircleFill className="w-3 h-3" />
          Не настроено
        </>
      )}
    </span>
  )

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
          <p className="mt-4 text-sm text-gray-600">Загрузка настроек...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Настройки</h1>
              <p className="mt-1 text-sm text-gray-500">
                Настройка API-ключей, поведения и интеграций
              </p>
            </div>
            <Button
              variant="ghost"
              size="md"
              leftIcon={<RiRefreshLine />}
              onClick={loadSettings}
            >
              Обновить
            </Button>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        {/* Integration Settings */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200">
          <div className="px-6 py-4 border-b border-gray-200">
            <div className="flex items-center gap-2">
              <RiKeyLine className="w-5 h-5 text-primary-600" />
              <h2 className="text-lg font-semibold text-gray-900">
                API интеграции
              </h2>
            </div>
            <p className="mt-1 text-sm text-gray-500">
              Настройка API-ключей внешних сервисов
            </p>
          </div>

          <div className="p-6 space-y-6">
            {/* Notion */}
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <RiNotionLine className="w-5 h-5 text-gray-800" />
                  <h3 className="font-medium text-gray-900">Notion</h3>
                </div>
                {configStatus && (
                  <StatusBadge configured={configStatus.integrations.notion.configured} />
                )}
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    API-ключ
                  </label>
                  <div className="relative">
                    <input
                      type={showNotionKey ? 'text' : 'password'}
                      value={notionApiKey}
                      onChange={(e) => setNotionApiKey(e.target.value)}
                      placeholder="secret_..."
                      className="w-full px-3 py-2 pr-10 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                    />
                    <button
                      type="button"
                      onClick={() => setShowNotionKey(!showNotionKey)}
                      className="absolute right-2 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                    >
                      {showNotionKey ? <RiEyeOffLine /> : <RiEyeLine />}
                    </button>
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Database ID
                  </label>
                  <input
                    type="text"
                    value={notionDatabaseId}
                    onChange={(e) => setNotionDatabaseId(e.target.value)}
                    placeholder="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  />
                </div>
              </div>

              <Button
                variant="secondary"
                size="sm"
                onClick={handleTestNotion}
                isLoading={testingNotion}
              >
                Проверить подключение
              </Button>
            </div>

            <hr className="border-gray-200" />

            {/* Telegram */}
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <RiTelegramLine className="w-5 h-5 text-blue-400" />
                  <h3 className="font-medium text-gray-900">Telegram Bot</h3>
                </div>
                {configStatus && (
                  <StatusBadge configured={configStatus.integrations.telegram.configured} />
                )}
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Bot Token
                  </label>
                  <div className="relative">
                    <input
                      type={showTelegramToken ? 'text' : 'password'}
                      value={telegramBotToken}
                      onChange={(e) => setTelegramBotToken(e.target.value)}
                      placeholder="123456789:ABC..."
                      className="w-full px-3 py-2 pr-10 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                    />
                    <button
                      type="button"
                      onClick={() => setShowTelegramToken(!showTelegramToken)}
                      className="absolute right-2 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                    >
                      {showTelegramToken ? <RiEyeOffLine /> : <RiEyeLine />}
                    </button>
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Chat ID
                  </label>
                  <input
                    type="text"
                    value={telegramChatId}
                    onChange={(e) => setTelegramChatId(e.target.value)}
                    placeholder="-1001234567890"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  />
                </div>
              </div>

              <Button
                variant="secondary"
                size="sm"
                onClick={handleTestTelegram}
                isLoading={testingTelegram}
              >
                Проверить подключение
              </Button>
            </div>

            <hr className="border-gray-200" />

            {/* Puter.js LLM */}
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <RiRobot2Line className="w-5 h-5 text-purple-500" />
                  <h3 className="font-medium text-gray-900">Puter.js LLM</h3>
                </div>
                {configStatus && (
                  <StatusBadge configured={configStatus.integrations.puter.configured} />
                )}
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    API-ключ
                  </label>
                  <div className="relative">
                    <input
                      type={showPuterKey ? 'text' : 'password'}
                      value={puterApiKey}
                      onChange={(e) => setPuterApiKey(e.target.value)}
                      placeholder="pk_..."
                      className="w-full px-3 py-2 pr-10 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                    />
                    <button
                      type="button"
                      onClick={() => setShowPuterKey(!showPuterKey)}
                      className="absolute right-2 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                    >
                      {showPuterKey ? <RiEyeOffLine /> : <RiEyeLine />}
                    </button>
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    API URL
                  </label>
                  <input
                    type="text"
                    value={puterApiUrl}
                    onChange={(e) => setPuterApiUrl(e.target.value)}
                    placeholder="https://api.puter.ai/v1"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Модель по умолчанию
                  </label>
                  <select
                    value={puterModel}
                    onChange={(e) => setPuterModel(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  >
                    <option value="claude-sonnet-4.5">Claude Sonnet 4.5</option>
                    <option value="claude-opus-4.5">Claude Opus 4.5</option>
                    <option value="gpt-4o">GPT-4o</option>
                    <option value="gpt-4o-mini">GPT-4o Mini</option>
                  </select>
                </div>
              </div>
            </div>
          </div>

          <div className="px-6 py-4 bg-gray-50 border-t border-gray-200 rounded-b-xl">
            <Button
              variant="primary"
              leftIcon={<RiSaveLine />}
              onClick={handleSaveIntegrations}
              isLoading={isSaving}
            >
              Сохранить настройки интеграций
            </Button>
          </div>
        </div>

        {/* Behavior Settings */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200">
          <div className="px-6 py-4 border-b border-gray-200">
            <div className="flex items-center gap-2">
              <RiSettingsLine className="w-5 h-5 text-primary-600" />
              <h2 className="text-lg font-semibold text-gray-900">
                Настройки поведения
              </h2>
            </div>
            <p className="mt-1 text-sm text-gray-500">
              Настройка человекоподобного поведения для автоматизации
            </p>
          </div>

          <div className="p-6 space-y-6">
            {/* Typing Delays */}
            <div>
              <h3 className="font-medium text-gray-900 mb-3">Задержки набора</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Мин. задержка (мс)
                  </label>
                  <input
                    type="number"
                    value={minTypingDelay}
                    onChange={(e) => setMinTypingDelay(Number(e.target.value))}
                    min={10}
                    max={500}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Макс. задержка (мс)
                  </label>
                  <input
                    type="number"
                    value={maxTypingDelay}
                    onChange={(e) => setMaxTypingDelay(Number(e.target.value))}
                    min={50}
                    max={1000}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  />
                </div>
              </div>
              <p className="mt-2 text-xs text-gray-500">
                Случайная задержка между нажатиями клавиш для имитации человека
              </p>
            </div>

            <hr className="border-gray-200" />

            {/* Action Delays */}
            <div>
              <h3 className="font-medium text-gray-900 mb-3">Задержки действий</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Мин. задержка (мс)
                  </label>
                  <input
                    type="number"
                    value={minActionDelay}
                    onChange={(e) => setMinActionDelay(Number(e.target.value))}
                    min={100}
                    max={5000}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Макс. задержка (мс)
                  </label>
                  <input
                    type="number"
                    value={maxActionDelay}
                    onChange={(e) => setMaxActionDelay(Number(e.target.value))}
                    min={500}
                    max={10000}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  />
                </div>
              </div>
              <p className="mt-2 text-xs text-gray-500">
                Случайная задержка между действиями (клики, прокрутка и т.д.)
              </p>
            </div>

            <hr className="border-gray-200" />

            {/* Typo Simulation */}
            <div>
              <h3 className="font-medium text-gray-900 mb-3">Симуляция опечаток</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Вероятность опечатки (0-1)
                  </label>
                  <input
                    type="number"
                    value={typoProbability}
                    onChange={(e) => setTypoProbability(Number(e.target.value))}
                    min={0}
                    max={0.2}
                    step={0.01}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Вероятность исправления (0-1)
                  </label>
                  <input
                    type="number"
                    value={typoFixProbability}
                    onChange={(e) => setTypoFixProbability(Number(e.target.value))}
                    min={0}
                    max={1}
                    step={0.1}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  />
                </div>
              </div>
              <p className="mt-2 text-xs text-gray-500">
                Имитация опечаток и их исправления для большей реалистичности
              </p>
            </div>

            <hr className="border-gray-200" />

            {/* Rate Limits */}
            <div>
              <h3 className="font-medium text-gray-900 mb-3">Лимиты</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Макс. сообщений/час
                  </label>
                  <input
                    type="number"
                    value={maxMessagesPerHour}
                    onChange={(e) => setMaxMessagesPerHour(Number(e.target.value))}
                    min={1}
                    max={100}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Макс. сообщений/день
                  </label>
                  <input
                    type="number"
                    value={maxMessagesPerDay}
                    onChange={(e) => setMaxMessagesPerDay(Number(e.target.value))}
                    min={1}
                    max={500}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Пауза после пакета (мин)
                  </label>
                  <input
                    type="number"
                    value={cooldownAfterBatch}
                    onChange={(e) => setCooldownAfterBatch(Number(e.target.value))}
                    min={5}
                    max={120}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  />
                </div>
              </div>
              <p className="mt-2 text-xs text-gray-500">
                Ограничение частоты сообщений для избежания блокировки аккаунта
              </p>
            </div>
          </div>

          <div className="px-6 py-4 bg-gray-50 border-t border-gray-200 rounded-b-xl">
            <Button
              variant="primary"
              leftIcon={<RiSaveLine />}
              onClick={handleSaveBehavior}
              isLoading={isSaving}
            >
              Сохранить настройки поведения
            </Button>
          </div>
        </div>

        {/* Status Summary */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200">
          <div className="px-6 py-4 border-b border-gray-200">
            <div className="flex items-center gap-2">
              <RiDatabase2Line className="w-5 h-5 text-primary-600" />
              <h2 className="text-lg font-semibold text-gray-900">
                Статус конфигурации
              </h2>
            </div>
          </div>

          <div className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {/* Notion Status */}
              <div
                className={`p-4 rounded-lg border ${
                  configStatus?.integrations.notion.configured
                    ? 'border-success-200 bg-success-50'
                    : 'border-warning-200 bg-warning-50'
                }`}
              >
                <div className="flex items-center gap-2">
                  <RiNotionLine className="w-5 h-5 text-gray-800" />
                  <span className="font-medium">Notion</span>
                </div>
                <div className="mt-2 space-y-1 text-sm">
                  <div className="flex items-center gap-2">
                    {configStatus?.integrations.notion.api_key ? (
                      <RiCheckboxCircleFill className="w-3 h-3 text-success-600" />
                    ) : (
                      <RiCloseCircleFill className="w-3 h-3 text-warning-600" />
                    )}
                    <span>API Key</span>
                  </div>
                  <div className="flex items-center gap-2">
                    {configStatus?.integrations.notion.database_id ? (
                      <RiCheckboxCircleFill className="w-3 h-3 text-success-600" />
                    ) : (
                      <RiCloseCircleFill className="w-3 h-3 text-warning-600" />
                    )}
                    <span>Database ID</span>
                  </div>
                </div>
              </div>

              {/* Telegram Status */}
              <div
                className={`p-4 rounded-lg border ${
                  configStatus?.integrations.telegram.configured
                    ? 'border-success-200 bg-success-50'
                    : 'border-warning-200 bg-warning-50'
                }`}
              >
                <div className="flex items-center gap-2">
                  <RiTelegramLine className="w-5 h-5 text-blue-400" />
                  <span className="font-medium">Telegram</span>
                </div>
                <div className="mt-2 space-y-1 text-sm">
                  <div className="flex items-center gap-2">
                    {configStatus?.integrations.telegram.bot_token ? (
                      <RiCheckboxCircleFill className="w-3 h-3 text-success-600" />
                    ) : (
                      <RiCloseCircleFill className="w-3 h-3 text-warning-600" />
                    )}
                    <span>Bot Token</span>
                  </div>
                  <div className="flex items-center gap-2">
                    {configStatus?.integrations.telegram.chat_id ? (
                      <RiCheckboxCircleFill className="w-3 h-3 text-success-600" />
                    ) : (
                      <RiCloseCircleFill className="w-3 h-3 text-warning-600" />
                    )}
                    <span>Chat ID</span>
                  </div>
                </div>
              </div>

              {/* Puter Status */}
              <div
                className={`p-4 rounded-lg border ${
                  configStatus?.integrations.puter.configured
                    ? 'border-success-200 bg-success-50'
                    : 'border-warning-200 bg-warning-50'
                }`}
              >
                <div className="flex items-center gap-2">
                  <RiRobot2Line className="w-5 h-5 text-purple-500" />
                  <span className="font-medium">Puter.js LLM</span>
                </div>
                <div className="mt-2 space-y-1 text-sm">
                  <div className="flex items-center gap-2">
                    {configStatus?.integrations.puter.api_key ? (
                      <RiCheckboxCircleFill className="w-3 h-3 text-success-600" />
                    ) : (
                      <RiCloseCircleFill className="w-3 h-3 text-warning-600" />
                    )}
                    <span>API Key</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
