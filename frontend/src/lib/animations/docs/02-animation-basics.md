# 02 — Animation Basics: Базовые Анимации и Параметры

**Ссылка на документацию**: https://animejs.com/documentation/animation  
**Версия**: anime.js 4.0+  
**Сложность**: Базовая-Средняя

---

## 📋 Содержание модуля

1. Функция animate()
2. Таргеты (Targets)
3. Свойства и значения
4. Основные параметры
5. Callbacks и события
6. Примеры использования

---

## 1️⃣ Функция animate()

### Синтаксис

```javascript
import { animate } from 'animejs';

// Базовый синтаксис
animate(targets, params);

// Возвращает объект Animation
const animation = animate(targets, params);
```

### Возвращаемое значение

```javascript
const animation = animate('.box', { x: 100, duration: 1000 });

// Объект Animation содержит методы:
animation.play();      // Начать/продолжить
animation.pause();     // Пауза
animation.reverse();   // Обратное направление
animation.seek(500);   // Перейти к 500ms
animation.restart();   // Начать заново
animation.complete();  // Перейти в конец
animation.reset();     // Вернуться в начало

// Свойства
console.log(animation.progress);   // 0-1
console.log(animation.paused);     // boolean
console.log(animation.reversed);   // boolean
```

---

## 2️⃣ Таргеты (Targets)

### Типы таргетов

#### CSS селекторы (строки)
```javascript
animate('.element', { x: 100 });
animate('#unique-id', { opacity: 0.5 });
animate('[data-animate="true"]', { rotate: 360 });
animate('div.special > span', { y: 50 });
```

#### DOM элементы
```javascript
const element = document.querySelector('.box');
animate(element, { x: 100 });

const elements = document.querySelectorAll('.item');
animate(elements, { opacity: 1 });
```

#### Массивы элементов
```javascript
const el1 = document.querySelector('.box1');
const el2 = document.querySelector('.box2');
const el3 = document.querySelector('.box3');

animate([el1, el2, el3], { x: 100 });
```

#### Объекты JavaScript
```javascript
const obj = { value: 0, count: 100 };

const anim = animate(obj, { 
  value: 100,
  count: 200,
  onUpdate() {
    console.log(obj.value);  // Меняется во время анимации
  }
});
```

#### Смешанные таргеты
```javascript
const el1 = document.querySelector('.box1');
const obj = { x: 0 };

animate([el1, obj], { 
  x: 100,  // Работает для обоих
  duration: 1000 
});
```

### Селекторы для множественных элементов

```javascript
// Все элементы с классом
animate('.item', { x: 100 });

// Все элементы в контейнере
animate('.container .item', { x: 100 });

// nth-child селекторы
animate('.item:nth-child(odd)', { rotate: 90 });
animate('.item:nth-child(3n+1)', { scale: 1.2 });

// Атрибуты
animate('[data-type="card"]', { y: 50 });
animate('[disabled]', { opacity: 0.5 });

// Псевдо-классы (работает для hover, focus и т.д.)
animate(':hover', { scale: 1.1 });
```

---

## 3️⃣ Свойства и Значения

### Анимируемые свойства

#### CSS свойства
```javascript
animate('.box', {
  opacity: 0.5,              // 0-1
  backgroundColor: '#FF0000', // Цвет
  borderRadius: 50,          // px (числовое значение)
  fontSize: '20px',          // С единицей
  filter: 'blur(10px)',      // Фильтр
  width: '100%',             // % или другие единицы
  lineHeight: 1.5,           // Без единиц
});
```

#### CSS трансформации (рекомендуется использовать)
```javascript
animate('.box', {
  x: 100,           // translateX (px)
  y: 50,            // translateY (px)
  z: 100,           // translateZ (px)
  rotate: 360,      // rotate (deg по умолчанию)
  rotateX: 90,      // rotateX (deg)
  rotateY: 45,      // rotateY (deg)
  skewX: 30,        // skewX (deg)
  skewY: 15,        // skewY (deg)
  scale: 1.5,       // scale (без единиц)
  scaleX: 1.2,      // scaleX (без единиц)
  scaleY: 0.8,      // scaleY (без единиц)
});
```

#### SVG свойства
```javascript
// Атрибуты SVG элементов
animate('circle', {
  cx: 100,   // Центр X
  cy: 50,    // Центр Y
  r: 30,     // Радиус
  opacity: 0.5,
  stroke: '#FF0000',
  fill: '#00FF00',
});

// Path атрибуты
animate('path', {
  strokeDashoffset: 100,
  strokeWidth: 2,
  d: 'M10 10 L 90 90',  // Path definition
});
```

