 # ANIMATION_PLAYBOOK_ANIMEJS.md

**Version:** 1.0  
**Last Updated:** 2024-12-12  
**Status:** Production-Ready  
**Framework:** Anime.js V4  

---

## 📌 Обзор

Этот документ описывает, как использовать **Anime.js V4** в UXCode Meet так, чтобы все анимации:

✅ Были мощными и гладкими (30-60fps)  
✅ Подчинялись дизайн-системе (токены времени, цветов, эйзингов)  
✅ Работали на мобильных устройствах (mobile-first)  
✅ Соответствовали WCAG требованиям (reduced-motion режим)  
✅ Не убивали производительность (GPU-дружественные свойства)  
✅ Были легко тестируемы и переиспользуемы  

---

## 🏗️ Архитектура анимационного слоя

### Структура проекта

```
src/
├── animation/                          # Новый слой для всех анимаций
│   ├── index.ts                        # Экспорты API
│   ├── engine.ts                       # Инициализация и управление Engine
│   ├── hooks/
│   │   ├── useAnimeScope.ts            # Hook для регистрации анимаций
│   │   ├── useTimelineAnimation.ts     # Hook для таймлайнов
│   │   └── useDraggable.ts             # Hook для drag-drop
│   ├── presets/
│   │   ├── pageTransitions.ts          # Вход/выход страниц
│   │   ├── roomScenes.ts               # Сценарии комнаты
│   │   ├── participantEffects.ts       # Эффекты плиток участников
│   │   ├── boardAnimations.ts          # Анимации доски (tldraw)
│   │   ├── panelAnimations.ts          # Чат/файлы/панели
│   │   └── notifications.ts            # Тосты и badge'и
│   ├── helpers/
│   │   ├── resolveTokens.ts            # Резолв токенов из theme
│   │   ├── createAnimation.ts          # Helper для простых анимаций
│   │   └── validateMotion.ts           # Проверка reduced-motion
│   └── types.ts                        # TypeScript интерфейсы
├── hooks/
│   └── useTheme.ts                     # (существующий хук)
└── theme/
    └── theme.ts                        # (существующий, V3_DESIGN_SYSTEM.md)
```

### Принцип единого Engine

```typescript
// engine.ts
import anime from 'animejs';

// Глобальный engine инициализируется один раз при загрузке приложения
const engine = anime.engine();

// Управление:
// - engine.state.running — статус
// - engine.subscribe() — подписка на тики
// - engine.pause() / engine.play() — контроль

export const animationEngine = {
  get running() { return engine.state.running; },
  pause: () => engine.pause(),
  play: () => engine.play(),
  subscribe: (callback: () => void) => engine.subscribe(callback),
};
```

**Назначение Engine:**
- ✅ Синхронизирует все независимые анимации
- ✅ Позволяет паузировать/возобновлять приложение (при reconnect, blur/focus)
- ✅ Отвечает за тики (60fps)
- ✅ Интегрируется с React через useEffect

---

## 🎬 Основные API Anime.js (V4)

### 1. Getting Started — Простые анимации

**Документация:** https://animejs.com/documentation/getting-started

**Использование в UXCode Meet:**

```typescript
// ❌ ЗАПРЕЩЕНО — прямые вызовы
anime({
  targets: '.button',
  opacity: 1,
  duration: 300,
});

// ✅ ПРАВИЛЬНО — через helper
import { createAnimation } from '@/animation/helpers/createAnimation';

createAnimation({
  targets: '.button',
  preset: 'fade-in',  // Семантическое имя из theme
  duration: 'fast',   // Из theme.duration.fast
});
```

**Helper функция:**

```typescript
// src/animation/helpers/createAnimation.ts
import anime from 'animejs';
import { resolveTokens } from './resolveTokens';

interface AnimationParams {
  targets: string | HTMLElement | HTMLElement[];
  preset: string;  // 'fade-in', 'slide-up', 'scale-pop', etc.
  duration?: keyof typeof theme.duration;  // 'fast', 'normal', 'slow'
  easing?: keyof typeof theme.easing;      // 'standard', 'entrance', 'exit'
  delay?: number;
  opacity?: number | number[];
  transform?: string;
  [key: string]: any;
}

export const createAnimation = (params: AnimationParams) => {
  const { preset, duration = 'normal', easing = 'standard', ...rest } = params;
  
  const tokens = resolveTokens({
    duration,
    easing,
    preset,
  });

  return anime({
    ...rest,
    duration: tokens.duration,
    easing: tokens.easing,
  });
};
```

---

### 2. Timer — Периодические эффекты

**Документация:** https://animejs.com/documentation/timer

**Использование в UXCode Meet:**

```typescript
// Скелетон-лоадер (пульсация)
const skeletonPulse = anime.timeline({
  autoplay: false,
  loop: true,
});

skeletonPulse
  .add({
    targets: '.skeleton-loader',
    opacity: [0.5, 1, 0.5],
    duration: 1000,
    easing: 'easeInOutQuad',
  });

// Индикатор ожидания (спиннер)
const spinnerAnimation = anime({
  targets: '.spinner',
  rotate: 360,
  duration: 1200,
  loop: true,
  easing: 'linear',
});

// Timer для отсчёта удаления данных (30 дней)
const retentionBadgeTimer = setInterval(() => {
  const daysRemaining = calculateDaysRemaining();
  if (daysRemaining < 3) {
    // Подсветить красным
    anime({
      targets: '.retention-badge',
      backgroundColor: theme.colors.error,
      duration: 500,
    });
  }
}, 1000);
```

