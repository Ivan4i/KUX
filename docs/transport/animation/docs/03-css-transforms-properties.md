# 03 — CSS Transforms & Properties: Трансформации и CSS Свойства

**Ссылка на документацию**: https://animejs.com/documentation/animation/animatable-properties  
**Версия**: anime.js 4.0+  
**Сложность**: Средняя

---

## 📋 Содержание модуля

1. CSS Трансформации (Transform)
2. CSS Свойства (Properties)
3. CSS Переменные (Variables)
4. Производительность и оптимизация
5. Примеры и паттерны

---

## 1️⃣ CSS Трансформации (Transform)

### Что такое трансформации?

CSS трансформации — это **самый быстрый способ** анимировать элементы, так как они не вызывают переопределение макета (reflow) и перерисовку (repaint).

### Доступные трансформации

| Свойство | Синтаксис | Единица | Значение по умолчанию |
|----------|-----------|---------|---------------------|
| **translateX** (x) | `x: 100` | px | 0px |
| **translateY** (y) | `y: 50` | px | 0px |
| **translateZ** (z) | `z: 100` | px | 0px |
| **rotate** | `rotate: 360` | deg | 0deg |
| **rotateX** | `rotateX: 90` | deg | 0deg |
| **rotateY** | `rotateY: 45` | deg | 0deg |
| **rotateZ** | `rotateZ: 180` | deg | 0deg |
| **scale** | `scale: 1.5` | — | 1 |
| **scaleX** | `scaleX: 1.2` | — | 1 |
| **scaleY** | `scaleY: 0.8` | — | 1 |
| **scaleZ** | `scaleZ: 1.5` | — | 1 |
| **skew** | `skew: 30` | deg | 0deg |
| **skewX** | `skewX: 45` | deg | 0deg |
| **skewY** | `skewY: 30` | deg | 0deg |
| **perspective** | `perspective: 500` | px | 0px |

### Примеры трансформаций

```javascript
import { animate } from 'animejs';

// Перемещение
animate('.box', {
  x: 200,           // translateX
  y: 100,           // translateY
  z: 50,            // translateZ (для 3D)
  duration: 1000,
});

// Вращение
animate('.box', {
  rotate: 360,      // полный оборот
  duration: 2000,
  loop: true,
});

// 3D вращение
animate('.box', {
  rotateX: 90,
  rotateY: 45,
  rotateZ: 30,
  duration: 1500,
});

// Масштабирование
animate('.box', {
  scale: 1.5,       // увеличить на 50%
  duration: 800,
});

// Разные масштабирования по осям
animate('.box', {
  scaleX: 2,        // растянуть по X в 2 раза
  scaleY: 0.5,      // сжать по Y в 2 раза
  duration: 1000,
});

// Наклон
animate('.box', {
  skewX: 30,        // наклон на 30 градусов
  skewY: 15,        // наклон на 15 градусов
  duration: 800,
});

// Комбинированные трансформации
animate('.box', {
  x: 200,
  y: 100,
  rotate: 45,
  scale: 1.2,
  duration: 1200,
  ease: 'easeOutQuad',
});
```

### 3D трансформации с перспективой

```javascript
// Перспектива (нужна для 3D эффекта)
animate('.box', {
  perspective: 500,  // чем меньше, тем более ярко выражена перспектива
  rotateX: 45,
  rotateY: 45,
  duration: 1500,
});

// Более сложный 3D пример
animate('.card', {
  perspective: 800,
  rotateX: [0, 360],
  rotateY: [0, 360],
  duration: 3000,
  loop: true,
  ease: 'linear',
});
```

### Шортханд vs Полная форма

```javascript
// Шортхенд (рекомендуется для anime.js)
animate('.box', {
  x: 100,      // translateX
  y: 50,       // translateY
  rotate: 45,  // rotate
  scale: 1.2,  // scale
});

// Полная форма (для WAAPI)
import { waapi } from 'animejs';

waapi.animate('.box', {
  transform: 'translateX(100px) translateY(50px) rotate(45deg) scale(1.2)',
  duration: 1000,
});
```

---

## 2️⃣ CSS Свойства (Properties)

### Что анимируются?

Любые CSS свойства, которые имеют численное значение или цвет.

### Основные CSS свойства

```javascript
animate('.box', {
  // Размеры
  width: 200,          // px (по умолчанию)
  height: '100%',      // процент
  padding: 20,
  margin: 10,
  
  // Позиционирование
  top: 50,
  left: 100,
  right: 20,
  bottom: 10,
  
  // Границы и фон
  borderRadius: 50,    // px
  borderWidth: 5,
  backgroundColor: '#FF0000',
  
  // Текст
  fontSize: 24,        // px (по умолчанию)
  lineHeight: 1.5,     // без единиц
  letterSpacing: 2,
  
  // Прозрачность (РЕКОМЕНДУЕТСЯ)
  opacity: 0.5,        // 0-1 (самое быстрое!)
  
  // Фильтры
  filter: 'blur(10px)',
  backdropFilter: 'blur(5px)',
  
  // Тени
  boxShadow: '0 10px 20px rgba(0,0,0,0.3)',
  textShadow: '2px 2px 4px rgba(0,0,0,0.5)',
  
  duration: 1000,
});
```

