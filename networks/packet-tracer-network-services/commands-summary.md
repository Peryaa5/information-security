# Основные настройки и команды проекта

## 1. Назначение устройств

| Устройство | Роль |
|-----------|------|
| Server1 | DNS, Web и FTP-сервер |
| Server2 | DHCP-сервер |
| PC1 | клиент, получает параметры TCP/IP через DHCP |

## 2. IP-настройки серверов

### Server1

```text
IP address: 10.0.0.1
Subnet mask: 255.0.0.0
```

### Server2

```text
IP address: 10.0.0.2
Subnet mask: 255.0.0.0
```

## 3. Настройка PC1

На PC1 в настройках FastEthernet0 выбран режим получения IP-адреса через DHCP:

```text
IP Configuration: DHCP
```

## 4. DNS на Server1

На Server1 включена служба DNS.

Пример DNS-записей:

```text
Type: A
Name: server1.rambler.ru
Address: 10.0.0.1
```

```text
Type: CNAME
Name: www.rambler.ru
Host Name: server1.rambler.ru
```

В проекте доменное имя используется для открытия сайта на Server1.

## 5. HTTP на Server1

На Server1 включена служба HTTP.

Пример содержимого стартовой страницы:

```html
<html>
<center><font size='+2' color='blue'>Cisco Packet Tracer</font></center>
<p>WWW.RAMBLER.RU</p>
<p>Server1</p>
</html>
```

## 6. Проверка DNS

На Server1 или PC1 можно проверить работу DNS через команду:

```text
nslookup www.rambler.ru
```

Ожидаемый результат:

```text
Server: 10.0.0.1
Address: 10.0.0.1

Name: server1.rambler.ru
Address: 10.0.0.1
Aliases: www.rambler.ru
```

## 7. FTP на Server1

На Server1 включена служба FTP.

Созданы пользователи:

```text
Username: user1
Password: password1
Permissions: read / write
```

```text
Username: admin
Password: admin123
Permissions: full access
```

## 8. Основные FTP-команды

```text
dir
```

Просмотр содержимого директории.

```text
get имя_файла
```

Скачать файл с FTP-сервера.

```text
put имя_файла
```

Загрузить файл на FTP-сервер.

```text
bye
```

Завершить FTP-сеанс.

## 9. DHCP на Server2

На Server2 включена DHCP-служба.

Пример настроек DHCP-пула:

```text
Pool Name: serverPool
Default Gateway: 0.0.0.0
DNS Server: 10.0.0.1
Start IP Address: 10.0.0.10
Subnet Mask: 255.0.0.0
Maximum Number of Users: 5
TFTP Server: 0.0.0.0
```

## 10. Проверка получения адреса на PC1

Сброс старых параметров IP:

```text
ipconfig /release
```

Получение новых параметров от DHCP-сервера:

```text
ipconfig /renew
```

Ожидаемый результат:

```text
IP Address: 10.0.0.10
Subnet Mask: 255.0.0.0
Default Gateway: 0.0.0.0
DNS Server: 10.0.0.1
```

## 11. Проверка Web-сервера

На PC1 в браузере открыть доменное имя:

```text
http://www.rambler.ru
```

После этого должна открыться стартовая страница сайта, размещённая на Server1.

## 12. Проверка FTP-сервера

Подключение к FTP-серверу:

```text
ftp 10.0.0.1
```

Ввод учётных данных:

```text
Username: admin
Password: admin123
```

Просмотр файлов:

```text
dir
```

Скачивание файлов:

```text
get download.txt
get upload.txt
```

Проверка файлов на PC1:

```text
dir
```

