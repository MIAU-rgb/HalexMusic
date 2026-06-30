@echo off
chcp 65001 >nul
title Курс Python - Викторина

:START
cls
echo.
echo  ╔══════════════════════════════════════════╗
echo  ║     🐍  КУРС PYTHON - ВИКТОРИНА  🐍     ║
echo  ╚══════════════════════════════════════════╝
echo.
echo  Выбери сложность:
echo.
echo    [Y] - ЛЕГКО (для новичков)
echo    [N] - СЛОЖНО (для профи)
echo    [Q] - Выход
echo.
set /p diff="Твой выбор (Y/N/Q): "

if /i "%diff%"=="Q" goto EXIT
if /i "%diff%"=="Y" goto EASY
if /i "%diff%"=="N" goto HARD
echo Неверный ввод! Жми Enter...
pause >nul
goto START

:EASY
set score=0
set total=10
cls
echo.
echo  ╔══════════════════════════════════════════╗
echo  ║         🟢  ЛЕГКИЙ УРОВЕНЬ  🟢         ║
echo  ╚══════════════════════════════════════════╝
echo.

echo  📝 Вопрос 1/10:
echo  Что выведет print("Привет")?
echo.
echo    A) Привет
echo    B) "Привет"
echo    C) Ошибка
echo.
set /p ans="Твой ответ (A/B/C): "
if /i "%ans%"=="A" (
    echo ✅ Верно!
    set /a score+=1
) else (
    echo ❌ Неверно. Правильный ответ: A
)
echo  Нажми Enter...
pause >nul
cls

echo.
echo  📝 Вопрос 2/10:
echo  Какой оператор используется для присваивания?
echo.
echo    A) ==
echo    B) =
echo    C) :=
echo.
set /p ans="Твой ответ (A/B/C): "
if /i "%ans%"=="B" (
    echo ✅ Верно!
    set /a score+=1
) else (
    echo ❌ Неверно. Правильный ответ: B
)
echo  Нажми Enter...
pause >nul
cls

echo.
echo  📝 Вопрос 3/10:
echo  Что такое переменная?
echo.
echo    A) Число
echo    B) Ячейка для хранения данных
echo    C) Функция
echo.
set /p ans="Твой ответ (A/B/C): "
if /i "%ans%"=="B" (
    echo ✅ Верно!
    set /a score+=1
) else (
    echo ❌ Неверно. Правильный ответ: B
)
echo  Нажми Enter...
pause >nul
cls

echo.
echo  📝 Вопрос 4/10:
echo  Что делает type(5)?
echo.
echo    A) Печатает 5
echo    B) Узнаёт тип данных
echo    C) Создаёт файл
echo.
set /p ans="Твой ответ (A/B/C): "
if /i "%ans%"=="B" (
    echo ✅ Верно!
    set /a score+=1
) else (
    echo ❌ Неверно. Правильный ответ: B
)
echo  Нажми Enter...
pause >nul
cls

echo.
echo  📝 Вопрос 5/10:
echo  Как закомментировать строку в Python?
echo.
echo    A) //
echo    B) --
echo    C) #
echo.
set /p ans="Твой ответ (A/B/C): "
if /i "%ans%"=="C" (
    echo ✅ Верно!
    set /a score+=1
) else (
    echo ❌ Неверно. Правильный ответ: C
)
echo  Нажми Enter...
pause >nul
cls

echo.
echo  📝 Вопрос 6/10:
echo  Что будет в переменной name после: name = "Alex"
echo.
echo    A) Строка "Alex"
echo    B) Число 0
echo    C) Ничего
echo.
set /p ans="Твой ответ (A/B/C): "
if /i "%ans%"=="A" (
    echo ✅ Верно!
    set /a score+=1
) else (
    echo ❌ Неверно. Правильный ответ: A
)
echo  Нажми Enter...
pause >nul
cls

