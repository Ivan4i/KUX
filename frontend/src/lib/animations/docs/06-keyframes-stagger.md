# 06 — Keyframes & Stagger: Keyframes и Последовательные Эффекты

**Ссылка на документацию**: https://animejs.com/documentation/animation/keyframes  
**Версия**: anime.js 4.0+  
**Сложность**: Средняя-Продвинутая

---

## 1️⃣ Property Keyframes

### Массив значений

```javascript
// Простой массив (плавная последовательность)
animate('.box', {
  x: [0, 100, 200, 0],   // 0 → 100 → 200 → 0
  duration: 2000,
});

// С одинаковым временем для каждого этапа
animate('.box', {
  x: [0, 100, 200, 0],
  opacity: [1, 0.5, 0.3, 1],
  duration: 3000,
  // Все этапы занимают одинаковое время
});

// Разные стартовые значения
animate('.box', {
  x: [null, 100, 200],   // От текущего значения
  duration: 2000,
});
```

### Параметров Keyframes (Tween параметры)

```javascript
// С параметрами для каждого keyframe
animate('.box', {
  x: [
    { value: 100, duration: 500, ease: 'easeInQuad' },
    { value: 200, duration: 300, ease: 'easeOutQuad' },
    { value: 0,   duration: 400, ease: 'linear' }
  ],
  duration: 3000,  // Общая длительность
});

// Shorthand параметры
animate('.box', {
  x: [
    { to: 100 },
    { to: 200 },
    { to: 0 }
  ],
  duration: 2000,
});

// С delay для каждого этапа
animate('.box', {
  x: [
    { to: 100, delay: 0 },
    { to: 200, delay: 200 },
    { to: 0,   delay: 100 }
  ],
  duration: 3000,
});
```

---

## 2️⃣ Animation Keyframes (Множественные свойства)

### Duration-based Keyframes

```javascript
// Последовательность анимаций разных свойств
animate('.box', {
  keyframes: [
    { x: 100, y: 0 },        // Этап 1
    { x: 100, y: 100 },      // Этап 2
    { x: 0,   y: 100 },      // Этап 3
    { x: 0,   y: 0 }         // Этап 4
  ],
  duration: 3000,
  ease: 'easeInOutQuad',
});

// Разные ease для разных этапов
animate('.box', {
  keyframes: [
    { x: 100, ease: 'easeInQuad' },
    { x: 200, ease: 'easeOutQuad' },
    { x: 0,   ease: 'linear' }
  ],
  duration: 3000,
});
```

### Percentage-based Keyframes

```javascript
// Процентная разбивка времени
animate('.box', {
  keyframes: {
    '0%':   { x: 0,   y: 0,   opacity: 0 },
    '25%':  { x: 100, y: 0,   opacity: 1 },
    '50%':  { x: 100, y: 100, opacity: 1 },
    '75%':  { x: 0,   y: 100, opacity: 1 },
    '100%': { x: 0,   y: 0,   opacity: 0 }
  },
  duration: 4000,
  ease: 'easeInOutCubic',
});

// Гибкое распределение
animate('.box', {
  keyframes: {
    '0%':   { scale: 0 },
    '50%':  { scale: 1.5 },
    '100%': { scale: 1 }
  },
  duration: 1500,
});
```

---

## 3️⃣ Stagger (Последовательное Распределение)

### Время Stagger

```javascript
import { stagger } from 'animejs';

// Простой численный stagger (задержка в мс)
animate('.item', {
  opacity: [0, 1],
  delay: stagger(100),  // 0, 100, 200, 300, 400...
  duration: 600,
});

// С диапазоном (range)
animate('.item', {
  opacity: [0, 1],
  delay: stagger({
    start: 0,
    amount: 500,   // Общая задержка 500ms
    from: 'first',  // От первого элемента
  }),
  duration: 600,
});

// От центра
animate('.item', {
  opacity: [0, 1],
  delay: stagger({
    amount: 300,
    from: 'center', // Волна от центра
  }),
  duration: 600,
});

// От последнего
animate('.item', {
  opacity: [0, 1],
  delay: stagger({
    amount: 400,
    from: 'last',   // Волна от конца
  }),
  duration: 600,
});

// Обратный порядок
animate('.item', {
  opacity: [0, 1],
  delay: stagger({
    amount: 300,
    reversed: true,  // Обратный порядок
  }),
  duration: 600,
});
```

