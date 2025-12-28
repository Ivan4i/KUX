# 05 — Timing & Easing: Управление Временем и Ease Функции

**Ссылка на документацию**: https://animejs.com/documentation/animation/animation-playback-settings  
**Версия**: anime.js 4.0+  
**Сложность**: Средняя

---

## 1️⃣ Duration (Длительность)

```javascript
animate('.box', {
  x: 100,
  duration: 1000,  // 1 секунда (миллисекунды!)
  // Стандартное значение: 1000ms
});

// Разные продолжительности
animate('.box', {
  x: 100,
  duration: 300,   // Быстро (0.3 сек)
});

animate('.box', {
  x: 100,
  duration: 2000,  // Медленно (2 сек)
});

// Разные длительности для разных свойств
// Для каждого свойства через keyframes или delay
```

---

## 2️⃣ Delay (Задержка)

```javascript
// Общая задержка перед началом
animate('.box', {
  x: 100,
  delay: 500,      // Жди 500ms перед началом
  duration: 1000,
});

// Разная задержка для каждого элемента (функция)
animate('.item', {
  x: 100,
  delay: (el, i) => i * 100,  // 0, 100, 200, 300...
  duration: 1000,
});

// Используя stagger для более удобной задержки
import { stagger } from 'animejs';

animate('.item', {
  x: 100,
  delay: stagger(100),  // 0, 100, 200, 300...
  duration: 1000,
});
```

---

## 3️⃣ Loop (Повторение)

```javascript
// Без повторения (по умолчанию)
animate('.box', {
  x: 100,
  loop: false,     // Один раз
  duration: 1000,
});

// Бесконечное повторение
animate('.box', {
  x: 100,
  loop: true,      // Повторять бесконечно
  duration: 1000,
});

// Определенное количество повторений
animate('.box', {
  x: 100,
  loop: 3,         // Повторить 3 раза
  duration: 1000,
});

// С цикловой задержкой (время между циклами)
animate('.box', {
  x: 100,
  loop: 2,
  loopDelay: 500,  // 500ms между циклами
  duration: 1000,
});
```

---

## 4️⃣ Alternate (Туда-обратно)

```javascript
// Нормальное направление (вперед)
animate('.box', {
  x: 100,
  alternate: false,  // Не менять направление
  loop: true,
  duration: 1000,
});

// Туда-обратно (как yo-yo)
animate('.box', {
  x: 100,
  alternate: true,   // После каждого цикла: вперед → назад
  loop: true,
  duration: 1000,
  // Результат: 0 → 100 → 0 → 100 → 0...
});

// Комбинированный пример
animate('.box', {
  x: 100,
  rotate: 360,
  alternate: true,
  loop: 3,
  duration: 1000,
  // Повторяется 3 раза туда-обратно
});
```

---

## 5️⃣ Reversed (Обратное направление)

```javascript
// Нормальное направление
animate('.box', {
  x: 100,
  reversed: false,   // От 0 к 100
  duration: 1000,
});

// Обратное направление
animate('.box', {
  x: 100,
  reversed: true,    // От 100 к 0
  duration: 1000,
});

// Управление направлением через метод
const anim = animate('.box', {
  x: 100,
  duration: 1000,
  autoplay: false,
});

anim.play();     // Нормальное направление (0 → 100)
anim.reverse();  // Обратное направление (100 → 0)
```

---

## 6️⃣ Autoplay (Автоматический старт)

```javascript
// Автоматический старт (по умолчанию)
animate('.box', {
  x: 100,
  autoplay: true,   // Начинается сразу
  duration: 1000,
});

// Ручной старт
const anim = animate('.box', {
  x: 100,
  autoplay: false,  // Не запускаться автоматически
  duration: 1000,
});

// Запуск по кнопке
document.querySelector('.play-btn').addEventListener('click', () => {
  anim.play();
});

document.querySelector('.pause-btn').addEventListener('click', () => {
  anim.pause();
});

document.querySelector('.restart-btn').addEventListener('click', () => {
  anim.restart();
});
```

---

## 7️⃣ Ease Функции (Ослабление)

### Встроенные ease функции

```javascript
// Линейное движение
animate('.box', { x: 100, ease: 'linear' });

// Power функции (по умолчанию power=1.675)
animate('.box', { x: 100, ease: 'in' });        // inPower
animate('.box', { x: 100, ease: 'out' });       // outPower
animate('.box', { x: 100, ease: 'inOut' });     // inOutPower
animate('.box', { x: 100, ease: 'outIn' });     // outInPower

// С параметром
animate('.box', { x: 100, ease: 'in(2)' });    // power = 2

// Quad функции
animate('.box', { x: 100, ease: 'inQuad' });
animate('.box', { x: 100, ease: 'outQuad' });
animate('.box', { x: 100, ease: 'inOutQuad' });

// Cubic
animate('.box', { x: 100, ease: 'inCubic' });
animate('.box', { x: 100, ease: 'outCubic' });
animate('.box', { x: 100, ease: 'inOutCubic' });

// Quart, Quint, Sine, Expo, Circ
animate('.box', { x: 100, ease: 'inExpo' });
animate('.box', { x: 100, ease: 'outExpo' });

// Bounce эффект (отскок)
animate('.box', { x: 100, ease: 'outBounce' });
animate('.box', { x: 100, ease: 'inBounce' });

// Back эффект (с параметром overshoot)
animate('.box', { x: 100, ease: 'outBack' });
animate('.box', { x: 100, ease: 'outBack(1.2)' });

// Elastic эффект (пружина)
animate('.box', { x: 100, ease: 'outElastic' });
animate('.box', { x: 100, ease: 'outElastic(0.8, 1.2)' });

// Spring анимация
animate('.box', { x: 100, ease: 'spring(0.8, 1, 0.6)' });
```

