# 10 — Utilities & Engine: Утилиты, Цвета и Вспомогательные Функции

**Ссылка на документацию**: https://animejs.com/documentation/utilities  
**Версия**: anime.js 4.0+  
**Сложность**: Средняя-Продвинутая

---

## 1️⃣ Color Utilities (Работа с Цветами)

### Преобразование цветов

```javascript
import { utils } from 'animejs';

// Получить или установить цвет элемента
utils.set('.box', { backgroundColor: '#FF0000' });
utils.get('.box', 'backgroundColor');

// Работа с CSS переменнымия
utils.set(':root', { '--color': '#FF0000' });
```

---

## 2️⃣ Random Utilities (Случайные Значения)

### random() — случайное число

```javascript
import { random } from 'animejs';

// Случайное число от 0 до 100
animate('.item', {
  x: random(0, 100),
  duration: 1000,
});

// Разные случайные значения для каждого элемента
animate('.item', {
  x: (el, i) => random(0, 200),
  y: (el, i) => random(-50, 50),
  rotate: (el, i) => random(0, 360),
  delay: (el, i) => random(0, 200),
  duration: 1000,
});

// С параметром для каждого элемента
animate('.item', {
  x: random({
    min: 0,
    max: 300,
    count: 5,  // Генерировать 5 значений
  }),
  duration: 1000,
});
```

### createSeededRandom() — детерминированные случайные числа

```javascript
import { createSeededRandom } from 'animejs';

// Создать функцию с фиксированным seed
const seededRandom = createSeededRandom(42);  // Всегда одинаковые числа

animate('.item', {
  x: (el, i) => seededRandom() * 100,
  duration: 1000,
});
```

### randomPick() — выбрать случайный элемент

```javascript
import { randomPick } from 'animejs';

const colors = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00'];

animate('.item', {
  backgroundColor: () => randomPick(colors),
  duration: 1000,
});
```

---

## 3️⃣ Array Utilities (Работа с Массивами)

### shuffle() — перемешать массив

```javascript
import { shuffle } from 'animejs';

const items = [1, 2, 3, 4, 5];
const shuffled = shuffle(items);

animate('.item', {
  x: (el, i) => shuffled[i] * 100,
  delay: (el, i) => i * 100,
  duration: 1000,
});
```

---

## 4️⃣ Math Utilities (Математические функции)

### Основные утилиты

```javascript
import { 
  round, clamp, snap, wrap, mapRange, 
  lerp, damp, degToRad, radToDeg, 
  roundPad, padStart, padEnd 
} from 'animejs';

// round — округление
round(3.7);       // 4
round(3.14, 1);   // 3.1 (1 знак после запятой)

// clamp — ограничение значения
clamp(50, 0, 100);    // 50
clamp(150, 0, 100);   // 100 (ограничено макс)
clamp(-50, 0, 100);   // 0 (ограничено мин)

// snap — привязка к сетке
snap(25, 50);     // 50 (ближайший кратный 50)
snap(37, 10);     // 40 (ближайший кратный 10)

// wrap — циклическое значение
wrap(150, 0, 100); // 50 (150 - 100 = 50)

// mapRange — преобразование диапазона
mapRange(50, 0, 100, 0, 1);     // 0.5
mapRange(25, 0, 100, 0, 360);   // 90 (25% = 90 градусов)

// lerp — линейная интерполяция
lerp(0, 100, 0.5);   // 50 (середина между 0 и 100)

// damp — затухающее движение
damp(10, 0, 0.1, 0.016);  // Плавно к 0

// Конвертация углов
degToRad(180);      // 3.14... (π радиан)
radToDeg(3.14159);  // 180

// Padding
roundPad(12, 3);    // "012"
padStart("5", 3, "0");  // "005"
padEnd("5", 3, "-");    // "5--"
```

---

## 5️⃣ String Utilities (Работа со Строками)

### Очистка inline стилей

```javascript
import { cleanInlineStyles } from 'animejs';

// Удалить inline стили из элемента
const el = document.querySelector('.box');
cleanInlineStyles(el);

// Очистить все transform, opacity и другие inline стили
// Полезно когда нужно вернуть элемент в исходное состояние
```

---

## 6️⃣ DOM Utilities (Работа с DOM)

### set() и get()

```javascript
import { set, get } from 'animejs';

// Установить значение
set('.box', {
  backgroundColor: '#FF0000',
  transform: 'translateX(100px)',
  opacity: 0.5,
});

// Получить значение
const value = get('.box', 'backgroundColor');
console.log(value);

// С множественными элементами
set('.item', { 
  opacity: 0.5,
  x: 100,
});
```

### remove() — удалить элементы

```javascript
import { remove } from 'animejs';

// Удалить элементы из DOM
remove('.temp-element');
remove('.item');
```

---

## 7️⃣ Engine & Performance (Настройки движка)

### Engine параметры

```javascript
import { engine } from 'animejs';

// Установить единицы времени
engine.timeUnit = 's';   // Секунды
engine.timeUnit = 'ms';  // Миллисекунды (по умолчанию)

// Скорость анимаций
engine.speed = 1;    // Нормальная скорость
engine.speed = 0.5;  // Половинная скорость
engine.speed = 2;    // Двойная скорость

// FPS
engine.fps = 60;   // 60 кадров в секунду
engine.fps = 30;   // Более низкие ресурсы

// Точность вычислений
engine.precision = 2;  // 2 знака после запятой

// Пауза при скрытии вкладки
engine.pauseOnDocumentHidden = true;  // По умолчанию true
```

