# 01 — Foundations: Основы и Установка anime.js

**Ссылка на документацию**: https://animejs.com/documentation/getting-started  
**Версия**: anime.js 4.0+  
**Сложность**: Базовая

---

## 📋 Содержание модуля

1. Установка и импорт
2. Базовые концепции
3. Первая анимация
4. Структура проекта
5. Интеграция с фреймворками
6. TypeScript поддержка

---

## 1️⃣ Установка и Импорт

### NPM установка
```bash
npm install animejs
```

### Импорт в проект

#### ES6 модули (рекомендуется)
```javascript
import anime from 'animejs';

// Или специфичные функции
import { animate, timeline, stagger } from 'animejs';
```

#### CommonJS
```javascript
const anime = require('animejs');
```

#### CDN (быстрый старт)
```html
<!-- jsdelivr CDN -->
<script src="https://cdn.jsdelivr.net/npm/animejs@3/lib/anime.min.js"></script>

<!-- unpkg CDN -->
<script src="https://unpkg.com/animejs@3/lib/anime.min.js"></script>

<script>
  // anime доступен глобально
  anime.animate('.element', { x: 100 });
</script>
```

#### Модульный импорт (WAAPI версия)
```javascript
// JavaScript версия (рекомендуется для большинства случаев)
import { animate } from 'animejs';

// Web Animation API версия (аппаратное ускорение, но меньше функций)
import { waapi } from 'animejs';
```

---

## 2️⃣ Базовые Концепции

### Что такое anime.js?

Anime.js — это легкая библиотека для создания анимаций на JavaScript с поддержкой:
- ✅ CSS свойств и трансформаций
- ✅ SVG атрибутов
- ✅ Объектов JavaScript
- ✅ HTML атрибутов
- ✅ Временных последовательностей (Timeline)
- ✅ Drag and drop анимаций
- ✅ Scroll-triggered анимаций
- ✅ Text splitting и морфинга
- ✅ Встроенных ease функций

### Основные компоненты

```
┌─────────────────────────────────────┐
│     Anime.js Architecture           │
├─────────────────────────────────────┤
│                                     │
│  ┌──────────────────────────────┐   │
│  │   Animation Core             │   │
│  │  (animate function)          │   │
│  └──────────────────────────────┘   │
│           ▲        ▲                │
│           │        │                │
│    ┌──────┴────────┴──────┐         │
│    │                      │         │
│  Timeline            Advanced       │
│  (Composition)       (Draggable,    │
│                      Scroll,        │
│                      SVG, Text)     │
│                                     │
│  ┌──────────────────────────────┐   │
│  │   Engine & Utilities         │   │
│  │  (Eases, Stagger, Colors)    │   │
│  └──────────────────────────────┘   │
│                                     │
└─────────────────────────────────────┘
```

### Ключевые термины

| Термин | Описание | Пример |
|--------|---------|--------|
| **Target** | Элемент(ы), которые анимируются | CSS селектор, DOM элемент, объект |
| **Property** | Свойство, которое изменяется | `x`, `opacity`, `rotate` |
| **Value** | Целевое значение свойства | `100`, `'#FF0000'`, `[0, 100, 200]` |
| **Duration** | Время анимации в миллисекундах | `1000` (1 секунда) |
| **Delay** | Задержка перед началом в мс | `500` |
| **Ease** | Функция ослабления (timing function) | `'easeOutQuad'` |
| **Loop** | Количество повторений или `true` для бесконечного | `true` или `3` |
| **Keyframes** | Последовательность значений для одного свойства | `[0, 50, 100]` |

---

## 3️⃣ Первая Анимация

### Минимальный пример

```html
<div class="box"></div>

<style>
  .box {
    width: 50px;
    height: 50px;
    background: #FF6B6B;
  }
</style>

<script type="module">
  import { animate } from 'animejs';
  
  // Простая анимация
  animate('.box', {
    x: 200,           // двигаем на 200px вправо
    duration: 1000,   // 1 секунда
  });
</script>
```

### Анимация с параметрами

```javascript
import { animate } from 'animejs';

const animation = animate('.box', {
  // Целевые свойства
  x: 200,
  opacity: 0.5,
  rotate: 360,
  
  // Параметры анимации
  duration: 2000,
  delay: 500,
  ease: 'easeOutQuad',
  
  // Callbacks (обратные вызовы)
  onBegin() {
    console.log('Анимация началась');
  },
  onComplete() {
    console.log('Анимация завершена');
  }
});

// Управление анимацией
animation.play();
animation.pause();
animation.restart();
```

---

## 4️⃣ Структура Проекта

### Рекомендованная структура для проекта с anime.js

```
project/
├── index.html
├── css/
│   ├── styles.css
│   └── animations.css
├── js/
│   ├── main.js
│   ├── animations/
│   │   ├── hero.js
│   │   ├── buttons.js
│   │   ├── scroll.js
│   │   └── interactive.js
│   └── config.js
├── assets/
│   ├── images/
│   └── svg/
└── package.json
```

### Лучшие практики для организации кода