---

### 3. Animation — Стандартный API

**Документация:** https://animejs.com/documentation/animation

**Использование в UXCode Meet:**

```typescript
// Событие "кто-то говорит" — мягкое свечение микрофона
const speakingIndicator = anime({
  targets: '.participant-mic-icon',
  boxShadow: `0 0 ${theme.shadow.lg} ${theme.colors.primary}`,
  scale: 1.1,
  duration: 300,
  easing: theme.easing.entrance,
});

// Когда закончил говорить — затухание
speakingIndicator.reverse();

// События Animation
speakingIndicator.play();
speakingIndicator.pause();
speakingIndicator.seek(50);  // Seek на 50% от длительности
speakingIndicator.reverse(); // Назад

// Callback на события
speakingIndicator.complete = () => {
  console.log('Animation completed');
};
```

---

### 4. Timeline — Сложные сцены

**Документация:** https://animejs.com/documentation/timeline

**Использование в UXCode Meet:**

#### Сценарий: Вход в комнату

```typescript
// src/animation/presets/roomScenes.ts
import anime from 'animejs';
import { theme } from '@/theme';

export const createRoomEntryTimeline = (scopeId: string) => {
  const timeline = anime.timeline({
    autoplay: false,
  });

  // Фаза 1: Появление фона доски (200ms)
  timeline.add({
    targets: `[data-scope="${scopeId}"] .board-container`,
    opacity: [0, 1],
    duration: theme.duration.normal,
    easing: theme.easing.entrance,
  }, 0);  // Начало = 0

  // Фаза 2: Появление дока участников (150ms, стартует при -100ms от конца фазы 1)
  timeline.add({
    targets: `[data-scope="${scopeId}"] .participants-dock`,
    translateY: [40, 0],
    opacity: [0, 1],
    duration: theme.duration.fast,
    easing: theme.easing.entrance,
  }, '-=100');  // Начинается раньше на 100ms

  // Фаза 3: Слайд чата справа (100ms, параллельно с доком)
  timeline.add({
    targets: `[data-scope="${scopeId}"] .chat-panel`,
    translateX: [200, 0],
    opacity: [0, 1],
    duration: theme.duration.fast,
    easing: theme.easing.entrance,
  }, '-=150');  // Одновременно с доком

  // Фаза 4: Стикеры на доске появляются последовательно
  const stickers = document.querySelectorAll(
    `[data-scope="${scopeId}"] .board-sticker`
  );
  stickers.forEach((sticker, index) => {
    timeline.add({
      targets: sticker,
      scale: [0.8, 1],
      opacity: [0, 1],
      duration: theme.duration.fast,
      easing: theme.easing.entrance,
    }, `${index * 50}`);  // Каждый стикер на 50ms позже
  });

  return timeline;
};

// Использование в компоненте
const useRoomEntry = (roomId: string) => {
  useEffect(() => {
    const timeline = createRoomEntryTimeline(roomId);
    timeline.play();

    return () => timeline.pause();
  }, [roomId]);
};
```

#### Сценарий: Переход в режим презентации

```typescript
export const createPresentationModeTimeline = (scopeId: string) => {
  const timeline = anime.timeline({
    autoplay: false,
  });

  // Доска сворачивается в угол (мини-превью)
  timeline.add({
    targets: `[data-scope="${scopeId}"] .board-container`,
    width: ['100%', '25%'],
    height: ['100%', '25%'],
    right: 0,
    bottom: 0,
    duration: theme.duration.normal,
    easing: theme.easing.standard,
  }, 0);

  // Основной контент (презентация/экран) масштабируется и центрируется
  timeline.add({
    targets: `[data-scope="${scopeId}"] .presentation-content`,
    scale: [0.9, 1],
    opacity: [0.7, 1],
    duration: theme.duration.normal,
    easing: theme.easing.entrance,
  }, 0);  // Параллельно с сворачиванием доски

  // Чат панель уходит на фон (z-index + прозрачность)
  timeline.add({
    targets: `[data-scope="${scopeId}"] .chat-panel`,
    opacity: 0.3,
    duration: theme.duration.fast,
    easing: theme.easing.standard,
  }, 0);

  return timeline;
};
```

---

### 5. Animatable — Что можно анимировать

**Документация:** https://animejs.com/documentation/animatable

**Доступные свойства в UXCode Meet:**

```typescript
// CSS свойства (GPU-friendly)
{
  opacity: [0, 1],                    // Видимость
  transform: 'translateX(100px)',     // Движение
  scale: [0.8, 1],                   // Масштаб
  rotate: [0, 45],                   // Поворот
}

// Цвета (из theme)
{
  backgroundColor: [theme.colors.bg, theme.colors.primary],
  borderColor: [theme.colors.border, theme.colors.primary],
  color: [theme.colors.text, theme.colors.primary],
}

// Тень (из theme)
{
  boxShadow: [theme.shadows.sm, theme.shadows.lg],
}

// SVG атрибуты
{
  r: [5, 15],                        // Радиус круга
  'stroke-width': [1, 3],
  d: 'path(M10,10 L100,100)',
}

// Числовые значения JS-объектов
{
  value: [0, 100],  // Числовая анимация (например, для счётчика)
}

// ❌ НЕ GPU-friendly (избегать)
{
  width: [100, 200],                 // Используй transform: scaleX
  height: [100, 200],                // Используй transform: scaleY
  left: [0, 100],                    // Используй transform: translate
  top: [0, 100],                     // Используй transform: translate
}
```