### Контроль движка

```javascript
import { engine } from 'animejs';

engine.pause();   // Пауза всех анимаций
engine.resume();  // Продолжить все анимации
engine.update();  // Принудительное обновление
```

---

## 8️⃣ WAAPI (Web Animation API)

### Использование WAAPI

```javascript
import { waapi } from 'animejs';

// WAAPI версия (использует встроенный Web Animation API)
waapi.animate('.box', {
  x: 100,
  duration: 1000,
  ease: 'easeOutQuad',
});

// Преимущества:
// ✓ Аппаратное ускорение (GPU)
// ✓ Лучшая производительность
// ✗ Меньше функций

// Недостатки vs JS версии:
// ✗ Меньше встроенных ease функций
// ✗ Меньше параметров
// ✗ Сложнее отлаживать
```

---

## 9️⃣ Цепные Функции Утилит

```javascript
import { 
  round, clamp, snap, mapRange, 
  lerp, compose 
} from 'animejs';

// Цепочка преобразований
const transform = (value) => {
  return clamp(round(mapRange(value, 0, 100, 0, 10), 1), 0, 10);
};

const result = transform(75);  // Преобразовать 75 в новый диапазон
```

---

## 🔟 createTimekeeper() — Управление Временем

```javascript
import { createTimekeeper } from 'animejs';

// Создать таймер
const timer = createTimekeeper();

timer.start();      // Начать отсчет
timer.stop();       // Остановить
timer.pause();      // Пауза
timer.resume();     // Продолжить

console.log(timer.time);      // Текущее время в мс
console.log(timer.elapsed);   // Прошедшее время
```

---

## 1️⃣1️⃣ Практические Примеры

### Пример 1: Случайная распределение с ограничением

```javascript
import { random, clamp } from 'animejs';

animate('.item', {
  x: (el, i) => random(0, 300),
  y: (el, i) => random(-100, 100),
  rotation: (el, i) => random(-45, 45),
  delay: (el, i) => clamp(i * 50, 0, 500),  // Максимум 500ms
  duration: 1000,
});
```

### Пример 2: Преобразование значений

```javascript
import { mapRange, lerp, round } from 'animejs';

// Преобразовать прогресс скролла в другой диапазон
const scrollProgress = 0.5;  // 50% скролла
const rotationDegrees = mapRange(scrollProgress, 0, 1, 0, 360);

animate('.spinner', {
  rotate: rotationDegrees,
  duration: 500,
});
```

### Пример 3: Производительность для мобильных

```javascript
import { engine } from 'animejs';

// Определить мобильное устройство
const isMobile = /iPhone|iPad|Android/i.test(navigator.userAgent);

if (isMobile) {
  engine.fps = 30;  // Снизить FPS на мобильных
  engine.speed = 0.8;  // Чуть медленнее анимации
}

// Теперь все анимации будут адаптированы
animate('.box', {
  x: 100,
  duration: 1000,
});
```

---

## 📚 Ссылки на документацию

- **Utilities**: https://animejs.com/documentation/utilities
- **Stagger**: https://animejs.com/documentation/utilities/stagger
- **Random**: https://animejs.com/documentation/utilities/random
- **Math Utilities**: https://animejs.com/documentation/utilities
- **Engine**: https://animejs.com/documentation/engine

---

## ✅ Финальный Контрольный Список

- [ ] Знаю все утилиты для случайных чисел
- [ ] Могу использовать math утилиты
- [ ] Понимаю работу Engine параметров
- [ ] Знаю разницу между JS и WAAPI версиями
- [ ] Завершил все 10 модулей!

---

## 🎓 Итоговая Справка

### Краткая Схема Использования

```
Простая анимация?
├─ YES → animate() → 02-animation-basics.md
└─ NO → Сложная?
    ├─ Временная последовательность?
    │  └─ YES → timeline() → 07-timeline.md
    ├─ Много элементов?
    │  └─ YES → stagger() → 06-keyframes-stagger.md
    ├─ SVG или текст?
    │  └─ YES → SVG/text → 09-svg-text.md
    ├─ Драг или скролл?
    │  └─ YES → draggable()/onScroll() → 08-advanced-features.md
    └─ Нужна оптимизация?
       └─ YES → CSS transforms + engine settings → 03-css + 10-utilities
```

### Быстрые Ссылки на Все Модули

- **00-index.md** — Навигация и обзор
- **01-foundations.md** — Установка и начало
- **02-animation-basics.md** — Базовые анимации
- **03-css-transforms-properties.md** — CSS трансформации
- **04-values-types.md** — Типы значений
- **05-timing-easing.md** — Время и ease
- **06-keyframes-stagger.md** — Keyframes и stagger
- **07-timeline.md** — Композиция
- **08-advanced-features.md** — Продвинутые функции
- **09-svg-text.md** — SVG и текст
- **10-utilities-engine.md** — Утилиты (это файл)

---

## 🚀 Заключение

Вы завершили полное изучение **anime.js Design System**!

Теперь вы знаете:
✅ Все основные API функции
✅ Как оптимизировать анимации
✅ Как создавать сложные последовательности
✅ Как работать с SVG и текстом
✅ Как использовать продвинутые функции
✅ Как отлаживать и повышать производительность

**Желаем успехов в создании интерактивных и плавных анимаций! 🎬**

---

**Дата создания**: 2025-12-17  
**Версия системы**: 1.0  
**Совместимость**: anime.js 4.0+
