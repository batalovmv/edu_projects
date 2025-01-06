# Quiz Bot

## Описание проекта

Этот проект представляет собой Telegram-бота для проведения квиза по Python. Бот позволяет пользователям отвечать на вопросы, получать баллы за правильные ответы и видеть итоговый результат после завершения квиза. Данные о пользователях, их прогрессе и баллах сохраняются в базе данных, размещенной в Yandex Cloud.

---

## Функционал бота

1. **Запуск квиза**:
   - Пользователь запускает квиз с помощью команды `/start` или кнопки **"Начать игру"**.
   - Перед началом квиза бот отправляет обложку с приветственным сообщением.

2. **Процесс квиза**:
   - Бот задает вопросы с несколькими вариантами ответов.
   - Пользователь выбирает ответ, кликая на одну из интерактивных кнопок.
   - Бот реагирует на правильные и неправильные ответы:
     - За правильный ответ начисляются баллы.
     - При неправильном ответе бот сообщает правильный вариант.

3. **Завершение квиза**:
   - После прохождения всех вопросов бот выводит итоговое количество баллов.

4. **Хранение данных**:
   - Вопросы для квиза хранятся в таблице базы данных `quiz_questions`.
   - Прогресс пользователя (индекс текущего вопроса и количество баллов) сохраняется в таблице `quiz_state`.

---

## Структура базы данных

### 1. **Таблица `quiz_questions`**  
Хранит вопросы и ответы для квиза.

| Поле            | Тип      | Описание                                   |
|------------------|----------|-------------------------------------------|
| `question_id`    | Uint64   | Уникальный идентификатор вопроса.         |
| `question`       | String   | Текст вопроса.                            |
| `options`        | String   | Варианты ответа, разделенные `;`.         |
| `correct_option` | Uint64   | Индекс правильного ответа (начинается с 0).|

---

### 2. **Таблица `quiz_state`**  
Хранит прогресс пользователей.

| Поле             | Тип      | Описание                                  |
|-------------------|----------|------------------------------------------|
| `user_id`         | Uint64   | Уникальный идентификатор пользователя.   |
| `question_index`  | Uint64   | Индекс текущего вопроса.                 |
| `total_points`    | Uint64   | Количество набранных пользователем очков.|

---

## Как работает бот?

### 1. **Yandex Cloud Object Storage**
Обложка квиза размещена в **Yandex Cloud Object Storage**. Ссылка на изображение:
```
https://storage.yandexcloud.net/batalovmv-quiz-images/_.png
```
Картинка отправляется пользователю при запуске квиза.

### 2. **Yandex Database (YDB)**
- Вопросы и ответы для квиза хранятся в таблице `quiz_questions`.
- Прогресс и баллы пользователей сохраняются в таблице `quiz_state`.

### 3. **Telegram API**
Бот использует библиотеку `aiogram` для взаимодействия с Telegram API. Она обеспечивает:
- Обработку команд (`/start`) и текстовых сообщений.
- Отправку сообщений, фотографий и интерактивных кнопок пользователям.


---

## Основные файлы и их назначение

### 1. **`database.py`**
Содержит функции для взаимодействия с базой данных:
- Подключение к Yandex Database.
- Выполнение SQL-запросов (выборка и обновление данных).
- Загрузка вопросов из таблицы `quiz_questions` в память при запуске.

### 2. **`service.py`**
Содержит основные функции квиза:
- **`new_quiz`**: Обнуляет прогресс и начинает новый квиз.
- **`get_question`**: Отправляет текущий вопрос пользователю.
- **`generate_options_keyboard`**: Генерирует кнопки с вариантами ответов.
- **`get_quiz_index`, `get_total_points`, `update_quiz_index`**: Работают с прогрессом пользователя в базе данных.

### 3. **`handlers.py`**
Обрабатывает команды и действия пользователя:
- **`/start`**: Показывает приветственное сообщение и кнопку для начала игры.
- **"Начать игру"**: Показывает обложку квиза и начинает игру.
- **`right_answer` и `wrong_answer`**: Реагируют на выбор ответа, обновляют прогресс и баллы.

---

## Пример использования

1. Пользователь запускает бота с помощью команды `/start`.
2. Бот отправляет обложку квиза и предлагает начать игру.
3. Пользователь нажимает кнопку **"Начать игру"**.
4. Бот задает вопросы, пользователь отвечает.
5. В конце квиза бот отправляет итоговый результат с количеством набранных очков.

---

## Как начать работу с ботом?

1. **Найдите бота в Telegram**:
   - Откройте Telegram.
   - В строке поиска введите **`batalovmv_yandex_bot`**.
   - Нажмите на найденного бота и откройте чат с ним.

2. **Запустите бота**:
   - Отправьте команду `/start` или нажмите на кнопку **"Start"** в чате с ботом.
   - Бот отправит вам приветственное сообщение и предложит начать квиз.

3. **Начать квиз**:
   - Нажмите кнопку **"Начать игру"**.
   - Бот отправит обложку квиза и начнет задавать вопросы.

4. **Отвечайте на вопросы**:
   - Для каждого вопроса будет предложено несколько вариантов ответа в виде кнопок.
   - Нажмите на выбранный вариант ответа.

5. **Завершение квиза**:
   - После прохождения всех вопросов бот отправит сообщение с вашим итоговым результатом (количество набранных очков).

---

## Основные команды

- **`/start`** — Запуск бота и приветственное сообщение.
- **"Начать игру"** — Начало нового квиза.

---

## Пример общения с ботом

1. **Запуск команды `/start`**:
   ```
   Добро пожаловать в квиз по Python! 🐍
   Нажмите "Начать игру", чтобы приступить к вопросам!
   ```

   (Отправляется кнопка **"Начать игру"**)

2. **Начало игры после нажатия кнопки**:
   Бот отправляет обложку квиза и первый вопрос:
   ```
   Вопрос: Какой из этих типов данных является неизменяемым в Python?
   [Список кнопок: "list", "tuple", "set", "dict"]
   ```

3. **Правильный ответ**:
   ```
   Верно!
   ```

4. **Неправильный ответ**:
   ```
   Неправильно. Правильный ответ: tuple
   ```

5. **Завершение квиза**:
   ```
   Это был последний вопрос. Квиз завершен! Ваш результат: 4 очка.
   ```

---

## Требования для работы с ботом

- Установленный Telegram на вашем устройстве.
- Бот доступен по ссылке: [batalovmv_yandex_bot](https://t.me/batalovmv_yandex_bot).

---

Если у вас возникнут вопросы или проблемы с использованием бота, напишите разработчику! 😊