**Принцип:** GPU-friendly свойства (transform, opacity) обязательны для smooth анимаций на мобильных.

---

### 6. Draggable — Перетаскивание

**Документация:** https://animejs.com/documentation/draggable

**Использование в UXCode Meet:**

#### Стикеры на доске

```typescript
// src/animation/presets/boardAnimations.ts
import anime from 'animejs';

export const enableBoardStickerDragging = (sticker: HTMLElement) => {
  // Draggable V4
  const draggable = anime.draggable({
    target: sticker,
    onDragStart() {
      // При начале перетаскивания — подсветить
      anime({
        targets: sticker,
        boxShadow: theme.shadows.lg,
        duration: 150,
      });
    },
    onDrag(instance: any) {
      // Во время перетаскивания — opacity немного ниже
      sticker.style.opacity = '0.9';
    },
    onDragEnd(instance: any) {
      // При отпускании — эффект пружины к позиции снапа
      const snappedX = Math.round(instance.x / GRID_SIZE) * GRID_SIZE;
      const snappedY = Math.round(instance.y / GRID_SIZE) * GRID_SIZE;

      anime({
        targets: sticker,
        translateX: snappedX,
        translateY: snappedY,
        opacity: 1,
        duration: theme.duration.fast,
        easing: 'easeOutElastic(1, 0.5)',
      });

      // Сохранить позицию на сервер
      saveStickerPosition(sticker.id, snappedX, snappedY);
    },
    // Ограничения по осям (если нужны)
    constrainAxis: true,
  });

  return draggable;
};
```

#### Карточки в интерфейсе (лёгкое перемещение)

```typescript
export const enableCardSlideAnimation = (card: HTMLElement) => {
  const draggable = anime.draggable({
    target: card,
    translateX: {
      min: -100,  // Макс смещение влево
      max: 100,   // Макс смещение вправо
    },
    modifiers: {
      // Кривая сопротивления
      x(x: number) {
        return Math.cos(x * 0.01) * x * 0.5;
      },
    },
    onDragEnd(instance: any) {
      // Отпустить — вернуть на место
      anime({
        targets: card,
        translateX: 0,
        duration: theme.duration.normal,
        easing: 'easeOutBack',
      });
    },
  });
};
```

---

### 7. Scope — Изоляция анимаций

**Документация:** https://animejs.com/documentation/scope

**Использование в UXCode Meet:**

```typescript
// Каждая комната имеет свой scope ID
const roomScopeId = `room-${roomId}`;

// Все анимации в этой комнате помечаются data-scope
return (
  <div data-scope={roomScopeId} className="room-container">
    <div className="board-container">...</div>
    <div className="participants-dock">...</div>
    <div className="chat-panel">...</div>
  </div>
);

// При переходе или закрытии комнаты — очистить все анимации этого scope
export const cleanupRoomAnimations = (scopeId: string) => {
  // Остановить все анимации с этим data-scope
  const targets = document.querySelectorAll(`[data-scope="${scopeId}"]`);
  targets.forEach((target) => {
    anime.set(target, {
      // Сбросить все анимированные свойства
      opacity: '',
      transform: '',
    });
  });
};
```

**Преимущества:**
- ✅ Нет утечек памяти при смене комнат
- ✅ Изолированные таймлайны
- ✅ Легко отладить (можно паузировать/перемотавать по scope)

---

### 8. Events — События анимации

**Документация:** https://animejs.com/documentation/events

**Использование в UXCode Meet:**

```typescript
// Синхронизация UI-состояний React
const animation = anime({
  targets: '.overlay',
  opacity: [1, 0],
  duration: theme.duration.normal,
  easing: theme.easing.exit,
});

// Callback на start
animation.begin = () => {
  console.log('Animation started');
  setAnimationState('running');
};

// Callback на update (на каждый frame)
animation.update = (instance) => {
  console.log(`Progress: ${instance.progress}%`);
};

// Callback на complete
animation.complete = () => {
  console.log('Animation finished');
  setAnimationState('idle');
  // Например, скрыть overlay после завершения
  setOverlayVisible(false);
};

// Callback на loop (если loop: true)
animation.loopComplete = () => {
  console.log('Loop completed');
};
```

---

### 9. SVG — Векторные анимации

**Документация:** https://animejs.com/documentation/svg

**Использование в UXCode Meet:**

```typescript
// Логотип — появление штрихов
export const animateLogo = () => {
  const logo = document.querySelector('.logo-svg');
  
  anime({
    targets: '.logo-svg path',
    strokeDashoffset: [anime.setDashoffset, 0],
    fill: 'rgba(255, 255, 255, 0)',
    easing: 'easeInOutQuad',
    duration: 1400,
    delay: (el, i) => i * 50,
    loop: false,
  });
};

// Пульсирующий значок (например, микрофон)
export const animatePulsingIcon = () => {
  anime({
    targets: '.mic-icon circle',
    r: [5, 8],
    opacity: [1, 0],
    duration: 800,
    easing: 'linear',
    loop: true,
  });
};
```

---

### 10. Text — Текстовые эффекты

**Документация:** https://animejs.com/documentation/text

**Использование в UXCode Meet:**

```typescript
// ⚠️ Используется ОСТОРОЖНО (может быть медленным)

// Появление текста буква за буквой (только для заголовков)
export const animateHeadlineText = (headlineElement: HTMLElement) => {
  anime({
    targets: `${headlineElement.id} .character`,
    opacity: [0, 1],
    translateY: [-10, 0],
    easing: 'easeOutExpo',
    duration: 400,
    delay: (el, i) => i * 30,
  });
};

// Счётчик текста (количество дней до удаления)
export const animateRetentionCounter = (from: number, to: number) => {
  anime({
    targets: { value: from },
    value: to,
    easing: 'easeOutQuad',
    duration: 500,
    round: 1,  // Округлять целые числа
    update(instance) {
      document.querySelector('.retention-days')!.textContent = 
        Math.round(instance.progress * (to - from) + from).toString();
    },
  });
};
```

