# 08 — Advanced Features: Продвинутые Возможности

**Ссылка на документацию**: https://animejs.com/documentation  
**Версия**: anime.js 4.0+  
**Сложность**: Продвинутая

---

## 1️⃣ Draggable (Перетаскивание)

```javascript
import { draggable } from 'animejs';

// Базовое использование
const drag = draggable('.element', {
  x: true,      // Разрешить движение по X
  y: true,      // Разрешить движение по Y
});

// С ограничениями
const drag = draggable('.element', {
  x: { min: 0, max: 300 },
  y: { min: 0, max: 300 },
  container: '.container',  // Ограничить контейнером
});

// С привязкой к сетке
const drag = draggable('.element', {
  x: { snap: 50 },   // Привязка к сетке 50px
  y: { snap: 50 },
});

// С callbacks
const drag = draggable('.element', {
  x: true,
  y: true,
  onGrab() { console.log('Grabbed'); },
  onDrag() { console.log('Dragging'); },
  onRelease() { console.log('Released'); },
  onSnap() { console.log('Snapped'); },
  onSettle() { console.log('Settled'); },
});
```

---

## 2️⃣ Scroll Observer (Анимация при Скролле)

```javascript
import { onScroll } from 'animejs';

// Базовое использование
onScroll({
  animation: {
    targets: '.element',
    opacity: [0, 1],
    y: [50, 0],
  },
  threshold: 0.5,  // Когда 50% видно
});

// С множественными анимациями
onScroll({
  targets: [
    {
      target: '.box1',
      animation: { x: 100 },
    },
    {
      target: '.box2',
      animation: { y: 50, rotate: 90 },
    }
  ],
  threshold: 0.3,
});

// С синхронизацией
onScroll({
  animation: {
    targets: '.progress-bar',
    width: '100%',
  },
  threshold: 0,
  sync: 'playback-progress',  // Синхронизировать с прогрессом скролла
});
```

---

## 3️⃣ Scope (Инциализация в Контексте)

```javascript
import { Scope } from 'animejs';

// Создать scope для группы элементов
const scope = new Scope({
  root: document.querySelector('.container'),
  defaults: {
    duration: 600,
    ease: 'easeOutQuad',
  },
});

// Добавить анимации в scope
scope.add({
  targets: '.item',
  opacity: [0, 1],
});

// Использовать scope методы
scope.add(() => {
  console.log('Custom function in scope');
});

scope.refresh();  // Обновить
scope.revert();   // Вернуть в исходное состояние
```

---

## 4️⃣ Callbacks в Деталях

```javascript
animate('.box', {
  x: 100,
  duration: 1000,
  
  // Жизненный цикл
  onBegin(anim) {
    console.log('Beginning - первый кадр');
  },
  
  onBeforeUpdate(anim) {
    console.log('Before update - перед обновлением значений');
  },
  
  onUpdate(anim) {
    console.log('Update - значения изменены');
    console.log('Progress:', anim.progress);  // 0-1
  },
  
  onRender(anim) {
    console.log('Render - отрендерено');
  },
  
  onLoop(anim) {
    console.log('Loop - цикл завершен');
  },
  
  onPause(anim) {
    console.log('Pause - на паузе');
  },
  
  onComplete(anim) {
    console.log('Complete - завершена');
  },
});
```

---

## 5️⃣ Методы Управления

```javascript
const anim = animate('.box', {
  x: 100,
  autoplay: false,
  duration: 2000,
});

// Воспроизведение
anim.play();      // Начать/продолжить
anim.pause();     // Пауза
anim.reverse();   // Обратное направление
anim.alternate(); // Переключить направление (если loop)

// Навигация
anim.seek(500);    // Перейти к 500ms
anim.restart();    // Перезапустить
anim.reset();      // Вернуть в начало
anim.complete();   // Прыгнуть в конец

// Отмена и восстановление
anim.cancel();     // Отменить (стоп и reset)
anim.revert();     // Вернуть элемент в исходное состояние
anim.refresh();    // Обновить анимацию

// Растяжение/сжатие времени
anim.stretch(2000);  // Растянуть на 2000ms
```

---

## 6️⃣ Свойства Анимации

```javascript
const anim = animate('.box', {
  x: 100,
  y: 50,
  duration: 2000,
});

// Информация об анимации
console.log(anim.targets);       // Целевые элементы
console.log(anim.duration);      // Длительность в мс
console.log(anim.progress);      // 0-1
console.log(anim.paused);        // Boolean
console.log(anim.reversed);      // Boolean
console.log(anim.autoplay);      // Boolean
console.log(anim.loop);          // Number или boolean
console.log(anim.delay);         // Задержка
console.log(anim.playbackRate);  // Скорость
console.log(anim.animations);    // Массив анимаций
```

---

## 7️⃣ Типовые Ошибки и Решения

### Ошибка 1: Анимация не работает

```javascript
// ❌ Неправильно - нет элемента
animate('.nonexistent', { x: 100 });

// ✅ Правильно - проверьте селектор
animate('.existing', { x: 100 });

// ✅ Или используйте элемент напрямую
const el = document.querySelector('.box');
if (el) {
  animate(el, { x: 100 });
}
```

### Ошибка 2: Множественные анимации конфликтуют

```javascript
// ❌ Проблема - вторая анимация перезаписывает первую
animate('.box', { x: 100, duration: 1000 });
animate('.box', { x: 200, duration: 1000 });  // Вторая начинается, первая останавливается

// ✅ Решение - используйте Timeline
const tl = timeline();
tl.add({ targets: '.box', x: 100, duration: 1000 });
tl.add({ targets: '.box', x: 200, duration: 1000 });

// ✅ Или используйте onComplete
animate('.box', {
  x: 100,
  duration: 1000,
  onComplete() {
    animate('.box', { x: 200, duration: 1000 });
  }
});
```

### Ошибка 3: Медленная анимация

```javascript
// ❌ Проблема - анимирует положение (вызывает reflow)
animate('.box', {
  left: 100,
  top: 50,
  duration: 1000,
});

// ✅ Решение - используйте трансформации
animate('.box', {
  x: 100,
  y: 50,
  duration: 1000,
});
```

---

## 📚 Ссылки на документацию

- **Draggable**: https://animejs.com/documentation/draggable
- **Scroll Events**: https://animejs.com/documentation/events/onscroll
- **Scope**: https://animejs.com/documentation/scope
- **Callbacks**: https://animejs.com/documentation/animation/animation-callbacks
- **Methods**: https://animejs.com/documentation/animation/animation-methods

---

## ✅ Контрольный список

- [ ] Знаю как использовать Draggable
- [ ] Могу использовать Scroll Observer
- [ ] Понимаю все callbacks в деталях
- [ ] Знаю все методы управления
- [ ] Готов к 09-svg-text.md

---

**Следующий файл**: `09-svg-text.md` — SVG и текст анимации
