## WhatWeatherIsItBot
Telegram бот для тестового задания в Школу Будущих СТО Яндекс.Облака.

К сожалению я сделал опечатку в названии при создании телеграм бота, и в телеграме он называется WhatWheatherIsIt :( 

### Описание задачи:
#### О сервисе:
  Сервис призван помогать пользователю быстро определить погоду в своем населенном пункте и советовать, а что необходимо надеть сегодня на улицу, чтобы чувствовать себя комфортно.

Выбранный уровень сложности - средний.

#### Технические моменты реализации:
  Для обертки я использовал телеграм бота, с которым работал с помощью библиотеки telebot. Для получения сведений о погоде использовал API OpenWeatherMap. Бот реализован на языке python.

#### Как работает мой телеграм бот:
  * Вначале работы требуется выполнить команду /start или /help.
  * Далее требутеся нажать на кнопку о том, какую погоду требуется узнать, в моем случае это "Узнать текущую погоду", но также есть возможность добавить и кнопку с прогнозом погоды на нужное время (если получить доступ OpenWeatherMap).
  * Далее появятся три кнопки: "Ввести новый город", "Последний просмотренный город", "Назад".
    1. Если пользователь вводит "Ввести новый город", то дальше его просят ввести название города на русском с заглавной буквы.
    2. Если пользователь вводит "Последний просмотренный город", то в качестве города используется последний город, который пользователь вводил до этого, все предудыщие города хранятся в виде словоря с id чата в качестве ключа (для серьёзного эксплуатирования требуется использовать какую-либо key-value базу данных), в случае если такого нет, используется "Москва".
    3. Если пользователь вводит "Назад", то пользователь попадает в меню с кнопкой "Узнать текущую погоду".
  * После этого программа узнала город пользователя, и формирует запрос для openweathermap.
  * Далее полученный от oopenweathermap ответ в случае успешного получения данных преобразуется, и отправляется в виде сообщения пользователю.
  * Формат вывода данных о погоде:
  
    Погода в cityname на данный момент 
    
    Температура  __ по Цельсию 
    
    Ощущуается как __
    
    Краткое описание: __
    
    Давление __мм ртутного столба 
    
    Влажность __% 
    
    Скорость ветра __м/с
    
  * Обработка ошибок:
    1. Если пользователь вводит текст, не являющийся командой, или названием кнопки, то ему пишется сообщение об ошибке.
    2. Если пользователь вводил неверное имя города, то запрос всё равно отправляется, после чего получается ответ от сервера о некорректности имения города, и пользователю выводится сообщение об ошибке.
    
##### Для запуска программы требуется:
  * создать файл config.py, в котором записать token для телеграм бота и для openweathermap.
  * установить библиотеку telebot
  * иметь python3
  * включить подключение tor, или запускать не из России любым другим способом
  * запустить бота python3 WhatWeatherIsItBot
  
##### Что можно добавить для расширения функциональности:
  * можно добавить возможность получить сведения о погоде на будушее (на 3/6/24 часа вперед, если это позолит API для прогноза погоды)
  * можно добавить получение координта пользователя, по которым формировать запрос для API сервера прогноза погоды.
  * можно добавить расширенный прогноз погоды, время восхода/захода солнца и т.п. (не сделал этого чтобы пока не перегружать выдачу)
  * можно добавить возможность на карте отметить кординаты пользователя, которые полсе можно отправить на API сервиса.