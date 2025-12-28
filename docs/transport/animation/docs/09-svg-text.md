# 09 — SVG & Text: Анимация SVG и Текста

**Ссылка на документация**: https://animejs.com/documentation/svg  
**Версия**: anime.js 4.0+  
**Сложность**: Продвинутая

---

## 1️⃣ SVG Атрибуты

### Анимирование SVG элементов

```javascript
// Анимация круга
animate('circle', {
  cx: 200,    // Центр X
  cy: 150,    // Центр Y
  r: 50,      // Радиус
  fill: '#FF0000',
  stroke: '#00FF00',
  duration: 1500,
});

// Анимация пути
animate('path', {
  strokeDashoffset: 0,  // Для stroke-dasharray animations
  strokeWidth: 5,
  fill: '#0000FF',
  duration: 2000,
});

// Множественные элементы
animate('rect', {
  x: 100,
  y: 100,
  width: 200,
  height: 200,
  rx: 10,  // Border radius для rect
  ry: 10,
  duration: 1500,
});

// Line элементы
animate('line', {
  x1: 0,
  y1: 0,
  x2: 200,
  y2: 200,
  stroke: '#FF0000',
  'stroke-width': 2,
  duration: 1000,
});

// Polygon точки (более сложно)
// Обычно через изменение атрибута points
animate('polygon', {
  opacity: 0.5,
  fill: '#00FF00',
  duration: 1000,
});
```

### Stroke-Dasharray анимация (Line Drawing)

```javascript
// Рисование линии
const path = document.querySelector('path');
const length = path.getTotalLength();

animate(path, {
  strokeDashoffset: [length, 0],  // От полного смещения к 0
  duration: 2000,
  ease: 'easeInOutQuad',
  onComplete() {
    console.log('Line drawn!');
  }
});

// CSS для работы dasharray
// path {
//   stroke-dasharray: [length];
//   stroke-dashoffset: [length];
// }
```

---

## 2️⃣ SVG Морфинг (Morphing)

### createDrawable() для морфинга путей

```javascript
import { animate, svg } from 'animejs';

// Создание drawable объекта для морфинга
const drawable = svg.createDrawable('path');

// Анимация рисования
animate(drawable, {
  draw: '0 1',  // От 0% к 100%
  duration: 2000,
  ease: 'easeInOutQuad',
});

// Для морфинга между путями нужно использовать SMIL или другие методы
```

---

## 3️⃣ Motion Path (Движение по пути)

### createMotionPath()

```javascript
import { animate, svg } from 'animejs';

// Анимация объекта по пути
const motionPath = svg.createMotionPath('path#route');

animate('.car', {
  ...motionPath,  // Распаковываем translateX, translateY, rotate
  duration: 5000,
  ease: 'linear',
  loop: true,
});

// Со смещением
const motionPath2 = svg.createMotionPath('path#route', 0.5);  // Начать с 50% пути
```

### HTML пример

```html
<svg viewBox="0 0 400 400">
  <!-- Определяем путь -->
  <path id="route" d="M 10 10 L 200 50 L 350 200 L 200 350 L 50 300" 
        fill="none" stroke="gray" stroke-width="2"/>
  
  <!-- Элемент для движения по пути -->
  <g class="car">
    <circle r="10" fill="red"/>
  </g>
</svg>

<script type="module">
  import { animate, svg } from 'animejs';
  
  const { translateX, translateY, rotate } = svg.createMotionPath('#route');
  
  animate('.car', {
    translateX,
    translateY,
    rotate,
    duration: 5000,
    loop: true,
  });
</script>
```

---

## 4️⃣ Text Splitting (Разделение текста)

### splitText() для анимации букв

```javascript
import { animate, text } from 'animejs';

// Разделить текст на буквы
const splitter = text.splitText({
  element: '.text',  // Селектор или элемент
  chars: true,       // Разделить на буквы
  words: false,      // Не разделять на слова
  lines: false,      // Не разделять на строки
});

// Анимировать каждую букву
animate(splitter.chars, {
  opacity: [0, 1],
  y: [20, 0],
  rotate: [180, 0],
  delay: (char, i) => i * 50,
  duration: 600,
  ease: 'easeOutElastic(1, .8)',
});

// Вернуть текст в исходное состояние
splitter.revert();
```