---

### 11. Utilities — Вспомогательные функции

**Документация:** https://animejs.com/documentation/utilities

```typescript
// Случайное число (для множественных элементов)
anime({
  targets: '.particle',
  x: () => anime.random(-100, 100),
  y: () => anime.random(-100, 100),
  delay: anime.stagger(50),  // Задержка между элементами
  duration: 1000,
});

// Stagger — последовательное появление
anime({
  targets: '.list-item',
  opacity: [0, 1],
  translateX: [-20, 0],
  delay: anime.stagger(100),  // 100ms между каждым
  duration: 500,
});

// Кастомный stagger
anime({
  targets: '.tile',
  scale: [0.8, 1],
  delay: anime.stagger(50, { start: 100 }),  // Начинает с задержкой 100ms
  duration: 400,
});
```

---

### 12. Easings — Кривые анимации

**Документация:** https://animejs.com/documentation/easings

**Использование в UXCode Meet (только из theme.easing):**

```typescript
// ✅ ПРАВИЛЬНО — из theme
easing: theme.easing.standard,      // cubic-bezier(0.16, 1, 0.3, 1)
easing: theme.easing.entrance,      // cubic-bezier(0.34, 1.56, 0.64, 1)
easing: theme.easing.exit,          // cubic-bezier(0.25, 0.46, 0.45, 0.94)

// Preset-кривые Anime.js (используются редко, всегда согласовывать с дизайнером)
easing: 'easeInOutQuad',
easing: 'easeOutExpo',
easing: 'easeOutElastic(1, 0.5)',
easing: 'linear',
```

**Правило:** Все ease-функции должны быть определены в theme или согласованы с дизайнером.

---

### 13. WAAPI — Web Animation API интеграция

**Документация:** https://animejs.com/documentation/waapi

```typescript
// Конвертировать Anime.js анимацию в WAAPI (для совместимости)
const nativeAnimation = anime.convertToWAAPI({
  targets: '.element',
  opacity: [0, 1],
  duration: 1000,
});

// Использование WAAPI напрямую (очень редко, только если нужна специфика)
const waapi = document.querySelector('.element')!.animate(
  [
    { opacity: 0, transform: 'translateY(10px)' },
    { opacity: 1, transform: 'translateY(0)' },
  ],
  {
    duration: 1000,
    easing: theme.easing.standard,
    fill: 'forwards',
  }
);
```

---

### 14. Engine — Управление движком

**Документация:** https://animejs.com/documentation/engine

```typescript
// src/animation/engine.ts
import anime from 'animejs';

export const initializeAnimationEngine = () => {
  // Получить engine (создаётся автоматически)
  const engine = anime.engine;

  // Подписка на тики (для отладки или синхронизации)
  engine.subscribe((time: number) => {
    // time в миллисекундах
    console.log(`Engine tick: ${time}ms`);
  });

  // Пауза всех анимаций (например, при blur окна)
  window.addEventListener('blur', () => {
    engine.pause();
  });

  // Возобновление (focus)
  window.addEventListener('focus', () => {
    engine.play();
  });

  // Пауза на reconnect (Socket.IO disconnect)
  socket.on('disconnect', () => {
    engine.pause();
  });

  // Возобновление на reconnect
  socket.on('connect', () => {
    engine.play();
  });

  return engine;
};

// Использование
export const animationEngine = {
  get isRunning() {
    return anime.engine.state.running;
  },
  pause: () => anime.engine.pause(),
  play: () => anime.engine.play(),
};
```

---

## 🎯 Плейбук сцен UXCode Meet

### Сценарий 1: Вход в приложение (Auth → Rooms)

**Когда:** Пользователь авторизуется через Telegram  
**Длительность:** 600ms  
**Тип:** Timeline с последовательностью  

```typescript
// src/animation/presets/pageTransitions.ts
import anime from 'animejs';
import { theme } from '@/theme';

export const createAuthToRoomsTimeline = () => {
  const timeline = anime.timeline({
    autoplay: false,
  });

  // Фаза 1 (0ms): Фон затемняется и исчезает
  timeline.add({
    targets: '.auth-background',
    opacity: [1, 0],
    duration: theme.duration.normal,
    easing: theme.easing.exit,
  }, 0);

  // Фаза 2 (300ms): Список комнат появляется с fade + slide-up
  timeline.add({
    targets: '.rooms-list',
    opacity: [0, 1],
    translateY: [40, 0],
    duration: theme.duration.normal,
    easing: theme.easing.entrance,
  }, 300);

  // Фаза 3 (350ms): Каждая карточка комнаты появляется со смещением
  timeline.add({
    targets: '.room-card',
    opacity: [0, 1],
    translateY: [20, 0],
    duration: theme.duration.fast,
    easing: theme.easing.entrance,
    delay: anime.stagger(50),
  }, 350);

  // Фаза 4 (400ms): Кнопка "Create Room" появляется
  timeline.add({
    targets: '.create-room-btn',
    opacity: [0, 1],
    scale: [0.9, 1],
    duration: theme.duration.fast,
    easing: theme.easing.entrance,
  }, 400);

  return timeline;
};
```

