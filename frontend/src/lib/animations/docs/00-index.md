# Anime.js Design System — Полная документация анимационной библиотеки

**Версия:** anime.js 4.0+  
**Дата создания:** 2025-12-17  
**Уровень сложности:** От базового до продвинутого  
**Назначение:** Полное руководство для LLM при создании анимаций на anime.js

---

## Структура документации

Данная документация разделена на **10 основных модулей**:

1. **01-foundations.md** — Основы, установка, концепции
2. **02-animation-basics.md** — Базовые анимации, свойства, параметры
3. **03-css-transforms-properties.md** — CSS трансформации и свойства
4. **04-values-types.md** — Типы значений, цвета, относительные значения
5. **05-timing-easing.md** — Управление временем, ease функции, delay, duration
6. **06-keyframes-stagger.md** — Keyframes, stagger эффекты, последовательные анимации
7. **07-timeline.md** — Timeline для композиции анимаций
8. **08-advanced-features.md** — Draggable, Scope, обработка событий
9. **09-svg-text.md** — SVG анимации, text splitting, морфинг
10. **10-utilities-engine.md** — Утилиты, цвета, различные вспомогательные функции

---

## Как использовать эту документацию

### Для LLM / AI агентов:

```
Когда нужно создать анимацию:
1. Определи ТИП анимации (простая, временная последовательность, драг, скролл)
2. Найди соответствующий модуль (02-06)
3. Изучи примеры из соответствующей категории
4. Проверь параметры и особенности в соответствующем разделе
5. Использй правильный синтаксис и обработку ошибок
6. При необходимости комбинируй с Timeline для сложных последовательностей
```

### Для разработчиков:

Используй эту систему как:
- **Справочник** для быстрого поиска нужной функции
- **Паттерны** для типовых решений
- **Примеры** для адаптации под свои нужды
- **MCP команды** для автоматизации через browser-control и desktop-commander

---

## Ключевые принципы anime.js

### 1. Селекторы и Таргеты
```javascript
// CSS селекторы
animate('.element', { x: 100 });
animate('#button', { opacity: 0.5 });
animate('[data-animate]', { rotate: 360 });

// DOM элементы напрямую
const element = document.querySelector('.box');
animate(element, { x: 100 });

// Массивы элементов
animate([el1, el2, el3], { y: 50 });

// Объекты JavaScript
const obj = { value: 0 };
animate(obj, { value: 100 });
```

### 2. Анимируемые свойства
- **CSS свойства**: `opacity`, `backgroundColor`, `filter`, и т.д.
- **CSS трансформации**: `x`, `y`, `rotate`, `scale`, `skew` и т.д.
- **SVG атрибуты**: `cx`, `cy`, `r`, `d` (для path)
- **HTML атрибуты**: `width`, `height`, `viewBox`
- **Объекты JS**: любые численные свойства
- **CSS переменные**: `--custom-property`

### 3. Типы значений

| Тип | Пример | Использование |
|-----|--------|--------------|
| Численное | `x: 100` | Простое число, используется по умолчанию px |
| Строковое с единицей | `width: '50%'` | Для процентов, rem, em, и т.д. |
| Цвет | `backgroundColor: '#FF0000'` | Hex, rgb, rgba, hsl, hsla, именованные |
| Относительное | `x: '+=100'` | `+=` добавить, `-=` отнять, `*=` умножить, `/=` разделить |
| Функция | `x: (t, i) => Math.sin(t) * 100` | Динамическое вычисление значения |
| Массив (keyframes) | `x: [0, 100, 200]` | Последовательность значений |

### 4. Структура параметров

```javascript
animate(target, {
  // Анимируемые свойства
  property: toValue,
  
  // Опции анимации (применяются ко всем свойствам)
  duration: 1000,        // мс
  delay: 0,              // мс
  ease: 'easeOutQuad',   // функция ослабления
  loop: false,           // зацикливание
  autoplay: true,        // автозапуск
  
  // Callbacks
  onBegin: () => {},     // в начале
  onUpdate: () => {},    // при обновлении
  onComplete: () => {},  // в конце
});
```

---

## Основные API функции

### animate()
Основная функция для создания анимаций
```javascript
const animation = animate(target, params);
```

### timeline
Для управления композицией нескольких анимаций
```javascript
const tl = timeline();
tl.add({ targets: '.el', x: 100 });
tl.add({ targets: '.el', y: 100 }, 0);  // одновременно с предыдущей
```

### Методы управления

| Метод | Описание |
|-------|---------|
| `.play()` | Начать/продолжить воспроизведение |
| `.pause()` | Остановить |
| `.restart()` | Начать заново |
| `.reverse()` | Обратная направление |
| `.seek(time)` | Перейти к моменту времени |
| `.complete()` | Прыгнуть в конец |
| `.reset()` | Вернуть в начальное состояние |