echo.
echo  📝 Вопрос 7/10:
echo  Что такое int?
echo.
echo    A) Строка
echo    B) Дробное число
echo    C) Целое число
echo.
set /p ans="Твой ответ (A/B/C): "
if /i "%ans%"=="C" (
    echo ✅ Верно!
    set /a score+=1
) else (
    echo ❌ Неверно. Правильный ответ: C
)
echo  Нажми Enter...
pause >nul
cls

echo.
echo  📝 Вопрос 8/10:
echo  Что делает input()?
echo.
echo    A) Ждёт ввода от пользователя
echo    B) Выводит текст
echo    C) Завершает программу
echo.
set /p ans="Твой ответ (A/B/C): "
if /i "%ans%"=="A" (
    echo ✅ Верно!
    set /a score+=1
) else (
    echo ❌ Неверно. Правильный ответ: A
)
echo  Нажми Enter...
pause >nul
cls

echo.
echo  📝 Вопрос 9/10:
echo  Как запустить Python-файл из командной строки?
echo.
echo    A) start file.py
echo    B) python file.py
echo    C) run file.py
echo.
set /p ans="Твой ответ (A/B/C): "
if /i "%ans%"=="B" (
    echo ✅ Верно!
    set /a score+=1
) else (
    echo ❌ Неверно. Правильный ответ: B
)
echo  Нажми Enter...
pause >nul
cls

echo.
echo  📝 Вопрос 10/10:
echo  Что такое список в Python?
echo.
echo    A) list = []
echo    B) list = ()
echo    C) list = {}
echo.
set /p ans="Твой ответ (A/B/C): "
if /i "%ans%"=="A" (
    echo ✅ Верно!
    set /a score+=1
) else (
    echo ❌ Неверно. Правильный ответ: A
)
echo  Нажми Enter...
pause >nul
cls

goto RESULT

:HARD
set score=0
set total=10
cls
echo.
echo  ╔══════════════════════════════════════════╗
echo  ║         🔴  СЛОЖНЫЙ УРОВЕНЬ  🔴        ║
echo  ╚══════════════════════════════════════════╝
echo.

echo  📝 Вопрос 1/10:
echo  Что выведет: print(type([1,2,3]))
echo.
echo    A) list
echo    B) tuple
echo    C) dict
echo.
set /p ans="Твой ответ (A/B/C): "
if /i "%ans%"=="A" (
    echo ✅ Верно!
    set /a score+=1
) else (
    echo ❌ Неверно. Правильный ответ: A - list
)
echo  Нажми Enter...
pause >nul
cls

echo.
echo  📝 Вопрос 2/10:
echo  Что такое lambda в Python?
echo.
echo    A) Анонимная функция
echo    B) Цикл
echo    C) Класс
echo.
set /p ans="Твой ответ (A/B/C): "
if /i "%ans%"=="A" (
    echo ✅ Верно!
    set /a score+=1
) else (
    echo ❌ Неверно. Правильный ответ: A
)
echo  Нажми Enter...
pause >nul
cls

echo.
echo  📝 Вопрос 3/10:
echo  Что выведет: print(2**3)
echo.
echo    A) 6
echo    B) 8
echo    C) 23
echo.
set /p ans="Твой ответ (A/B/C): "
if /i "%ans%"=="B" (
    echo ✅ Верно!
    set /a score+=1
) else (
    echo ❌ Неверно. Правильный ответ: B - 8 (2 в степени 3)
)
echo  Нажми Enter...
pause >nul
cls

echo.
echo  📝 Вопрос 4/10:
echo  Как отсортировать список my_list по возрастанию?
echo.
echo    A) my_list.sort()
echo    B) sort(my_list)
echo    C) my_list.order()
echo.
set /p ans="Твой ответ (A/B/C): "
if /i "%ans%"=="A" (
    echo ✅ Верно!
    set /a score+=1
) else (
    echo ❌ Неверно. Правильный ответ: A
)
echo  Нажми Enter...
pause >nul
cls

echo.
echo  📝 Вопрос 5/10:
echo  Что такое декоратор в Python?
echo.
echo    A) Функция, изменяющая другую функцию
echo    B) Шаблон оформления кода
echo    C) Класс для рисования
echo.
set /p ans="Твой ответ (A/B/C): "
if /i "%ans%"=="A" (
    echo ✅ Верно!
    set /a score+=1
) else (
    echo ❌ Неверно. Правильный ответ: A
)
echo  Нажми Enter...
pause >nul
cls