### Варианты разделения

```javascript
import { text } from 'animejs';

// По словам
const wordSplitter = text.splitText({
  element: '.text',
  words: true,
});

animate(wordSplitter.words, {
  opacity: [0, 1],
  delay: (word, i) => i * 100,
  duration: 500,
});

// По строкам
const lineSplitter = text.splitText({
  element: '.text',
  lines: true,
});

animate(lineSplitter.lines, {
  opacity: [0, 1],
  x: [-50, 0],
  delay: (line, i) => i * 150,
  duration: 600,
});

// По буквам (по умолчанию)
const charSplitter = text.splitText({
  element: '.text',
  chars: true,
});
```

### Параметры splitText

```javascript
const splitter = text.splitText({
  element: '.text',
  lines: true,           // Разделить на строки
  words: true,           // Разделить на слова
  chars: true,           // Разделить на буквы
  debug: false,          // Показать границы
  includespaces: true,   // Включить пробелы
  accessible: true,      // Доступность
  
  // HTML обертка для каждого элемента
  wrap: 'span',          // <span> вокруг каждого
  
  // Класс для каждого элемента
  class: 'char',         // class="char"
  
  // Клонировать элемент
  clone: false,          // Не клонировать
});

// Доступ к разделенным элементам
console.log(splitter.chars);   // Массив букв
console.log(splitter.words);   // Массив слов
console.log(splitter.lines);   // Массив строк
```

---

## 5️⃣ Практические Примеры

### Пример 1: Рисование SVG иконки

```html
<svg viewBox="0 0 100 100">
  <path id="icon" d="M 10 50 L 30 70 L 90 20" 
        stroke="black" stroke-width="4" fill="none" 
        stroke-linecap="round" stroke-linejoin="round"/>
</svg>

<script type="module">
  import { animate } from 'animejs';
  
  const path = document.querySelector('#icon');
  const length = path.getTotalLength();
  
  path.style.strokeDasharray = length;
  path.style.strokeDashoffset = length;
  
  animate(path, {
    strokeDashoffset: 0,
    duration: 1500,
    ease: 'easeOutQuad',
  });
</script>
```

### Пример 2: Анимация букв с эффектом

```html
<h1 class="animated-text">Hello World</h1>

<script type="module">
  import { animate, text, stagger } from 'animejs';
  
  const splitter = text.splitText({
    element: '.animated-text',
    chars: true,
  });
  
  animate(splitter.chars, {
    opacity: [0, 1],
    y: [30, 0],
    rotate: [-90, 0],
    scale: [0.5, 1],
    delay: stagger(50),
    duration: 1000,
    ease: 'easeOutElastic(1, .8)',
  });
</script>
```

### Пример 3: Машина по дороге

```html
<svg viewBox="0 0 400 200">
  <path id="road" d="M 10 100 Q 200 50 390 100" 
        stroke="gray" stroke-width="40" fill="none"/>
  <g class="car">
    <circle cx="0" cy="0" r="8"/>
    <rect x="-15" y="-10" width="30" height="15" fill="blue"/>
  </g>
</svg>

<script type="module">
  import { animate, svg } from 'animejs';
  
  const { translateX, translateY, rotate } = svg.createMotionPath('#road');
  
  animate('.car', {
    ...translateX, ...translateY, ...rotate,
    duration: 4000,
    loop: true,
  });
</script>
```

---

## 📚 Ссылки на документацию

- **SVG**: https://animejs.com/documentation/svg
- **morphTo**: https://animejs.com/documentation/svg/morphto
- **createDrawable**: https://animejs.com/documentation/svg/createdrawable
- **createMotionPath**: https://animejs.com/documentation/svg/createmotionpath
- **Text**: https://animejs.com/documentation/text
- **splitText**: https://animejs.com/documentation/text/splittext

---

## ✅ Контрольный список

- [ ] Знаю как анимировать SVG атрибуты
- [ ] Могу использовать stroke-dasharray для рисования линий
- [ ] Могу использовать createMotionPath для движения по пути
- [ ] Могу разделять текст с splitText
- [ ] Готов к 10-utilities-engine.md

---

**Следующий файл**: `10-utilities-engine.md` — Утилиты и вспомогательные функции
