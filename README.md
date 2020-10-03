# API_URL
<h2>Инструкция:</h2>

1) <h3>Запуск:</h3> 
  <p>Клонируем на свой ПК репозиторий https://github.com/PTaras/API_URL.git <p>
  Запускаем проект => файл <i>app.py</i>
  
2) <h3>Краткое описание функционала API</h3>
API http://127.0.0.1:5000/urls/ позволяет получать, добавлять, обновлять или удалять ссылки.
Данный сервис может принимать на входе любую ссылку и превращать её в короткую с помощью другой API для сокращения ссылок https://app.bitly.com/.
Так же, при добавлении новой ссылки, API записывает ей дату добавления, что позволяет хранить url то время, которое мы указали (<i>livetime</i>). По умолчанию время жизни указывается 90 дней, 
максимальное - 365 дней.
API позволяет добавлять только уникальные ссылки.
  
3) <h3>Тестирование API</h3>
  <p>Протестировать api можно локально при помощи консольной утилиты <i>curl</i> или клиента <i>Insomnia REST</i>.</p>
  <ul>
  <li>Проверка <b>GET-запроса</b>: http://127.0.0.1:5000/urls/</li>
  В ответ получаем json со всеми имеющимся ссылками и их дополнительными параметрами. 
  <img src=https://github.com/PTaras/API_URL/blob/master/assets/img/get-api.png alt="get-api"/>
  <li>Проверка <b>POST-запроса</b> (добавление новой ссылки): http://127.0.0.1:5000/urls/</li>
    Принимает в теле запроса <i>json</i> с обязательным параметром - <i>url</i> и  не обязательным - <i>livetime</i>. Если время жизни ссылки не указано в теле запроса, то при сохранении новой ссылки оно будет проставлено по умолчанию как 90.
  <img src=https://github.com/PTaras/API_URL/blob/master/assets/img/post-api.png alt="post-api"/>
  Если, при попытке отправки POST-запроса, такой url уже существует, то api вернёт соответствующее сообщениие:
  <img src=https://github.com/PTaras/API_URL/blob/master/assets/img/post-api-exists.png alt="post-api-exists"/>
  <li>Проверка <b>PUT-запроса</b> (обновление (апдейт) параметров ссылки): http://127.0.0.1:5000/urls/{id}</li>
    Принимает в теле запроса <i>json</i> с параметрами, которые необходимо обновить (<i>url</i> или <i>livetime</i>). 
    В api необходимо указать <i>id</i> url-а, который необходимо обновить.
  <img src=https://github.com/PTaras/API_URL/blob/master/assets/img/put-api.png alt="put-api"/>
  Результат успешного обновления livetime:
<img src=https://github.com/PTaras/API_URL/blob/master/assets/img/put-api-update.png alt="put-api"/>
  <li>Проверка <b>DELETE-запроса</b> (удаление ссылки): http://127.0.0.1:5000/urls/{id}</li>
  В api указывать <i>id</i> url, который необходимо удалить. 
  <img src=https://github.com/PTaras/API_URL/blob/master/assets/img/delete-api.png alt="delete-api"/>
  </ul>