**Использование в компоненте:**

```typescript
// src/pages/Rooms.tsx
import { useEffect } from 'react';
import { useTimelineAnimation } from '@/animation/hooks/useTimelineAnimation';

export const RoomsPage = () => {
  const { timeline } = useTimelineAnimation('rooms-page', () =>
    createAuthToRoomsTimeline()
  );

  useEffect(() => {
    timeline?.play();
  }, [timeline]);

  return (
    <div data-scope="rooms-page">
      {/* Content */}
    </div>
  );
};
```

---

### Сценарий 2: Вход в комнату (загрузка доски + участников + чат)

**Когда:** Пользователь нажал на комнату  
**Длительность:** 800ms  
**Тип:** Timeline с параллельностью  

```typescript
export const createRoomEntranceTimeline = (scopeId: string) => {
  const timeline = anime.timeline({
    autoplay: false,
  });

  // Фаза 1 (0ms): Доска появляется с fade
  timeline.add({
    targets: `[data-scope="${scopeId}"] .board-container`,
    opacity: [0, 1],
    duration: theme.duration.normal,
    easing: theme.easing.entrance,
  }, 0);

  // Фаза 2 (-150ms относительно конца фазы 1): Док с участниками slide-up
  timeline.add({
    targets: `[data-scope="${scopeId}"] .participants-dock`,
    translateY: [60, 0],
    opacity: [0, 1],
    duration: theme.duration.normal,
    easing: theme.easing.entrance,
  }, '-=150');

  // Фаза 3 (0ms): Чат справа slide-in
  timeline.add({
    targets: `[data-scope="${scopeId}"] .chat-panel`,
    translateX: [300, 0],
    opacity: [0, 1],
    duration: theme.duration.normal,
    easing: theme.easing.entrance,
  }, 0);

  // Фаза 4: Плитки участников появляются со stagger
  timeline.add({
    targets: `[data-scope="${scopeId}"] .participant-tile`,
    scale: [0.8, 1],
    opacity: [0, 1],
    duration: theme.duration.fast,
    easing: theme.easing.entrance,
    delay: anime.stagger(50),
  }, 200);

  return timeline;
};
```

---

### Сценарий 3: Переход в режим презентации

**Когда:** Пользователь начинает screen share или выбирает участника для focus  
**Длительность:** 400ms  
**Тип:** Timeline с трансформациями  

```typescript
export const createPresentationModeTimeline = (
  scopeId: string,
  presentationElementSelector: string
) => {
  const timeline = anime.timeline({
    autoplay: false,
  });

  // Доска уходит в corner (мини-превью)
  timeline.add(
    {
      targets: `[data-scope="${scopeId}"] .board-container`,
      width: ['100%', '20vw'],
      height: ['100%', '20vh'],
      position: 'fixed',
      right: 0,
      bottom: 0,
      duration: theme.duration.normal,
      easing: theme.easing.standard,
    },
    0
  );

  // Презентация масштабируется и центрируется (параллельно)
  timeline.add(
    {
      targets: presentationElementSelector,
      scale: [0.95, 1],
      opacity: [0.8, 1],
      duration: theme.duration.normal,
      easing: theme.easing.entrance,
    },
    0
  );

  // Чат становится полупрозрачным (фон)
  timeline.add(
    {
      targets: `[data-scope="${scopeId}"] .chat-panel`,
      opacity: 0.2,
      pointerEvents: 'none',
      duration: theme.duration.fast,
      easing: theme.easing.exit,
    },
    0
  );

  return timeline;
};

// Выход из режима презентации
export const createExitPresentationModeTimeline = (scopeId: string) => {
  const timeline = anime.timeline({
    autoplay: false,
  });

  // Доска возвращается на полный экран
  timeline.add({
    targets: `[data-scope="${scopeId}"] .board-container`,
    width: '100%',
    height: '100%',
    right: 'auto',
    bottom: 'auto',
    duration: theme.duration.normal,
    easing: theme.easing.entrance,
  }, 0);

  // Чат возвращается
  timeline.add({
    targets: `[data-scope="${scopeId}"] .chat-panel`,
    opacity: 1,
    pointerEvents: 'auto',
    duration: theme.duration.normal,
    easing: theme.easing.entrance,
  }, 0);

  return timeline;
};
```

---

### Сценарий 4: Участник присоединился (появление плитки)

**Когда:** Новый участник подключился к WebRTC  
**Длительность:** 300ms  
**Тип:** Простая анимация  

```typescript
export const animateNewParticipant = (
  participantElement: HTMLElement,
  index: number
) => {
  anime({
    targets: participantElement,
    scale: [0.7, 1],
    opacity: [0, 1],
    translateY: [30, 0],
    duration: theme.duration.normal,
    easing: theme.easing.entrance,
    delay: index * 50,  // Если несколько одновременно
  });
};
```

---

### Сценарий 5: Индикатор "говорит" (мигание микрофона)

**Когда:** Участник говорит (по VAD или Server Signal)  
**Длительность:** 200ms (loop)  
**Тип:** Looping animation  

```typescript
export const animateSpeakingIndicator = (
  participantTile: HTMLElement
) => {
  const indicator = participantTile.querySelector('.mic-indicator');

  const animation = anime({
    targets: indicator,
    boxShadow: [
      `0 0 0 0 ${theme.colors.primary}`,
      `0 0 12px 6px ${theme.colors.primary}`,
    ],
    scale: [1, 1.1],
    duration: 200,
    easing: theme.easing.standard,
    loop: true,
  });

  return {
    stop: () => {
      animation.pause();
      // Вернуть в нормальное состояние
      anime({
        targets: indicator,
        boxShadow: 'none',
        scale: 1,
        duration: 100,
        easing: theme.easing.exit,
      });
    },
  };
};
```