---

## Поддерживаемые функции ослабления (Eases)

```
linear
in, out, inOut, outIn (с параметром power)
inQuad, outQuad, inOutQuad, outInQuad
inCubic, outCubic, inOutCubic, outInCubic
inQuart, outQuart, inOutQuart, outInQuart
inQuint, outQuint, inOutQuint, outInQuint
inSine, outSine, inOutSine, outInSine
inExpo, outExpo, inOutExpo, outInExpo
inCirc, outCirc, inOutCirc, outInCirc
inBounce, outBounce, inOutBounce, outInBounce
inBack, outBack, inOutBack, outInBack
inElastic, outElastic, inOutElastic, outInElastic
spring(damping, mass, stiffness)
```

---

## Быстрые ссылки на документацию

### Официальная документация anime.js
- [animejs.com/documentation](https://animejs.com/documentation)
- [Getting Started](https://animejs.com/documentation/getting-started)
- [Animation API](https://animejs.com/documentation/animation)
- [Timeline API](https://animejs.com/documentation/timeline)
- [Utilities](https://animejs.com/documentation/utilities)

### Категории документации (для углубленного изучения)
- **Getting Started**: https://animejs.com/documentation/getting-started
- **Timer**: https://animejs.com/documentation/timer
- **Animation**: https://animejs.com/documentation/animation
- **Timeline**: https://animejs.com/documentation/timeline
- **Animatable**: https://animejs.com/documentation/animatable
- **Draggable**: https://animejs.com/documentation/draggable
- **Scope**: https://animejs.com/documentation/scope
- **Events**: https://animejs.com/documentation/events
- **SVG**: https://animejs.com/documentation/svg
- **Text**: https://animejs.com/documentation/text
- **Utilities**: https://animejs.com/documentation/utilities
- **Easings**: https://animejs.com/documentation/easings
- **WAAPI**: https://animejs.com/documentation/web-animation-api
- **Engine**: https://animejs.com/documentation/engine

---

## MCP команды для исследования

Если нужна дополнительная информация во время разработки:

```bash
# Используя browser-control MCP
browser-control navigate https://animejs.com/documentation/animation

# Используя desktop-commander MCP
desktop-commander open-browser "https://animejs.com/documentation/easings"
```

---

## Типовые сценарии использования

### Сценарий 1: Простая анимация при наведении
```javascript
animate('.button:hover', {
  scale: 1.1,
  duration: 300,
  ease: 'easeOutQuad'
});
```

### Сценарий 2: Последовательная анимация элементов
```javascript
animate('.item', {
  opacity: 1,
  y: 0,
  delay: stagger(100),
  duration: 600,
  ease: 'easeOutCubic'
});
```

### Сценарий 3: Анимация при скролле
```javascript
onScroll({
  target: '.element',
  animation: {
    opacity: [0, 1],
    y: [100, 0]
  },
  threshold: 0.5
});
```

### Сценарий 4: Сложная временная последовательность
```javascript
const tl = timeline();
tl.add({ targets: '.step1', x: 100 });
tl.add({ targets: '.step2', x: 100 }, '-=200');  // с перекрытием
tl.add({ targets: '.step3', x: 100 });
```

---

## Содержание остальных модулей

### В следующих документах ты найдёшь:

1. **01-foundations.md** → Установка, импорт, базовые концепции
2. **02-animation-basics.md** → Все о базовой функции animate()
3. **03-css-transforms-properties.md** → CSS трансформации, свойства, оптимизация
4. **04-values-types.md** → Типы значений, цвета, относительные и функциональные
5. **05-timing-easing.md** → Duration, delay, loop, ease функции
6. **06-keyframes-stagger.md** → Keyframes, stagger, последовательности
7. **07-timeline.md** → Управление композицией анимаций
8. **08-advanced-features.md** → Draggable, Scope, события, callbacks
9. **09-svg-text.md** → SVG морфинг, путь движения, разделение текста
10. **10-utilities-engine.md** → Утилиты, цвета, рандомизация, движок

---

## Версия и обновления

- **Версия библиотеки**: 4.0+
- **Последний обновлены**: 2025-12-17
- **Совместимость**: All modern browsers (ES6+)

## Лицензия и ссылка на проект

- GitHub: [juliangarnier/anime](https://github.com/juliangarnier/anime)
- NPM: `npm install animejs`
- CDN: `https://cdn.jsdelivr.net/npm/animejs@3.2.1/lib/anime.min.js`

---

**Следующий файл:** `01-foundations.md` — Основы и установка
