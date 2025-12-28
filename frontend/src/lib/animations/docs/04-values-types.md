# 04 — Value Types: Типы Значений и Цвета

**Ссылка на документацию**: https://animejs.com/documentation/animation/tween-value-types  
**Версия**: anime.js 4.0+  
**Сложность**: Средняя

---

## 📋 Содержание модуля

1. Типы значений
2. Цвета (Color Values)
3. Относительные значения
4. Функции вычисления значений
5. Примеры и сценарии

---

## 1️⃣ Типы Значений

### Численные значения

```javascript
// Простое число (используется по умолчанию px для трансформ)
animate('.box', {
  x: 100,           // → translateX(100px)
  y: 50,            // → translateY(50px)
  duration: 1000,
});

// Строка с числом
animate('.box', {
  x: '100px',       // Явно указана единица
  width: '50%',     // Процент
  fontSize: '20em', // Em единица
  duration: 1000,
});

// Наследование единиц
animate('.box', { width: '50%' });      // Устанавливает 50%
animate('.box', { width: 75 });         // Наследует % → 75%

// Множественные типы единиц
animate('.box', {
  x: 100,              // px (по умолчанию для трансформ)
  width: '50%',        // %
  fontSize: '1.5rem',  // rem
  duration: 1000,
});
```

### Поддерживаемые единицы

| Единица | Описание | Примеры |
|---------|---------|---------|
| **px** | Пиксели | `100px`, `x: 100` |
| **%** | Проценты | `50%`, `width: '100%'` |
| **em** | Относительно размера шрифта | `1.5em` |
| **rem** | Относительно корневого размера | `2rem` |
| **vw** | % от ширины viewport | `50vw` |
| **vh** | % от высоты viewport | `50vh` |
| **deg** | Градусы | `rotate: 360` |
| **rad** | Радианы | `rotate: '6.28rad'` |
| **turn** | Полные обороты | `rotate: '1turn'` |
| **s** | Секунды (редко) | `'2s'` |
| **ms** | Миллисекунды (редко) | `'2000ms'` |

### Примеры с единицами

```javascript
// Разные единицы
animate('.box', {
  // Трансформации (обычно px)
  x: 100,           // 100px по умолчанию
  x: '10rem',       // 10rem явно
  
  // Размеры
  width: '50%',     // 50% от родителя
  height: '100vh',  // 100% от высоты окна
  
  // Углы
  rotate: 360,      // 360deg по умолчанию
  rotate: '1turn',  // 1 полный оборот
  rotate: '6.28rad', // 2π радиан
  
  duration: 1000,
});
```

---

## 2️⃣ Цвета (Color Values)

### Форматы цветов

```javascript
// Hex цвета
animate('.box', {
  backgroundColor: '#FF0000',        // Красный
  backgroundColor: '#F00',           // Сокращенный формат
  color: '#00FF00',
  borderColor: '#0000FF',
  duration: 1000,
});

// RGB/RGBA
animate('.box', {
  backgroundColor: 'rgb(255, 0, 0)',           // RGB
  color: 'rgba(0, 255, 0, 0.5)',              // RGBA
  borderColor: 'rgba(0, 0, 255, 1)',
  duration: 1000,
});

// HSL/HSLA
animate('.box', {
  backgroundColor: 'hsl(0, 100%, 50%)',       // Красный
  color: 'hsla(120, 100%, 50%, 0.5)',        // Зеленый полупрозрачный
  duration: 1000,
});

// Именованные цвета (CSS)
animate('.box', {
  backgroundColor: 'red',
  color: 'blue',
  borderColor: 'green',
  duration: 1000,
});

// Комбинированные цветовые анимации
animate('.box', {
  backgroundColor: '#FF0000',      // От текущего к красному
  color: 'rgb(0, 255, 0)',        // К зеленому
  borderColor: 'hsl(240, 100%, 50%)',  // К синему
  duration: 1000,
});
```

### Рекомендации по форматам