### Значения Stagger

```javascript
import { stagger } from 'animejs';

// Распределение значений (не задержка, а саму значения)
animate('.item', {
  scale: stagger([0.5, 1.5]),  // От 0.5 к 1.5 для каждого
  duration: 800,
  ease: 'easeOutQuad',
});

// Диапазон значений
animate('.item', {
  rotate: stagger({
    start: -45,
    amount: 90,    // От -45 до 45
  }),
  duration: 1000,
});

// С ease для stagger значений
animate('.item', {
  opacity: stagger({
    start: 0,
    amount: 1,
    ease: 'easeOutQuad',
  }),
  duration: 800,
});
```

### Grid Stagger (Сетка)

```javascript
import { stagger } from 'animejs';

// Двумерный stagger для сетки
const container = document.querySelector('.grid');
const items = container.querySelectorAll('.item');

animate(items, {
  opacity: [0, 1],
  y: [50, 0],
  delay: stagger({
    grid: [3, 3],        // 3x3 сетка
    from: 'center',      // Волна от центра
    amount: 400,
  }),
  duration: 800,
  ease: 'easeOutCubic',
});

// С параметрами оси
animate(items, {
  opacity: [0, 1],
  delay: stagger({
    grid: [4, 4],
    from: 'center',
    axis: 'x',           // Волна по оси X
    amount: 300,
  }),
  duration: 600,
});
```

---

## 4️⃣ Практические Примеры

### Пример 1: Типичная волна элементов

```javascript
import { stagger } from 'animejs';

animate('.card', {
  opacity: [0, 1],
  y: [30, 0],
  delay: stagger(100, { start: 200 }),  // Начать с 200ms
  duration: 600,
  ease: 'easeOutCubic',
});
```

### Пример 2: Сложная последовательность

```javascript
animate('.box', {
  keyframes: {
    '0%':   { x: 0,   rotate: 0 },
    '25%':  { x: 100, rotate: 90 },
    '50%':  { x: 100, rotate: 180 },
    '75%':  { x: 0,   rotate: 270 },
    '100%': { x: 0,   rotate: 360 }
  },
  duration: 3000,
  loop: true,
  ease: 'linear',
});
```

### Пример 3: Загрузка с растущей полосой

```javascript
animate('.progress', {
  keyframes: [
    { width: '0%' },
    { width: '30%', duration: 1000 },
    { width: '60%', duration: 1500 },
    { width: '100%', duration: 500 }
  ],
  duration: 5000,
  ease: 'easeInOutQuad',
});
```

### Пример 4: Сетка с волной

```javascript
import { stagger } from 'animejs';

const grid = document.querySelectorAll('.grid-item');

animate(grid, {
  opacity: [0, 1],
  scale: [0.8, 1],
  rotate: [15, 0],
  delay: stagger({
    grid: [5, 4],        // 5 колонок, 4 ряда
    from: 'center',
    amount: 600,
  }),
  duration: 1000,
  ease: 'easeOutQuad',
});
```

---

## 📚 Ссылки на документацию

- **Keyframes**: https://animejs.com/documentation/animation/keyframes
- **Tween Values Keyframes**: https://animejs.com/documentation/animation/keyframes/tween-values-keyframes
- **Tween Parameters Keyframes**: https://animejs.com/documentation/animation/keyframes/tween-parameters-keyframes
- **Percentage-based Keyframes**: https://animejs.com/documentation/animation/keyframes/percentage-based-keyframes
- **Stagger**: https://animejs.com/documentation/utilities/stagger

---

## ✅ Контрольный список

- [ ] Могу использовать простые массивы keyframes
- [ ] Могу использовать параметр keyframes для множественных свойств
- [ ] Знаю разницу между duration-based и percentage-based keyframes
- [ ] Могу использовать стандартный stagger с задержкой
- [ ] Могу использовать grid stagger для сеток
- [ ] Готов к 07-timeline.md

---

**Следующий файл**: `07-timeline.md` — Timeline композиция