---

### Сценарий 6: Перетаскивание стикера на доске

**Когда:** Пользователь перетаскивает стикер (Miro/FigJam style)  
**Тип:** Draggable + пружинящий возврат  

```typescript
export const setupBoardStickerDragging = (
  sticker: HTMLElement,
  gridSize: number = 10
) => {
  const draggable = anime.draggable({
    target: sticker,
    onDragStart() {
      // При старте — приподнять с тенью
      anime({
        targets: sticker,
        boxShadow: theme.shadows.lg,
        zIndex: 1000,
        duration: 150,
      });
    },
    onDrag(instance: any) {
      // Во время перетаскивания — лёгкая полупрозрачность
      sticker.style.opacity = '0.95';
    },
    onDragEnd(instance: any) {
      // При отпускании — snap к сетке с bounce эффектом
      const snappedX = Math.round((instance.x || 0) / gridSize) * gridSize;
      const snappedY = Math.round((instance.y || 0) / gridSize) * gridSize;

      anime({
        targets: sticker,
        translateX: snappedX,
        translateY: snappedY,
        opacity: 1,
        boxShadow: theme.shadows.sm,
        zIndex: 'auto',
        duration: theme.duration.normal,
        easing: 'easeOutElastic(1, 0.6)',
      });

      // Сохранить позицию
      socket.emit('updateStickerPosition', {
        stickerId: sticker.dataset.id,
        x: snappedX,
        y: snappedY,
      });
    },
  });

  return draggable;
};
```

---

### Сценарий 7: Открытие/закрытие чат-панели

**Когда:** Пользователь кликает на вкладку "Чат" или "Файлы"  
**Длительность:** 250ms  
**Тип:** Slide + fade  

```typescript
export const createChatPanelToggleTimeline = (
  scopeId: string,
  isOpening: boolean
) => {
  return anime({
    targets: `[data-scope="${scopeId}"] .chat-panel`,
    translateX: isOpening ? [300, 0] : [0, 300],
    opacity: isOpening ? [0, 1] : [1, 0],
    duration: theme.duration.normal,
    easing: isOpening ? theme.easing.entrance : theme.easing.exit,
    pointerEvents: isOpening ? 'auto' : 'none',
  });
};
```

---

### Сценарий 8: Тост-уведомление (сообщение)

**Когда:** Система отправляет уведомление (сообщение в чате, файл загруженный, и т.д.)  
**Длительность:** 300ms (in) + 200ms (stay) + 300ms (out)  
**Тип:** Timeline  

```typescript
export const createToastNotificationTimeline = (
  toastElement: HTMLElement
) => {
  const timeline = anime.timeline({
    autoplay: true,
  });

  // In: Slide up + fade
  timeline.add({
    targets: toastElement,
    translateY: [40, 0],
    opacity: [0, 1],
    duration: theme.duration.normal,
    easing: theme.easing.entrance,
  }, 0);

  // Stay: Pause (200ms встроен в то, что тост висит)

  // Out: Через 3 секунды slide down + fade
  timeline.add(
    {
      targets: toastElement,
      translateY: [-40, 0],
      opacity: [1, 0],
      duration: theme.duration.normal,
      easing: theme.easing.exit,
    },
    3000  // После 3 секунд
  );

  return timeline;
};
```

---

### Сценарий 9: Badge "осталось 12 дней до удаления"

**Когда:** Пользователь видит комнату, которая будет удалена  
**Длительность:** Пульсирует каждые 2 секунды  
**Тип:** Looping  

```typescript
export const animateRetentionBadge = (badgeElement: HTMLElement) => {
  const animation = anime({
    targets: badgeElement,
    opacity: [1, 0.6],
    scale: [1, 1.05],
    duration: 2000,
    easing: theme.easing.standard,
    loop: true,
  });

  // Если < 3 дней до удаления — красная подсветка
  const daysRemaining = parseInt(
    badgeElement.dataset.daysRemaining || '30'
  );
  if (daysRemaining < 3) {
    anime({
      targets: badgeElement,
      backgroundColor: theme.colors.error,
      color: theme.colors.bg,
      boxShadow: `0 0 12px ${theme.colors.error}`,
    });
  }

  return animation;
};
```

---

### Сценарий 10: Загрузка файла (progress bar)

**Когда:** Пользователь загружает файл  
**Длительность:** Варьируется (0-100%)  
**Тип:** Число анимация  

```typescript
export const animateFileUploadProgress = (
  progressBar: HTMLElement,
  finalProgress: number = 100
) => {
  return anime({
    targets: { value: 0 },
    value: finalProgress,
    easing: 'linear',
    duration: finalProgress * 20,  // ~2ms per 1%
    update(instance) {
      const progress = Math.round(instance.progress * 100);
      progressBar.style.width = `${progress}%`;
      progressBar.textContent = `${progress}%`;
    },
  });
};
```

---

## 🛠️ React интеграция

### Custom Hook: useAnimeScope

