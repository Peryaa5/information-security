# Основные команды проекта

## 1. Создание VLAN

```cisco
enable
configure terminal

vlan 10
 name BUH

vlan 20
 name IT

vlan 30
 name HR

vlan 40
 name REST

vlan 50
 name ADMIN
```

## 2. Настройка access-портов

Access-порты используются для подключения конечных устройств к конкретному VLAN.

### VLAN10 — бухгалтерия

```cisco
interface range FastEthernet0/1-5
 switchport mode access
 switchport access vlan 10

interface FastEthernet0/6
 switchport mode access
 switchport access vlan 10
```

### VLAN20 — IT-отдел

```cisco
interface range FastEthernet0/1-5
 switchport mode access
 switchport access vlan 20
```

### VLAN30 — отдел кадров

```cisco
interface range FastEthernet0/1-5
 switchport mode access
 switchport access vlan 30

interface FastEthernet0/6
 switchport mode access
 switchport access vlan 30
```

### VLAN40 — комната отдыха

```cisco
interface range FastEthernet0/1-5
 switchport mode access
 switchport access vlan 40
```

### VLAN50 — системный администратор

```cisco
interface FastEthernet0/1
 switchport mode access
 switchport access vlan 50
```

## 3. Настройка trunk-портов

Trunk-порты нужны для передачи трафика нескольких VLAN между коммутаторами и маршрутизатором.

```cisco
interface FastEthernet0/24
 switchport mode trunk
```

На центральном коммутаторе:

```cisco
interface range FastEthernet0/1-5
 switchport mode trunk

interface GigabitEthernet0/1
 switchport mode trunk
```

## 4. Межвлановая маршрутизация Router-on-a-Stick

На Router0 создаются подинтерфейсы для каждого VLAN.

```cisco
enable
configure terminal

interface GigabitEthernet0/0
 no shutdown
```

### VLAN10

```cisco
interface GigabitEthernet0/0.10
 encapsulation dot1Q 10
 ip address 192.168.10.1 255.255.255.0
```

### VLAN20

```cisco
interface GigabitEthernet0/0.20
 encapsulation dot1Q 20
 ip address 192.168.20.1 255.255.255.0
```

### VLAN30

```cisco
interface GigabitEthernet0/0.30
 encapsulation dot1Q 30
 ip address 192.168.30.1 255.255.255.0
```

### VLAN40

```cisco
interface GigabitEthernet0/0.40
 encapsulation dot1Q 40
 ip address 192.168.40.1 255.255.255.0
```

### VLAN50

```cisco
interface GigabitEthernet0/0.50
 encapsulation dot1Q 50
 ip address 192.168.50.1 255.255.255.0
```

## 5. Подключение к внешней сети

### Router0

```cisco
interface GigabitEthernet0/1
 ip address 10.0.0.2 255.255.255.252
 no shutdown
```

Маршрут по умолчанию:

```cisco
ip route 0.0.0.0 0.0.0.0 10.0.0.1
```

### Router1

```cisco
interface GigabitEthernet0/0
 ip address 10.0.0.1 255.255.255.252
 no shutdown

interface GigabitEthernet0/1
 ip address 203.0.113.1 255.255.255.0
 no shutdown
```

## 6. Настройка NAT

NAT нужен, чтобы внутренние подсети 192.168.X.0/24 могли обращаться к внешней сети.

```cisco
access-list 1 permit 192.168.0.0 0.0.255.255

interface GigabitEthernet0/0
 ip nat inside

interface GigabitEthernet0/1
 ip nat outside

ip nat inside source list 1 interface GigabitEthernet0/1 overload
```

## 7. ACL для VLAN10 — бухгалтерия

Бухгалтерия имеет доступ только к своему VLAN и VLAN системного администратора. Доступ к другим VLAN и интернету запрещён.

```cisco
ip access-list extended VLAN10_SEC
 permit ip 192.168.10.0 0.0.0.255 192.168.50.0 0.0.0.255
 deny ip 192.168.10.0 0.0.0.255 any
 permit ip any any
exit

interface GigabitEthernet0/0.10
 ip access-group VLAN10_SEC in
```

## 8. ACL для VLAN20 — IT-отдел

IT-отдел имеет доступ к VLAN30, VLAN50 и интернету. Доступ к VLAN10 и VLAN40 запрещён.

```cisco
ip access-list extended VLAN20_SEC
 permit ip 192.168.20.0 0.0.0.255 192.168.50.0 0.0.0.255
 deny ip 192.168.20.0 0.0.0.255 192.168.10.0 0.0.0.255
 deny ip 192.168.20.0 0.0.0.255 192.168.40.0 0.0.0.255
 permit ip 192.168.20.0 0.0.0.255 192.168.30.0 0.0.0.255
 permit ip 192.168.20.0 0.0.0.255 any
exit

interface GigabitEthernet0/0.20
 ip access-group VLAN20_SEC in
```

## 9. ACL для VLAN30 — отдел кадров

Отдел кадров имеет доступ к VLAN20, VLAN50 и интернету. Доступ к VLAN10 и VLAN40 запрещён.

```cisco
ip access-list extended VLAN30_SEC
 permit ip 192.168.30.0 0.0.0.255 192.168.50.0 0.0.0.255
 deny ip 192.168.30.0 0.0.0.255 192.168.10.0 0.0.0.255
 deny ip 192.168.30.0 0.0.0.255 192.168.40.0 0.0.0.255
 permit ip 192.168.30.0 0.0.0.255 192.168.20.0 0.0.0.255
 permit ip 192.168.30.0 0.0.0.255 any
exit

interface GigabitEthernet0/0.30
 ip access-group VLAN30_SEC in
```

## 10. ACL для VLAN40 — комната отдыха

Комната отдыха имеет доступ только к VLAN50 и интернету. Доступ к VLAN10, VLAN20 и VLAN30 запрещён.

```cisco
ip access-list extended VLAN40_SEC
 permit ip 192.168.40.0 0.0.0.255 192.168.50.0 0.0.0.255
 deny ip 192.168.40.0 0.0.0.255 192.168.10.0 0.0.0.255
 deny ip 192.168.40.0 0.0.0.255 192.168.20.0 0.0.0.255
 deny ip 192.168.40.0 0.0.0.255 192.168.30.0 0.0.0.255
 permit ip 192.168.40.0 0.0.0.255 any
exit

interface GigabitEthernet0/0.40
 ip access-group VLAN40_SEC in
```

## 11. VLAN50 — системный администратор

Для VLAN50 ACL не применяется, так как системный администратор должен иметь полный доступ ко всем VLAN и внешним ресурсам.

## 12. Настройки Internet Server

```text
IP address: 203.0.113.10
Subnet mask: 255.255.255.0
Default gateway: 203.0.113.1
```

## 13. Сохранение конфигурации

```cisco
end
write memory
```