echo.
echo  📝 Вопрос 6/10:
echo  Что выведет: print(10 // 3)
echo.
echo    A) 3.33
echo    B) 3
echo    C) 1
echo.
set /p ans="Твой ответ (A/B/C): "
if /i "%ans%"=="B" (
    echo ✅ Верно!
    set /a score+=1
) else (
    echo ❌ Неверно. Правильный ответ: B - целочисленное деление
)
echo  Нажми Enter...
pause >nul
cls

echo.
echo  📝 Вопрос 7/10:
echo  Что делает enumerate()?
echo.
echo    A) Нумерует элементы с индексами
echo    B) Считает элементы
echo    C) Переворачивает список
echo.
set /p ans="Твой ответ (A/B/C): "
if /i "%ans%"=="A" (
    echo ✅ Верно!
    set /a score+=1
) else (
    echo ❌ Неверно. Правильный ответ: A
)
echo  Нажми Enter...
pause >nul
cls

echo.
echo  📝 Вопрос 8/10:
echo  Что такое *args и **kwargs?
echo.
echo    A) Переменное число аргументов
echo    B) Комментарии
echo    C) Типы данных
echo.
set /p ans="Твой ответ (A/B/C): "
if /i "%ans%"=="A" (
    echo ✅ Верно!
    set /a score+=1
) else (
    echo ❌ Неверно. Правильный ответ: A
)
echo  Нажми Enter...
pause >nul
cls

echo.
echo  📝 Вопрос 9/10:
echo  Что такое self в методах класса?
echo.
echo    A) Ссылка на экземпляр класса
echo    B) Ключевое слово
echo    C) Модуль
echo.
set /p ans="Твой ответ (A/B/C): "
if /i "%ans%"=="A" (
    echo ✅ Верно!
    set /a score+=1
) else (
    echo ❌ Неверно. Правильный ответ: A
)
echo  Нажми Enter...
pause >nul
cls

echo.
echo  📝 Вопрос 10/10:
echo  Что выведет: print([x for x in range(5) if x%2==0])
echo.
echo    A) [0, 2, 4]
echo    B) [1, 3, 5]
echo    C) [0, 1, 2, 3, 4]
echo.
set /p ans="Твой ответ (A/B/C): "
if /i "%ans%"=="A" (
    echo ✅ Верно!
    set /a score+=1
) else (
    echo ❌ Неверно. Правильный ответ: A - [0, 2, 4]
)
echo  Нажми Enter...
pause >nul
cls

goto RESULT

:RESULT
cls
echo.
echo  ╔══════════════════════════════════════════╗
echo  ║            🏆  РЕЗУЛЬТАТ  🏆           ║
echo  ╚══════════════════════════════════════════╝
echo.
set /a percent=score*100/total
echo  Правильных ответов: %score% из %total%
echo  Процент: %percent%%%
echo.

if %score% GEQ 9 (
    echo  🌟 ОТЛИЧНО! Ты настоящий Python-мастер!
)
if %score% GEQ 7 if %score% LSS 9 (
    echo  👍 ХОРОШО! Ещё чуть-чуть подучить!
)
if %score% GEQ 5 if %score% LSS 7 (
    echo  📚 НЕПЛОХО! Но есть куда расти!
)
if %score% LSS 5 (
    echo  🐣 НИЧЕГО! Ты только учишься, продолжай!
)

echo.
echo  ═══════════════════════════════════════════
echo.
echo  [R] - Пройти заново
echo  [Q] - Выход
echo.
set /p again="Твой выбор: "
if /i "%again%"=="R" goto START
if /i "%again%"=="Q" goto EXIT
goto EXIT

:EXIT
cls
echo.
echo  Спасибо за прохождение викторины!
echo  Подписывайся на канал: [твой канал]
echo  Увидимся в следующей серии! 🐍
echo.
timeout /t 3 >nul
exit