```typescript
// src/animation/hooks/useAnimeScope.ts
import { useEffect, useRef } from 'react';
import anime from 'animejs';

interface UseAnimeScopeOptions {
  id: string;
  autoplay?: boolean;
}

export const useAnimeScope = (options: UseAnimeScopeOptions) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const animationsRef = useRef<anime.AnimeInstance[]>([]);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    // Добавить data-scope для изоляции
    container.dataset.scope = options.id;

    return () => {
      // Cleanup: остановить все анимации этого scope
      animationsRef.current.forEach((anim) => {
        anim.pause();
      });
      animationsRef.current = [];
    };
  }, [options.id]);

  // Helper функция для регистрации анимации
  const registerAnimation = (animation: anime.AnimeInstance) => {
    animationsRef.current.push(animation);
    return animation;
  };

  return {
    containerRef,
    scopeId: options.id,
    registerAnimation,
  };
};

// Использование
const MyComponent = () => {
  const { containerRef, scopeId, registerAnimation } = useAnimeScope({
    id: 'my-component-' + Math.random(),
  });

  useEffect(() => {
    const animation = anime({
      targets: `[data-scope="${scopeId}"] .element`,
      opacity: 1,
    });
    registerAnimation(animation);
  }, [scopeId, registerAnimation]);

  return <div ref={containerRef} />;
};
```

### Custom Hook: useTimelineAnimation

```typescript
// src/animation/hooks/useTimelineAnimation.ts
import { useEffect, useRef } from 'react';
import anime from 'animejs';

export const useTimelineAnimation = (
  id: string,
  createTimeline: () => anime.AnimeTimelineInstance
) => {
  const timelineRef = useRef<anime.AnimeTimelineInstance | null>(null);

  useEffect(() => {
    timelineRef.current = createTimeline();

    return () => {
      timelineRef.current?.pause();
      timelineRef.current = null;
    };
  }, [createTimeline]);

  return {
    timeline: timelineRef.current,
    play: () => timelineRef.current?.play(),
    pause: () => timelineRef.current?.pause(),
    reverse: () => timelineRef.current?.reverse(),
  };
};
```

### Custom Hook: useDraggable

```typescript
// src/animation/hooks/useDraggable.ts
import { useEffect, useRef } from 'react';
import anime from 'animejs';

interface UseDraggableOptions {
  onDragStart?: () => void;
  onDragEnd?: () => void;
  constrainAxis?: boolean;
}

export const useDraggable = (
  ref: React.RefObject<HTMLElement>,
  options: UseDraggableOptions = {}
) => {
  const draggableRef = useRef<any>(null);

  useEffect(() => {
    if (!ref.current) return;

    draggableRef.current = anime.draggable({
      target: ref.current,
      onDragStart: options.onDragStart,
      onDragEnd: options.onDragEnd,
      constrainAxis: options.constrainAxis,
    });

    return () => {
      draggableRef.current?.reset();
    };
  }, [ref, options]);

  return draggableRef.current;
};
```

---

## ⚙️ Производительность и оптимизация

### 1. Используй только GPU-friendly свойства

```typescript
// ✅ ХОРОШО (GPU)
{
  opacity: 1,
  transform: 'translateX(100px)',
  transform: 'scale(1.1)',
  transform: 'rotate(45deg)',
}

// ❌ ПЛОХО (non-GPU, перерисовка layout)
{
  width: 100,
  height: 100,
  left: 50,
  top: 50,
  padding: 10,
}
```

### 2. Батчирование анимаций (Timeline вместо множественных)

```typescript
// ❌ 5 отдельных anime()
anime({ targets: '.a', opacity: 1 });
anime({ targets: '.b', opacity: 1 });
anime({ targets: '.c', opacity: 1 });

// ✅ 1 Timeline
const timeline = anime.timeline();
timeline.add({ targets: '.a', opacity: 1 });
timeline.add({ targets: '.b', opacity: 1 });
timeline.add({ targets: '.c', opacity: 1 });
```

### 3. Will-change CSS

```typescript
// src/animation/helpers/resolveTokens.ts
const applyWillChange = (target: HTMLElement, properties: string[]) => {
  target.style.willChange = properties.join(', ');

  // Убрать после анимации (избежать утечек памяти)
  setTimeout(() => {
    target.style.willChange = 'auto';
  }, 300);  // После завершения анимации
};
```

### 4. requestAnimationFrame синхронизация

```typescript
// Engine автоматически использует RAF
// Ручная синхронизация (если нужна):
export const syncWithRAF = (callback: () => void) => {
  let rafId: number;

  const tick = () => {
    callback();
    rafId = requestAnimationFrame(tick);
  };

  rafId = requestAnimationFrame(tick);

  return () => cancelAnimationFrame(rafId);
};
```

### 5. Очистка памяти на unmount

```typescript
// Всегда очищай анимации при unmount компонента
useEffect(() => {
  const animation = anime({...});

  return () => {
    animation.pause();
    animation = null;  // Очистить ссылку
  };
}, []);
```

---

## ♿ Доступность (Accessibility)

### prefers-reduced-motion режим

```typescript
// src/animation/helpers/validateMotion.ts
import { theme } from '@/theme';

export const prefersReducedMotion = () => {
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
};

export const getAnimationDuration = (
  normalDuration: number
): number => {
  // Если пользователь просит меньше движений
  if (prefersReducedMotion()) {
    return 0;  // Или очень короткая (50ms для instant feedback)
  }
  return normalDuration;
};

export const getAnimationEasing = (
  normalEasing: string
): string => {
  if (prefersReducedMotion()) {
    return 'linear';  // Без лишних эффектов
  }
  return normalEasing;
};

// Использование
anime({
  targets: '.element',
  opacity: 1,
  duration: getAnimationDuration(theme.duration.normal),
  easing: getAnimationEasing(theme.easing.entrance),
});
```

### Цветовый контраст и читаемость