```javascript
// config.js — конфигурация глобальных параметров
export const ANIMATION_CONFIG = {
  defaultDuration: 600,
  defaultEase: 'easeOutQuad',
  staggerDelay: 100,
};

// animations/hero.js — модуль для одного компонента
import { animate, timeline } from 'animejs';
import { ANIMATION_CONFIG } from '../config.js';

export function initHeroAnimation() {
  const tl = timeline();
  
  tl.add({
    targets: '.hero-title',
    opacity: [0, 1],
    y: [50, 0],
    duration: ANIMATION_CONFIG.defaultDuration,
    ease: ANIMATION_CONFIG.defaultEase,
  });
  
  return tl;
}

// main.js — инициализация
import { initHeroAnimation } from './animations/hero.js';

document.addEventListener('DOMContentLoaded', () => {
  const heroTl = initHeroAnimation();
  heroTl.play();
});
```

---

## 5️⃣ Интеграция с Фреймворками

### React

```jsx
import { useEffect, useRef } from 'react';
import { animate } from 'animejs';

export function AnimatedBox() {
  const boxRef = useRef(null);

  useEffect(() => {
    if (boxRef.current) {
      animate(boxRef.current, {
        x: 200,
        duration: 1000,
      });
    }
  }, []);

  return <div ref={boxRef} className="box" />;
}
```

### Vue

```vue
<template>
  <div ref="boxEl" class="box"></div>
</template>

<script>
import { animate } from 'animejs';

export default {
  mounted() {
    animate(this.$refs.boxEl, {
      x: 200,
      duration: 1000,
    });
  }
}
</script>
```

### Angular

```typescript
import { Component, ViewChild, ElementRef, AfterViewInit } from '@angular/core';
import { animate } from 'animejs';

@Component({
  selector: 'app-animated-box',
  template: '<div #box class="box"></div>'
})
export class AnimatedBoxComponent implements AfterViewInit {
  @ViewChild('box') boxEl!: ElementRef;

  ngAfterViewInit() {
    animate(this.boxEl.nativeElement, {
      x: 200,
      duration: 1000,
    });
  }
}
```

### Svelte

```svelte
<script>
  import { animate } from 'animejs';
  import { onMount } from 'svelte';

  let boxEl;

  onMount(() => {
    animate(boxEl, {
      x: 200,
      duration: 1000,
    });
  });
</script>

<div bind:this={boxEl} class="box"></div>
```

---

## 6️⃣ TypeScript Поддержка

### Установка типов

```bash
# Типы входят в пакет anime.js
npm install animejs
# Типы автоматически загружаются из @types/animejs или из самого пакета
```

### Использование с TypeScript

```typescript
import { animate, timeline, AnimeParams } from 'animejs';

// Типизированные параметры
const params: AnimeParams = {
  targets: '.box',
  x: 100,
  duration: 1000,
  ease: 'easeOutQuad',
  onComplete: () => {
    console.log('Done');
  }
};

const anim = animate(params);

// Timeline с типами
const tl = timeline({
  autoplay: false,
});

tl.add({
  targets: '.element',
  opacity: 1,
  duration: 600,
}, 0);
```

### Типизированные функции утилит

```typescript
import { stagger, spring, eases, random } from 'animejs';

// stagger для последовательных анимаций
const staggerValue = stagger(100);

// spring ease
const springEase = spring({ damping: 0.8, mass: 1.2 });

// встроенные ease функции
const easeFunc = eases.outElastic(0.8, 1.2);

// случайные значения
const randomValue = random(10, 100);
```

---

## 🔧 Отладка и Проверка

### Консоль браузера

```javascript
// Проверка версии
console.log(anime.version);

// Информация об анимации
const anim = animate('.box', { x: 100 });
console.log(anim);
// Выведет объект с информацией об анимации

// Проверка состояния
console.log(anim.progress);  // от 0 до 1
console.log(anim.paused);    // boolean
```

### Использование browser-control MCP для отладки

```bash
# Открыть документацию
browser-control navigate "https://animejs.com/documentation/getting-started"

# Проверить примеры
browser-control navigate "https://animejs.com"
```

---

## 📚 Ссылки на документацию

### Official Documentation
- **Main**: https://animejs.com/documentation
- **Getting Started**: https://animejs.com/documentation/getting-started
- **Installation**: https://animejs.com/documentation/getting-started/installation
- **Module Imports**: https://animejs.com/documentation/getting-started/module-imports
- **Using with Vanilla JS**: https://animejs.com/documentation/getting-started/using-with-vanilla-js
- **Using with React**: https://animejs.com/documentation/getting-started/using-with-react

### GitHub Resources
- **Repository**: https://github.com/juliangarnier/anime
- **Issues & Discussions**: https://github.com/juliangarnier/anime/issues
- **Migration Guide (v3 to v4)**: https://github.com/juliangarnier/anime/blob/master/docs/MIGRATION.md

---

## ✅ Контрольный список для начинающих

- [ ] Установлена библиотека via npm или CDN
- [ ] Импорт работает без ошибок
- [ ] Первая простая анимация создана и работает
- [ ] Понимаю разницу между targets, properties и values
- [ ] Знаю как использовать delay, duration, ease
- [ ] Могу вывести и проверить объект анимации в консоли
- [ ] Проверил совместимость с моим браузером
- [ ] Готов перейти к 02-animation-basics.md

---

**Следующий файл**: `02-animation-basics.md` — Базовые анимации и параметры