### Важные замечания о производительности

#### ⚠️ ИЗБЕГАЙТЕ эти свойства (вызывают reflow/repaint):
```javascript
// ❌ МЕДЛЕННО - вызывает переопределение макета
animate('.box', {
  width: 300,      // Изменяет макет
  height: 200,     // Изменяет макет
  top: 100,        // Изменяет позицию
  left: 50,        // Изменяет позицию
});
```

#### ✅ БЫСТРО - используйте трансформации:
```javascript
// ✅ БЫСТРО - трансформации не вызывают reflow
animate('.box', {
  x: 100,          // translateX (быстро!)
  y: 50,           // translateY (быстро!)
  scale: 1.5,      // scale (быстро!)
  opacity: 0.5,    // opacity (быстро!)
});
```

### Цвета в CSS свойствах

```javascript
animate('.box', {
  // Hex цвета
  backgroundColor: '#FF0000',
  color: '#00FF00',
  borderColor: '#0000FF',
  
  // RGB/RGBA
  backgroundColor: 'rgb(255, 0, 0)',
  borderColor: 'rgba(0, 255, 0, 0.5)',
  
  // HSL/HSLA
  backgroundColor: 'hsl(0, 100%, 50%)',
  borderColor: 'hsla(120, 100%, 50%, 0.5)',
  
  // Именованные цвета
  backgroundColor: 'red',
  color: 'blue',
  
  duration: 1000,
});
```

### Фильтры CSS

```javascript
animate('.box', {
  // blur — размытие
  filter: 'blur(0px)',     // от 0px до нужного значения
  
  // Или несколько фильтров
  filter: 'blur(10px) brightness(1.2) contrast(1.1)',
  
  duration: 1000,
});

// Отдельная анимация каждого фильтра
animate('.box', {
  // К сожалению, anime.js не может анимировать фильтры отдельно
  // Используйте CSS переменные для каждого фильтра
  '--blur': '10px',
  '--brightness': '1.2',
  '--contrast': '1.1',
  duration: 1000,
});
```

---

## 3️⃣ CSS Переменные (CSS Custom Properties)

### Что это такое?

CSS переменные (custom properties) позволяют хранить значения и использовать их в CSS. Их можно анимировать!

### Примеры с CSS переменными

```html
<div class="box"></div>

<style>
  :root {
    --main-color: #FF0000;
    --blur-amount: 0px;
    --rotation: 0deg;
  }
  
  .box {
    width: 100px;
    height: 100px;
    background: var(--main-color);
    filter: blur(var(--blur-amount));
    transform: rotate(var(--rotation));
  }
</style>

<script type="module">
  import { animate } from 'animejs';
  
  // Анимируем CSS переменные
  animate(':root', {
    '--main-color': '#00FF00',      // Не работает для цветов напрямую
    '--blur-amount': '10px',        // Работает
    '--rotation': '360deg',         // Работает
    duration: 1000,
  });
</script>
```

### Лучший способ: использовать численные переменные

```html
<div class="box"></div>

<style>
  :root {
    --hue: 0;
    --blur: 0;
    --rotation: 0;
  }
  
  .box {
    width: 100px;
    height: 100px;
    background: hsl(var(--hue), 100%, 50%);
    filter: blur(calc(var(--blur) * 1px));
    transform: rotate(calc(var(--rotation) * 1deg));
  }
</style>

<script type="module">
  import { animate } from 'animejs';
  
  // Анимируем численные переменные
  animate(':root', {
    '--hue': 360,        // 0 к 360
    '--blur': 10,        // 0 к 10
    '--rotation': 360,   // 0 к 360
    duration: 2000,
  });
</script>
```

---

## 4️⃣ Производительность и Оптимизация

### Иерархия производительности (от быстрого к медленному)

```
┌────────────────────────────────────┐
│  БЫСТРО - Используйте всегда!     │
├────────────────────────────────────┤
│  1. opacity                        │
│  2. CSS transforms (x, y, rotate,  │
│     scale, skew)                   │
│  3. filter (с осторожностью)       │
├────────────────────────────────────┤
│  СРЕДНЕ - Используйте осторожно    │
├────────────────────────────────────┤
│  4. backgroundColor                │
│  5. boxShadow                      │
│  6. color                          │
├────────────────────────────────────┤
│  МЕДЛЕННО - Избегайте              │
├────────────────────────────────────┤
│  7. width, height                  │
│  8. top, left, right, bottom       │
│  9. margin, padding                │
│  10. borderRadius, borderWidth     │
│  11. All other properties          │
└────────────────────────────────────┘
```