```typescript
// ✅ Убедись, что анимированные цвета имеют достаточный контраст
{
  color: [theme.colors.textSecondary, theme.colors.primary],
  // theme.colors.primary имеет контраст >= 4.5:1 по WCAG AA
}
```

### Keyboard-friendly анимации

```typescript
// Анимации не должны блокировать клавиатурную навигацию
anime({
  targets: '.modal',
  opacity: [0, 1],
  duration: theme.duration.normal,
  // ❌ ПЛОХО: pointerEvents: 'none', // Блокирует также клавиатуру
  // ✅ ХОРОШО: просто не интерфейр с табуляцией
});
```

---

## ✅ Чек-лист перед merge

Перед тем как закомитить новую анимацию:

- [ ] **Все значения из theme** — нет hardcode миллисекунд, цветов, эйзингов
- [ ] **GPU-friendly свойства** — только transform, opacity, filter
- [ ] **Scope ID** — если в компоненте, то используется data-scope
- [ ] **Cleanup** — useEffect возвращает функцию для очистки
- [ ] **Reduced-motion** — тестировано с преферансой
- [ ] **Mobile-responsive** — анимация работает на всех breakpoints
- [ ] **No alert()** — ошибки показываются через toast или inline
- [ ] **Timeline для сложных** — если >2 элемента, то используется timeline
- [ ] **Тесты** — базовый тест что анимация запускается/заканчивается
- [ ] **Performance** — не более 5 одновременных свойств, батчированы
- [ ] **Доступность** — цветовой контраст, keyboard nav не блокирована
- [ ] **Комментарии** — объяснена логика сложных таймлайнов

---

## 📚 Ссылки на документацию Anime.js V4

| API | Документация | Использование в UXCode Meet |
|-----|--------------|------------------------------|
| **Getting started** | https://animejs.com/documentation/getting-started | Простые анимации (fade, slide) |
| **Timer** | https://animejs.com/documentation/timer | Looping эффекты, skeleton-loader |
| **Animation** | https://animejs.com/documentation/animation | Базовый API для всех анимаций |
| **Timeline** | https://animejs.com/documentation/timeline | Сложные сцены (вход, переходы) |
| **Animatable** | https://animejs.com/documentation/animatable | Какие CSS-свойства можно анимировать |
| **Draggable** | https://animejs.com/documentation/draggable | Перетаскивание стикеров и карточек |
| **Scope** | https://animejs.com/documentation/scope | Изоляция анимаций по компонентам |
| **Events** | https://animejs.com/documentation/events | Колбэки (start, update, complete) |
| **SVG** | https://animejs.com/documentation/svg | Векторные анимации (логотип, иконки) |
| **Text** | https://animejs.com/documentation/text | Текстовые эффекты (осторожно!) |
| **Utilities** | https://animejs.com/documentation/utilities | stagger, random, round |
| **Easings** | https://animejs.com/documentation/easings | Кривые анимации (только из theme!) |
| **WAAPI** | https://animejs.com/documentation/waapi | Web Animation API интеграция |
| **Engine** | https://animejs.com/documentation/engine | Управление движком (pause/play) |

**Официальный GitHub:** https://github.com/juliangarnier/anime

---

## 🚀 Быстрый старт

### 1. Инициализировать Engine при старте приложения

```typescript
// src/main.tsx
import { initializeAnimationEngine } from '@/animation/engine';

initializeAnimationEngine();

ReactDOM.render(<App />, document.getElementById('root'));
```

### 2. Использовать useAnimeScope в компоненте

```typescript
// src/pages/Room.tsx
import { useAnimeScope } from '@/animation/hooks/useAnimeScope';
import { createRoomEntranceTimeline } from '@/animation/presets/roomScenes';
import { useTimelineAnimation } from '@/animation/hooks/useTimelineAnimation';

export const Room = ({ roomId }: Props) => {
  const { containerRef, scopeId } = useAnimeScope({ id: `room-${roomId}` });
  
  const { timeline, play } = useTimelineAnimation(
    `room-entrance-${roomId}`,
    () => createRoomEntranceTimeline(scopeId)
  );

  useEffect(() => {
    play();
  }, [play]);

  return (
    <div ref={containerRef} data-scope={scopeId}>
      {/* Комната */}
    </div>
  );
};
```

### 3. Создавать пресеты для переиспользования

```typescript
// src/animation/presets/yourNewPreset.ts
export const createYourNewAnimation = (scopeId: string) => {
  return anime({
    targets: `[data-scope="${scopeId}"] .your-element`,
    // ...
  });
};
```

---

## 📞 Вопросы и решения

**Q: Как паузировать все анимации на disconnect?**  
A: Используй `animationEngine.pause()` в Socket.IO обработчике.

**Q: Как тестировать анимации?**  
A: Используй `anime.set()` для instant-установки конечного состояния в тестах, или `jest.useFakeTimers()`.

**Q: Как избежать утечек памяти?**  
A: Всегда очищай в useEffect return, регистрируй в scope.

**Q: Какую длительность использовать?**  
A: Всегда из `theme.duration.*` (fast, normal, slow).

**Q: Почему моя анимация лагает?**  
A: Проверь: 1) GPU-friendly? 2) Не более 5 свойств? 3) Батчирована в Timeline?

---

**Status:** ✅ **PRODUCTION-READY**  
**Framework:** Anime.js V4  
**React Integration:** ✅ Custom hooks  
**Accessibility:** ✅ WCAG 2.1 AA  
**Performance:** ✅ GPU-optimized  
**Mobile:** ✅ responsive & tested  