```javascript
// ✅ РЕКОМЕНДУЕТСЯ - Hex или HSL
animate('.box', {
  backgroundColor: '#FF0000',     // Hex - поддерживается везде
  color: 'hsl(0, 100%, 50%)',    // HSL - удобнее менять оттенок
  duration: 1000,
});

// ⚠️ ОСТОРОЖНО - RGB/RGBA может быть медленнее
animate('.box', {
  backgroundColor: 'rgb(255, 0, 0)',
  duration: 1000,
  // Работает, но может быть менее оптимизировано
});

// ⚠️ ИЗБЕГАЙТЕ - Именованные цвета в анимациях
animate('.box', {
  backgroundColor: 'red',  // Работает, но менее контролируемо
  duration: 1000,
});
```

### Работа с цветовыми пространствами

```javascript
// Анимация оттенка в HSL
const hue = { h: 0 };

animate(hue, {
  h: 360,
  duration: 3000,
  loop: true,
  onUpdate() {
    document.querySelector('.box').style.backgroundColor = 
      `hsl(${hue.h}, 100%, 50%)`;
  }
});

// Более элегантное решение - CSS переменные
// Смотри 03-css-transforms-properties.md
```

---

## 3️⃣ Относительные Значения

### Что такое относительные значения?

Относительные значения позволяют анимировать **от текущего значения** + операция.

### Операторы

| Оператор | Операция | Пример | Результат |
|----------|----------|--------|-----------|
| `+=` | Добавить | `x: '+=100'` | Текущее значение + 100 |
| `-=` | Вычесть | `x: '-=50'` | Текущее значение - 50 |
| `*=` | Умножить | `scale: '*=2'` | Текущее значение × 2 |
| `/=` | Разделить | `scale: '/=2'` | Текущее значение ÷ 2 |

### Примеры относительных значений

```javascript
// Добавить 100px к текущей позиции
animate('.box', {
  x: '+=100',        // Текущее x + 100
  duration: 500,
});

// Вычесть из текущей прозрачности
animate('.box', {
  opacity: '-=0.3',  // Текущее opacity - 0.3
  duration: 500,
});

// Увеличить в 2 раза
animate('.box', {
  scale: '*=2',      // Текущее scale × 2
  duration: 500,
});

// Уменьшить в 2 раза
animate('.box', {
  scale: '/=2',      // Текущее scale ÷ 2
  duration: 500,
});

// Комбинированные относительные значения
animate('.box', {
  x: '+=200',        // Сдвинуть вправо на 200
  y: '-=100',        // Сдвинуть вверх на 100
  scale: '*=1.5',    // Увеличить на 50%
  duration: 1000,
});
```

### Практические примеры

```javascript
// Пример 1: Анимация со смещением от текущей позиции
let currentX = 0;

document.querySelector('.btn').addEventListener('click', () => {
  animate('.box', {
    x: `+=${100}`,   // Каждый клик на 100px дальше
    duration: 300,
  });
  currentX += 100;
});

// Пример 2: Пульсирующая анимация
animate('.pulse', {
  scale: '*=1.2',    // Увеличить на 20%
  duration: 300,
  onComplete() {
    animate('.pulse', {
      scale: '/=1.2',  // Вернуть к исходному размеру
      duration: 300,
    });
  }
});
```

---

## 4️⃣ Функции Вычисления Значений

### Что это?

Функции позволяют вычислить значение для каждого элемента отдельно на основе индекса, элемента или других параметров.

### Синтаксис

```javascript
animate(targets, {
  property: (element, index, arrayOfElements) => {
    // Вычислить и вернуть значение
    return value;
  },
  duration: 1000,
});
```

### Примеры функций