### Рекомендации по оптимизации

```javascript
// ✅ ХОРОШО - Используем трансформации и opacity
animate('.element', {
  x: 100,              // transform (GPU accelerated)
  y: 50,               // transform (GPU accelerated)
  opacity: 0.5,        // opacity (GPU accelerated)
  duration: 1000,
  // Результат: 60 FPS на большинстве устройств
});

// ❌ ПЛОХО - Используем свойства, вызывающие reflow
animate('.element', {
  width: 200,          // Вызывает reflow
  height: 200,         // Вызывает reflow
  left: 100,           // Вызывает reflow
  duration: 1000,
  // Результат: 20-30 FPS, может быть рывки
});

// ✅ ОПТИМИЗАЦИЯ - Комбинируем подходы
animate('.container', {
  // Анимируем позицию через трансформацию
  x: 100,              // Быстро
  y: 50,               // Быстро
  duration: 1000,
});

// Если нужно изменить размер, делаем это через scale:
animate('.box', {
  scale: 1.5,          // Быстро (трансформация)
  duration: 1000,
});

// Вместо:
// width: 150,          // Медленно (reflow)
// height: 150,         // Медленно (reflow)
```

### Hardware Acceleration (GPU)

```javascript
// Убедитесь, что браузер использует GPU для трансформаций
animate('.element', {
  x: 100,
  y: 50,
  scale: 1.2,
  duration: 1000,
  // GPU автоматически используется для трансформаций
  // и opacity
});

// Для явного включения GPU (если нужно):
// Добавьте в CSS:
// will-change: transform, opacity;
// transform: translateZ(0);  // Или backface-visibility: hidden;
```

---

## 5️⃣ Примеры и Паттерны

### Пример 1: Параллакс эффект

```javascript
animate('.parallax-bg', {
  x: -100,           // Фон движется медленнее
  duration: 3000,
});

animate('.parallax-fg', {
  x: -200,           // Передний план движется быстрее
  duration: 3000,
});
```

### Пример 2: Hover эффект с трансформацией

```javascript
const card = document.querySelector('.card');

card.addEventListener('mouseenter', () => {
  animate(card, {
    scale: 1.05,
    y: -10,
    boxShadow: '0 20px 40px rgba(0,0,0,0.3)',
    duration: 300,
    ease: 'easeOutQuad',
  });
});

card.addEventListener('mouseleave', () => {
  animate(card, {
    scale: 1,
    y: 0,
    boxShadow: '0 5px 15px rgba(0,0,0,0.1)',
    duration: 300,
    ease: 'easeOutQuad',
  });
});
```

### Пример 3: Вращающееся колесо с фильтром

```javascript
animate('.wheel', {
  rotate: [0, 360],
  filter: 'blur(0px)',
  duration: 2000,
  loop: true,
  ease: 'linear',
});
```

### Пример 4: Комбинированные трансформации

```javascript
animate('.box', {
  // Комплексная анимация
  x: [0, 100, 50, 0],
  y: [0, 50, 100, 0],
  rotate: [0, 180, 360],
  scale: [1, 1.2, 0.8, 1],
  duration: 3000,
  ease: 'easeInOutQuad',
});
```

---

## 📚 Ссылки на документацию

### Official Documentation
- **CSS Properties**: https://animejs.com/documentation/animation/animatable-properties/css-properties
- **CSS Transforms**: https://animejs.com/documentation/animation/animatable-properties/css-transforms
- **CSS Variables**: https://animejs.com/documentation/animation/animatable-properties/css-variables
- **Animatable Properties**: https://animejs.com/documentation/animation/animatable-properties

### Дополнительные ресурсы
- **MDN CSS Transforms**: https://developer.mozilla.org/en-US/docs/Web/CSS/transform
- **MDN CSS Filters**: https://developer.mozilla.org/en-US/docs/Web/CSS/filter
- **Web Performance**: https://web.dev/animations-guide/

---

## ✅ Контрольный список

- [ ] Знаю все доступные CSS трансформации
- [ ] Понимаю разницу между трансформациями и другими свойствами
- [ ] Могу использовать 3D трансформации с перспективой
- [ ] Знаю, какие свойства быстрые, а какие медленные
- [ ] Могу анимировать CSS переменные
- [ ] Использовал оптимизацию для 60 FPS анимаций
- [ ] Готов к 04-values-types.md

---

**Следующий файл**: `04-values-types.md` — Типы значений и цвета
