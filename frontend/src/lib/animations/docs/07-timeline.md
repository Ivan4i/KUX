# 07 — Timeline: Композиция Сложных Анимаций

**Ссылка на документацию**: https://animejs.com/documentation/timeline  
**Версия**: anime.js 4.0+  
**Сложность**: Продвинутая

---

## 1️⃣ Создание Timeline

```javascript
import { timeline } from 'animejs';

// Создание пустой временной шкалы
const tl = timeline();

// С параметрами
const tl = timeline({
  autoplay: true,    // Запуск при создании
  duration: 5000,    // Общая длительность
  ease: 'easeInOutQuad',  // Ease по умолчанию
  loop: false,       // Не повторять
});
```

---

## 2️⃣ Добавление Анимаций

### Метод add()

```javascript
const tl = timeline();

// Добавить анимацию в конец временной шкалы
tl.add({
  targets: '.box1',
  x: 100,
  duration: 1000,
});

// Вторая анимация начнется после первой
tl.add({
  targets: '.box2',
  x: 100,
  duration: 1000,
});

// Добавить с временной позицией (одновременно с предыдущей)
tl.add({
  targets: '.box3',
  x: 100,
  duration: 1000,
}, 0);  // 0 = начало timeline

// Относительная позиция (на 200ms раньше конца)
tl.add({
  targets: '.box4',
  x: 100,
  duration: 1000,
}, '-=200');

// На 300ms позже начала предыдущей
tl.add({
  targets: '.box5',
  x: 100,
  duration: 1000,
}, '+=300');
```

### Временные Позиции

```javascript
const tl = timeline();

tl.add({ targets: '.a', x: 100 }, 0);      // Абсолютная позиция 0
tl.add({ targets: '.b', x: 100 }, 500);    // Абсолютная позиция 500ms
tl.add({ targets: '.c', x: 100 });         // В конец (по умолчанию)
tl.add({ targets: '.d', x: 100 }, '+=100'); // +100ms от конца
tl.add({ targets: '.e', x: 100 }, '-=200'); // Начать за 200ms до конца
```

---

## 3️⃣ Методы Timeline

### Управление Воспроизведением

```javascript
const tl = timeline({ autoplay: false });

tl.add({ targets: '.box', x: 100, duration: 1000 });

// Управление
tl.play();     // Начать/продолжить
tl.pause();    // Пауза
tl.reverse();  // Обратное направление
tl.restart();  // Перезапустить
tl.reset();    // Вернуть в начало
tl.seek(500);  // Перейти к 500ms
tl.complete(); // Прыгнуть в конец
```

### Добавление Функций

```javascript
const tl = timeline();

// Вызвать функцию в определенный момент
tl.call(() => {
  console.log('Milestone!');
}, 1000);  // На 1000ms

// Или в конце анимации
tl.add({ targets: '.box', x: 100, duration: 1000 });
tl.call(() => {
  console.log('After first animation');
});
```

### Метки (Labels)

```javascript
const tl = timeline();

// Добавить метку
tl.label('start');

tl.add({ targets: '.box1', x: 100, duration: 1000 });

tl.label('middle');  // Метка в текущей позиции

tl.add({ targets: '.box2', x: 100, duration: 1000 });

tl.label('end');

// Использовать метки для позиций
tl.add({ targets: '.box3', x: 100 }, 'middle');
tl.add({ targets: '.box4', x: 100 }, 'end');
```

---

## 4️⃣ Параметры Timeline

```javascript
const tl = timeline({
  // Параметры воспроизведения
  autoplay: false,
  duration: 5000,
  ease: 'easeInOutQuad',
  loop: 2,
  loopDelay: 300,
  alternate: true,
  reversed: false,
  
  // Callbacks
  onBegin() { console.log('Timeline started'); },
  onComplete() { console.log('Timeline completed'); },
  onLoop() { console.log('Loop'); },
  onUpdate() { console.log(tl.progress); },
});
```

---

## 5️⃣ Практические Примеры

### Пример 1: Последовательная анимация

```javascript
const tl = timeline();

tl.add({ targets: '.step1', opacity: [0, 1], duration: 600 });
tl.add({ targets: '.step2', opacity: [0, 1], duration: 600 });
tl.add({ targets: '.step3', opacity: [0, 1], duration: 600 });

tl.play();
```

### Пример 2: Параллельные анимации

```javascript
const tl = timeline();

// Все начинаются одновременно
tl.add({ targets: '.box1', x: 100, duration: 1000 }, 0);
tl.add({ targets: '.box2', x: 100, duration: 1000 }, 0);
tl.add({ targets: '.box3', x: 100, duration: 1000 }, 0);

// Потом все вместе
tl.add({ targets: '.box1', y: 100, duration: 500 });
tl.add({ targets: '.box2', y: 100, duration: 500 }, '-=500');
tl.add({ targets: '.box3', y: 100, duration: 500 }, '-=500');
```

### Пример 3: Сложная сцена

```javascript
const tl = timeline({ loop: true, duration: 8000 });

// Сцена 1: Появление
tl.add({ targets: '.character', opacity: [0, 1], y: [50, 0], duration: 500 }, 0);

// Сцена 2: Ходьба
tl.add({ targets: '.character', x: 200, duration: 2000, ease: 'linear' }, 500);

// Сцена 3: Прыжок (параллельно с ходьбой)
tl.add({ targets: '.character', y: [0, -100, 0], duration: 800, ease: 'easeInOutQuad' }, 1200);

// Сцена 4: Исчезновение
tl.add({ targets: '.character', opacity: [1, 0], duration: 500 }, 6500);
```

---

## 6️⃣ Управление Скоростью

```javascript
const tl = timeline();

tl.add({ targets: '.box', x: 100, duration: 1000 });

// Изменить скорость воспроизведения
tl.playbackRate = 2;    // Двойная скорость
tl.playbackRate = 0.5;  // Половинная скорость
tl.playbackRate = 1;    // Нормальная скорость

// С ease (сглаженное изменение скорости)
tl.playbackEase = 'easeInOutQuad';
```

---

## 📚 Ссылки на документацию

- **Timeline**: https://animejs.com/documentation/timeline
- **Add Animations**: https://animejs.com/documentation/timeline/add-animations
- **Timeline Methods**: https://animejs.com/documentation/timeline/timeline-methods

---

## ✅ Контрольный список

- [ ] Знаю как создавать Timeline
- [ ] Могу добавлять анимации с разными временными позициями
- [ ] Понимаю различие между абсолютными и относительными позициями
- [ ] Могу использовать метки (labels)
- [ ] Готов к 08-advanced-features.md

---

**Следующий файл**: `08-advanced-features.md` — Продвинутые возможности