```javascript
// Пример 1: Разные значения для каждого элемента
animate('.item', {
  x: (element, index) => {
    return index * 100;  // 0, 100, 200, 300...
  },
  duration: 1000,
});

// Пример 2: Случайные значения
import { random } from 'animejs';

animate('.item', {
  x: (el, i) => random(0, 200),
  y: (el, i) => random(-50, 50),
  rotate: (el, i) => random(0, 360),
  duration: 1000,
});

// Пример 3: Использование данных элемента
animate('[data-speed]', {
  x: (element, index) => {
    const speed = parseFloat(element.dataset.speed);
    return speed * 100;  // Умножить на коэффициент
  },
  duration: 1000,
});

// Пример 4: Зависит от ширины окна
animate('.item', {
  x: (el, i) => {
    const vw = window.innerWidth / 100;
    return i * vw * 10;  // Зависит от ширины экрана
  },
  duration: 1000,
});

// Пример 5: Комплексная логика
animate('.card', {
  x: (element, index) => {
    if (index % 2 === 0) return 100;
    return -100;  // Чередующееся направление
  },
  opacity: (element, index) => {
    return 1 - (index * 0.1);  // Уменьшающаяся прозрачность
  },
  duration: 1000,
});

// Пример 6: Использование DOM свойств
animate('.item', {
  x: (element, index) => {
    const width = element.offsetWidth;
    return width * 2;  // Анимация на 2 ширины элемента
  },
  duration: 1000,
});
```

---

## 5️⃣ Примеры и Сценарии

### Сценарий 1: Волна эффект

```javascript
import { stagger } from 'animejs';

animate('.item', {
  opacity: [0, 1, 0],
  scale: [0.5, 1, 0.5],
  delay: stagger(100),  // Каждый элемент на 100ms позже
  duration: 1500,
  loop: true,
  ease: 'easeInOutQuad',
});
```

### Сценарий 2: Счетчик с цветом

```javascript
const counter = { value: 0, hue: 0 };

animate(counter, {
  value: 1000,
  hue: 360,  // Меняется цвет
  duration: 2000,
  onUpdate() {
    const el = document.querySelector('.counter');
    el.textContent = Math.round(counter.value);
    el.style.color = `hsl(${counter.hue}, 100%, 50%)`;
  }
});
```

### Сценарий 3: Прогресс бар с цветом

```javascript
const progress = { value: 0 };

animate(progress, {
  value: 100,
  duration: 3000,
  onUpdate() {
    const el = document.querySelector('.progress-bar');
    el.style.width = progress.value + '%';
    
    // Цвет меняется от красного к зеленому
    const hue = progress.value * 1.2;  // 0 (красный) к 120 (зеленый)
    el.style.backgroundColor = `hsl(${hue}, 100%, 50%)`;
  }
});
```

### Сценарий 4: Сетка элементов с волной

```javascript
import { stagger } from 'animejs';

const grid = document.querySelectorAll('.grid-item');

animate(grid, {
  opacity: [0, 1],
  y: [20, 0],
  scale: [0.8, 1],
  delay: stagger({
    start: 0,
    from: 'center',  // Волна от центра
    amount: 300,     // 300ms общей задержки
  }),
  duration: 600,
  ease: 'easeOutQuad',
});
```

---

## 📚 Ссылки на документацию

### Official Documentation
- **Tween Value Types**: https://animejs.com/documentation/animation/tween-value-types
- **Numerical Value**: https://animejs.com/documentation/animation/tween-value-types/numerical-value
- **Color Value**: https://animejs.com/documentation/animation/tween-value-types/color-value
- **Relative Value**: https://animejs.com/documentation/animation/tween-value-types/relative-value
- **Function-based Values**: https://animejs.com/documentation/animation/tween-value-types/function-based

---

## ✅ Контрольный список

- [ ] Знаю все поддерживаемые единицы
- [ ] Могу анимировать цвета в разных форматах
- [ ] Понимаю относительные значения (+=, -=, *=, /=)
- [ ] Могу использовать функции для вычисления значений
- [ ] Знаю как использовать индекс в функциях
- [ ] Готов к 05-timing-easing.md

---

**Следующий файл**: `05-timing-easing.md` — Управление временем и ease функции
