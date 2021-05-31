##Как установить и настроить.

####Требования
- Linux
- Python3
- Chrome
- Доступ в support-console.beget по ключу

####Установка

1. Добавить в .bashrc функцию удобно вызывающую из консоли всю эту панель.
```
function domains() {
/usr/bin/google-chrome-stable 'http://localhost:8000/domain/?q='$1
}
```
2. Установить виртуальное окружение python
```
python3 -m venv venv
```
3. Активировать виртуальное окружение
```
source venv/bin/activate
```
4. Установить зависимости
```
PyCharmFP-work/fast_panel_site$ pip3 install -r requirements.txt
```
4.1 Поставить pyopenssl вручную
```
pip3 install pyopenssl
```

5. Запустить сервер.
```
PyCharmFP-work/fast_panel_site$ python3 manage.py runserver
```
6. Когда нужно прочекать домен, запусти в консоли функцию bash c доменом без
протокола
```
domains google.com
```
Вопросы ruslanakmanov@beget.ru