### Типы значений

```javascript
// Числовое значение (по умолчанию px для трансформ)
animate('.box', { x: 100 });

// Строка с единицей
animate('.box', { width: '50%', height: '10rem' });

// Цвет
animate('.box', { backgroundColor: 'rgb(255, 0, 0)' });

// Относительное значение
animate('.box', { x: '+=100' });  // Добавить 100
animate('.box', { y: '-=50' });   // Вычесть 50
animate('.box', { scale: '*=2' }); // Умножить на 2

// Функция (вычисляется для каждого элемента)
animate('.item', {
  x: (element, index) => index * 100,
  delay: (element, index) => index * 100,
});

// Массив (keyframes)
animate('.box', { x: [0, 100, 200, 0] });
```

---

## 4️⃣ Основные Параметры

### Временные параметры

```javascript
animate('.box', {
  x: 100,
  
  // Duration (длительность в миллисекундах)
  duration: 1000,    // 1 секунда (по умолчанию 1000)
  
  // Delay (задержка перед началом в миллисекундах)
  delay: 500,        // Жди 500ms перед началом
  
  // Autoplay (автоматический старт)
  autoplay: true,    // true по умолчанию
});
```

### Параметры движения

```javascript
animate('.box', {
  x: 100,
  
  // Ease (функция ослабления)
  ease: 'easeOutQuad',           // Встроенная ease функция
  ease: 'easeOutElastic(0.8, 1.2)', // С параметрами
  ease: 'linear',                // Линейное движение
  ease: 'spring(0.8, 1, 0.6)',  // Spring анимация
  
  // Loop (повторение)
  loop: false,       // Без повторений (по умолчанию)
  loop: true,        // Бесконечное повторение
  loop: 3,           // Повторить 3 раза
  
  // Alternate (туда-обратно)
  alternate: false,  // Не менять направление
  alternate: true,   // После каждого цикла менять направление
  
  // Reversed (запустить в обратном направлении)
  reversed: false,   // Нормальное направление
  reversed: true,    // Обратное направление
});
```

### Полный пример со всеми параметрами

```javascript
animate('.box', {
  // Свойства
  x: 100,
  opacity: 0.5,
  rotate: 360,
  
  // Время
  duration: 1000,
  delay: 200,
  
  // Движение
  ease: 'easeOutQuad',
  loop: 2,
  alternate: true,
  
  // Callbacks
  onBegin() {
    console.log('Анимация началась');
  },
  onUpdate() {
    console.log('Обновление кадра');
  },
  onComplete() {
    console.log('Анимация завершена');
  },
});
```

---

## 5️⃣ Callbacks и События

### Жизненный цикл анимации

```
┌─────────────────────────────────────┐
│      Animation Lifecycle            │
├─────────────────────────────────────┤
│                                     │
│  animate() вызвана                  │
│       ▼                             │
│  onBegin() ◄─ Анимация началась    │
│       ▼                             │
│  onBeforeUpdate() ◄─ Перед обнов   │
│       ▼                             │
│  onUpdate() ◄─ Каждый кадр          │
│       ▼                             │
│  onRender() ◄─ После рендеринга    │
│       ▼ (повторяется каждый кадр)   │
│       ▼                             │
│  onLoop() ◄─ При повторении        │
│       ▼                             │
│  onComplete() ◄─ Конец             │
│       ▼                             │
│  .then() ◄─ Promise выполнена      │
│                                     │
└─────────────────────────────────────┘
```

### Callback функции

```javascript
animate('.box', {
  x: 100,
  
  // onBegin — вызывается в начале анимации (один раз)
  onBegin: function(anim) {
    console.log('Началась');
    console.log(anim);  // Объект Animation
  },
  
  // onBeforeUpdate — вызывается перед обновлением (каждый кадр)
  onBeforeUpdate: function(anim) {
    console.log('Перед обновлением');
  },
  
  // onUpdate — вызывается при обновлении значений (каждый кадр)
  onUpdate: function(anim) {
    console.log('Прогресс:', anim.progress);  // 0-1
  },
  
  // onRender — вызывается после рендеринга (каждый кадр)
  onRender: function(anim) {
    console.log('Отрендерено');
  },
  
  // onLoop — вызывается при завершении цикла (если loop > 1)
  onLoop: function(anim) {
    console.log('Цикл завершен');
  },
  
  // onComplete — вызывается в конце анимации (один раз)
  onComplete: function(anim) {
    console.log('Завершена');
  },
  
  // onPause — вызывается при паузе
  onPause: function(anim) {
    console.log('На паузе');
  },
});
```

### Promise-based синтаксис