### Таблица всех ease функций

| Категория | Варианты |
|----------|----------|
| **Linear** | `linear` |
| **Power** | `in`, `out`, `inOut`, `outIn` |
| **Quad** | `inQuad`, `outQuad`, `inOutQuad`, `outInQuad` |
| **Cubic** | `inCubic`, `outCubic`, `inOutCubic`, `outInCubic` |
| **Quart** | `inQuart`, `outQuart`, `inOutQuart`, `outInQuart` |
| **Quint** | `inQuint`, `outQuint`, `inOutQuint`, `outInQuint` |
| **Sine** | `inSine`, `outSine`, `inOutSine`, `outInSine` |
| **Expo** | `inExpo`, `outExpo`, `inOutExpo`, `outInExpo` |
| **Circ** | `inCirc`, `outCirc`, `inOutCirc`, `outInCirc` |
| **Bounce** | `inBounce`, `outBounce`, `inOutBounce`, `outInBounce` |
| **Back** | `inBack(overshoot)`, `outBack(overshoot)`, `inOutBack(overshoot)` |
| **Elastic** | `inElastic(amp,period)`, `outElastic(amp,period)`, `inOutElastic(amp,period)` |
| **Spring** | `spring(damping, mass, stiffness)` |

### Рекомендуемые комбинации

```javascript
// Быстрое появление
animate('.element', {
  opacity: [0, 1],
  duration: 300,
  ease: 'easeOutQuad',  // Быстрое завершение
});

// Плавное скольжение
animate('.element', {
  x: 100,
  duration: 800,
  ease: 'easeInOutCubic',  // Мягкое начало и конец
});

// Упругое возвращение
animate('.element', {
  x: 100,
  duration: 1000,
  ease: 'outElastic(0.8, 1.2)',
});

// Отскочить и остановиться
animate('.element', {
  y: 100,
  duration: 600,
  ease: 'outBounce',
});

// Весна (реалистичное движение)
animate('.element', {
  scale: 1.5,
  duration: 1000,
  ease: 'spring(0.8, 1, 0.6)',
});
```

---

## 8️⃣ Framerate и Playback Rate

```javascript
// Частота кадров (по умолчанию 60)
animate('.box', {
  x: 100,
  framerate: 30,  // Медленнее, экономит ресурсы
  duration: 1000,
});

// Скорость воспроизведения (по умолчанию 1)
const anim = animate('.box', {
  x: 100,
  duration: 1000,
  playbackRate: 1,  // Нормальная скорость
});

// Изменение скорости во время воспроизведения
anim.playbackRate = 2;    // Двойная скорость
anim.playbackRate = 0.5;  // Половинная скорость
```

---

## 9️⃣ Полный пример со всеми параметрами

```javascript
const anim = animate('.box', {
  // Анимируемые свойства
  x: 100,
  opacity: 0.5,
  rotate: 360,
  
  // Временные параметры
  duration: 2000,      // 2 секунды
  delay: 500,          // Жди 500ms
  
  // Движение
  ease: 'easeOutQuad', // Функция ослабления
  
  // Повторение
  loop: true,          // Повторять
  loopDelay: 300,      // Пауза между циклами
  alternate: true,     // Туда-обратно
  
  // Управление
  autoplay: false,     // Ручной старт
  reversed: false,     // Нормальное направление
  framerate: 60,       // 60 кадров в секунду
  
  // Callbacks
  onBegin() { console.log('Start'); },
  onComplete() { console.log('End'); },
});

// Управление скоростью
anim.playbackRate = 1.5;  // 1.5x скорость
```

---

## 📚 Ссылки на документацию

- **Timer Playback Settings**: https://animejs.com/documentation/timer/timer-playback-settings
- **Animation Playback Settings**: https://animejs.com/documentation/animation/animation-playback-settings
- **Built-in Eases**: https://animejs.com/documentation/easings/built-in-eases
- **Spring Easing**: https://animejs.com/documentation/easings/spring

---

## ✅ Контрольный список

- [ ] Понимаю разницу между duration и delay
- [ ] Знаю как использовать loop и loopDelay
- [ ] Могу использовать все типы ease функций
- [ ] Знаю рекомендуемые комбинации ease и duration
- [ ] Могу управлять скоростью через playbackRate
- [ ] Готов к 06-keyframes-stagger.md

---

**Следующий файл**: `06-keyframes-stagger.md` — Keyframes и Stagger эффекты