```javascript
// Использование .then()
animate('.box', {
  x: 100,
  duration: 1000,
}).then(() => {
  console.log('Анимация завершена!');
  // Запустить следующую анимацию
  return animate('.box', { y: 100, duration: 1000 });
}).then(() => {
  console.log('Обе анимации завершены!');
});

// Использование async/await
async function animateSequence() {
  await animate('.box', { x: 100, duration: 1000 });
  console.log('Первая завершена');
  
  await animate('.box', { y: 100, duration: 1000 });
  console.log('Вторая завершена');
}

animateSequence();
```

---

## 6️⃣ Примеры Использования

### Пример 1: Простая анимация кнопки при клике

```html
<button class="btn">Click Me</button>

<style>
  .btn {
    padding: 10px 20px;
    font-size: 16px;
  }
</style>

<script type="module">
  import { animate } from 'animejs';
  
  const btn = document.querySelector('.btn');
  
  btn.addEventListener('click', () => {
    animate(btn, {
      scale: [1, 0.95, 1],  // Пульс эффект
      duration: 300,
      ease: 'easeOutQuad',
    });
  });
</script>
```

### Пример 2: Анимация появления элементов

```javascript
animate('.item', {
  opacity: [0, 1],     // От 0 к 1
  y: [50, 0],          // От 50px к 0
  duration: 600,
  delay: (el, i) => i * 100,  // Каждый элемент со смещением
  ease: 'easeOutCubic',
});
```

### Пример 3: Анимация счетчика

```javascript
const counter = { value: 0 };

animate(counter, {
  value: 1000,
  duration: 2000,
  ease: 'easeOutQuad',
  onUpdate: () => {
    document.querySelector('.counter').textContent = 
      Math.round(counter.value);
  },
});
```

### Пример 4: Бесконечная анимация загрузки

```javascript
animate('.loader', {
  rotate: 360,
  duration: 2000,
  loop: true,
  ease: 'linear',
});
```

### Пример 5: Анимация с управлением

```javascript
const anim = animate('.box', {
  x: 300,
  duration: 3000,
  autoplay: false,  // Не запускать автоматически
});

// Управление
document.querySelector('.play-btn').addEventListener('click', () => {
  anim.play();
});

document.querySelector('.pause-btn').addEventListener('click', () => {
  anim.pause();
});

document.querySelector('.reverse-btn').addEventListener('click', () => {
  anim.reverse();
});

document.querySelector('.restart-btn').addEventListener('click', () => {
  anim.restart();
});
```

---

## 🔍 Отладка Анимаций

### Вывод информации об анимации

```javascript
const anim = animate('.box', { x: 100, duration: 1000 });

console.log(anim);
// Выведет объект с информацией:
// {
//   targets: [...],
//   animations: [...],
//   duration: 1000,
//   delay: 0,
//   progress: 0,
//   paused: true,
//   reversed: false,
//   ...методы
// }
```

### Логирование во время анимации

```javascript
animate('.box', {
  x: 100,
  duration: 1000,
  onBegin(anim) {
    console.log('Start:', anim.progress);      // 0
  },
  onUpdate(anim) {
    console.log('Progress:', (anim.progress * 100).toFixed(0) + '%');
  },
  onComplete(anim) {
    console.log('End:', anim.progress);        // 1
  },
});
```

### Использование browser-control MCP

```bash
# Открыть документацию по анимации
browser-control navigate "https://animejs.com/documentation/animation"

# Открыть примеры
browser-control navigate "https://animejs.com"
```

---

## 📚 Ссылки на документацию

### Official Documentation
- **Animation API**: https://animejs.com/documentation/animation
- **Targets**: https://animejs.com/documentation/animation/targets
- **Animatable Properties**: https://animejs.com/documentation/animation/animatable-properties
- **Tween Parameters**: https://animejs.com/documentation/animation/tween-parameters
- **Callbacks**: https://animejs.com/documentation/animation/animation-callbacks
- **Methods**: https://animejs.com/documentation/animation/animation-methods

---

## ✅ Контрольный список

- [ ] Понимаю различие между targets, properties и values
- [ ] Могу использовать CSS селекторы для таргетирования
- [ ] Знаю разницу между duration и delay
- [ ] Могу использовать callbacks для отслеживания анимации
- [ ] Могу управлять анимацией методами (play, pause, restart)
- [ ] Использовал Promise-based синтаксис с .then()
- [ ] Отладил анимацию через консоль браузера
- [ ] Готов к 03-css-transforms-properties.md

---

**Следующий файл**: `03-css-transforms-properties.md` — CSS трансформации и свойства
