
<!-- nav -->
# Table of Contents

1. [Установка Arch Linux](#установка-arch-linux)
   1. [Arch Linux](#arch-linux)
   1. [Создание образа](#создание-образа)
   1. [Изменяем приоритет загрузки в BIOS/UEFI](#изменяем-приоритет-загрузки-в-biosuefi)
   1. [Настройка сети](#настройка-сети)
   1. [Размечаем диск](#размечаем-диск)
   1. [Устанавливаем ядро](#устанавливаем-ядро)
   1. [Генерируем fstab](#генерируем-fstab)
   1. [arch-chroot](#arch-chroot)
   1. [Настраиваем дату и локаль](#настраиваем-дату-и-локаль)
   1. [Прописываем хосты](#прописываем-хосты)
   1. [Initramfs](#initramfs)
   1. [Ставим пакеты](#ставим-пакеты)
   1. [Пользователи](#пользователи)
   1. [Установка grub](#установка-grub)
   1. [Завершение установки](#завершение-установки)
1. [Пакетные менеджеры](#пакетные-менеджеры)
1. [Нужные пакеты](#нужные-пакеты)
1. [Заменяем ядро на стабильное](#заменяем-ядро-на-стабильное)
1. [Права](#права)
1. [Добавляем путь в PATH](#добавляем-путь-в-path)
1. [bin в домашнем каталоге](#bin-в-домашнем-каталоге)
1. [Масштабировавние 150% как в Windows](#масштабировавние-150-как-в-windows)
1. [Расширения для Gnome](#расширения-для-gnome)
1. [Пользовательские сочетания клавиш](#пользовательские-сочетания-клавиш)
1. [Шрифты](#шрифты)
1. [Запуск исполняемых файлов по двойному клику в Nautilus](#запуск-исполняемых-файлов-по-двойному-клику-в-nautilus)
1. [Шаблоны файлов](#шаблоны-файлов)
1. [ZSH](#zsh)
   1. [Установка ZSH](#установка-zsh)
   1. [Oh My Zsh](#oh-my-zsh)
   1. [Темы Oh My Zsh!](#темы-oh-my-zsh)
      1. [Jovial](#jovial)
      1. [Powerlevel10k](#powerlevel10k)
   1. [Подробнее про ZSH](#подробнее-про-zsh)
1. [Разноцветный cat](#разноцветный-cat)
1. [Цветовые схемы для терминала](#цветовые-схемы-для-терминала)
1. [Блокируем сайты с рекламой через hosts](#блокируем-сайты-с-рекламой-через-hosts)
1. [asdf-vm](#asdf-vm)
1. [NVM](#nvm)
1. [Настройка Docker](#настройка-docker)
1. [Настройка Visual Code](#настройка-visual-code)
1. [Гибернация](#гибернация)
1. [RAID](#raid)
1. [LVM](#lvm)
   1. [Изменение размера логического раздела](#изменение-размера-логического-раздела)
   1. [Переименование логических разделов](#переименование-логических-разделов)
1. [Установка и настройка Postgres](#установка-и-настройка-postgres)
1. [Работаем с github через ssh](#работаем-с-github-через-ssh)
1. [Tor Service](#tor-service)
1. [Emoji](#emoji)
1. [Блокировка рекламных сайтов](#блокировка-рекламных-сайтов)
1. [Редактирование DConf](#редактирование-dconf)
1. [i3](#i3)
   1. [Описание](#описание)
   1. [Установка и настройка i3](#установка-и-настройка-i3)
   1. [XTerm](#xterm)
   1. [Termite: горячие клавиши](#termite-горячие-клавиши)
   1. [Цветовые схемы Termite](#цветовые-схемы-termite)
   1. [Заставка lockscreen](#заставка-lockscreen)
   1. [Сохранение/восстановление рабочего пространства](#сохранениевосстановление-рабочего-пространства)
1. [Частые проблемы](#частые-проблемы)
   1. [Что делать, если каталоги открываются в VSCode?](#что-делать-если-каталоги-открываются-в-vscode)
   1. [Enter password to unlock your login keyring](#enter-password-to-unlock-your-login-keyring)
1. [Справка по командам и т.д.](#справка-по-командам-и-тд)
   1. [Cheat.sh](#cheatsh)
   1. [Marker](#marker)
   1. [TLDR](#tldr)
1. [Шпаргалка по командам Shell](#шпаргалка-по-командам-shell)
<!-- /nav -->

# Установка Arch Linux

## Arch Linux

***Arch Linux*** ‒ это один из немногих дистрибутивов Linux, использующих модель роллинг-релизов. Это означает, что в нем доступны самые последние версии пакетов. Это одновременно является его как преимуществом так и недостатком. Пересесть на него меня заставила необходимость: мое компьютерное железо (процессор ryzen 5 2600 и видеоадаптер rx 590) оказались не совместимы с версией Linux Kernel младше 4.20.

![image](https://user-images.githubusercontent.com/12753171/61165815-cbe19b80-a514-11e9-9a11-6f854a50b93a.png)

На самом деле все не так плохо, но неприятные инциденты имеют место хотя и очень редко.

## Создание образа

Качаем [образ](https://www.archlinux.org/download/) и записываем его с помощью команды:

```bash
$ sudo dd if=/path/to/iso of=/dev/sdX bs=8M status=progress; sync
```

Где `sdX` &ndash; имя нашего USB устройства. Перегружаемся после удачного завершения операции.

В Windows для создания загрузочной флешки можно использовать [Rufus](https://rufus.ie/). При этом образ лучше записывать в dd режиме.

![image](https://user-images.githubusercontent.com/41215002/53678080-21867b80-3ccb-11e9-87a8-a4d028153a53.png)
![image](https://user-images.githubusercontent.com/41215002/53678082-2a774d00-3ccb-11e9-8a32-41f20d3dfd3c.png)

## Изменяем приоритет загрузки в BIOS/UEFI

При загрузке системы нажимаем F2 или Del (зависит от производителя материнской платы). Во вкладке BIOS в приоритете загрузки делаем первым наше USB-устройство. Нажимаем F10 и сохраняем настройки.

## Настройка сети

При подключении от кабеля ничего настраивать не надо. Настройка wifi требует ввода пары команд:

```bash
rfkill unblock wifi
wifi-menu
```

Следует отметить, что не все usb wifi адаптеры гараниторованно поддерживаются. Например, у меня не захотел работать dexp wfa 301, а вот с tp-link все ок.

## Размечаем диск

Для начала посмотрим все доступные устройства:

```bash
fdisk -l
```

Создадим новый раздел:

```bash
fdisk /dev/nvme0n1
```

Теперь нужно разметить раздел по LVM. Касательно LVM: единственное удобство в нем для меня – это возможность динамически менять размер разделов. Самая частая проблема, которая у меня была раньше – это то, что я не угадывал размер для корня. Когда в нем кончалось место, я с установочной флешки через gparted пытался отщепнуть от виндового раздела кусок (а у меня разделы всегда шли так: recovery, efi, reserved, windows, root, home), из этого куска создавал временный раздел, копировал в него файлы с хомяка, удалял хомяка, изменял размер корневого, опять создавал хомяка и из временного раздела копировал в него файлы, потом удалял временный раздел, расширял виндовый, правил `/etc/fstab`… А с LVM я могу просто выполнить пару команд: ужать хомяка, расширить корневой, причем. Увеличение размера логического раздела в отличии от уменьшения размонтирования не требует. Но эксперты могут возразить: «Хомяк на отдельном разделе не нужен!» — Да, если хочешь потерять все данные при переустановке.

В меню fdisk вводим `n` для создания нового раздела, порядковый номер раздела, потом начальное и конечные смещения. При задании конечного смещения можно отрицательное значение, например, `-10G`, так мы оставим свободными 10 Гб в конце диска. Для записи изменений на жесткий диск вводим `w` и выходим - `q`.

Создадим группу:

```bash
vgcreate lvm /dev/nvme0n1p5
```

Теперь создадим в ней логические разделы:

```bash
lvcreate -L 30G linux -n root
lvcreate -L 20G linux -n home
# Можно для раздела отдать все оставшееся место
lvcreate -L +100%FREE linux -n home
mkfs.ext4 /dev/linux/root
mkfs.ext4 /dev/linux/home
```

## Устанавливаем ядро

```bash
mount /dev/linux/root /mnt
mkdir /mnt/home
mount /dev/linux/home /mnt/home
mkdir -p /mnt/boot/efi
mount /dev/nvme0n1p2 /mnt/boot/efi
# Создаем файл подкачки. Не нужно верить дурачкам: он нужен всегда. Без него система будет лагать
fallocate -l 2G /mnt/swapfile
# Если хотим использовать гибернацию, то файл подкачки должен быть равен размеру оперативной памяти
# fallocate -l `awk '/Mem:/ {print $2}' <(free -m)`M /mnt/swapfile
chmod 600 /mnt/swapfile
mkswap /mnt/swapfile
swapon /mnt/swapfile
# Устанавливаем ядро системы
pacstrap /mnt base base-devel
```

## Генерируем fstab

```bash
genfstab /mnt >> /mnt/etc/fstab
```

## arch-chroot

```bash
# Предотвращаем ошибки lvm:
#   WARNING: Failed to connect lvmetad...
#   WARNING: Device /dev/nvme0n1 not initialized in udev database...
mkdir /mnt/hostlvm
mount --bind /run/lvm /mnt/hostlvm
arch-chroot /mnt
ln -s /run/lvm /hostlvm
```

## Настраиваем дату и локаль

```bash
ln -sf /usr/share/zoneinfo/Europe/Moscow /etc/localtime
hwclock --systohc
```

Далее:

```bash
nano /etc/locale.gen
```

Раскоментируем:

```bash
en_US.UTF-8
```

Генерируем локаль:

```bash
locale-gen
echo "LANG=en_US.UTF-8" > /etc/locale.conf
```

Если пропустить этот шаг, то не будет запускаться терминал.

## Прописываем хосты

```bash
echo "sergey-pc" > /etc/hostname
```

```bash
nano /etc/hosts
```

Добавляем в файл такие строки:

```
127.0.0.1 localhost
::1 localhost
127.0.1.1 sergey-pc.localdomain sergey-pc
```

## Initramfs

Если пропустить этот шаг, то система не станет грузиться с lvm.

Нам нужно отредактировать `/etc/mkinitcpio.conf` и модифицировать список HOOKS, добавив `lvm2` **ДО ЗНАЧЕНИЯ** `filesystems`:

```
HOOKS=(base udev autodetect modconf block lvm2 filesystems keyboard fsck)
```

Генерируем:

```bash
mkinitcpio -p linux
```

## Ставим пакеты

Эти пакеты понадобятся далее:

```bash
pacman -S sudo grub efibootmgr ntfs-3g os-prober alsa-utils xf86-video-ati gnome
```
xf86-video-ati – свободный драйвер для видеокарт AMD. xorg и xorg-server отдельно ставить не нужно, так как эти пакеты есть в зависимостях.

## Пользователи

Задаем пароль для супер-пользователя:

```bash
passwd
```

Создаем пользователя:

```bash
useradd -m -g users -G wheel -s /bin/bash sergey
```

Устанавливаем пароль для нового пользователя:

```
passwd sergey
chage -d 0 sergey
```

Пароль для пользователя можно ставить 1, так как при логине придется его сменит.

Теперь в файле `/etc/sudoers` нужно  раскоментировать строку:

```
%wheel ALL=(ALL:ALL) ALL
```

## Установка grub

```bash
grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id="Arch Linux"
```

Чтобы отключить автоматическую загрузку Linux, редактируем дефолтный конфиг груба:

```bash
nano /etc/default/grub
```

Меняем GRUB_TIMEOUT:

```
GRUB_TIMEOUT=-1
```

Затем генерируем grub:

```bash
grub-mkconfig -o /boot/grub/grub.cfg
```

## Завершение установки

Включаем gdm для экрана логина и MetworkManager для автоматического подключения к сети:

```bash
systemctl enable gdm
systemctl enable NetworkManager
```

Надо еще настроить звук:

```bash
# Сохраним на всякий случай состояние
alsactl store
# Для автоматического сохранения/восстановления значения громкости звука:
systemctl enable alsa-restore
```

Теперь можно выходить и перегружаться:

```bash
exit
reboot
```

---

# Пакетные менеджеры

Пакетным менеджером по-умолчанию для Arch Linux является pacman. Для подсветки вывода pacman в `/etc/pacman.conf` нужно раскомментировать `Color`. Пользовательским репозиторием является [AUR](https://aur.archlinux.org/). Пакеты из него можно использовать только на свой страх и риск. Чтобы не собирать пакеты из него ручками можно поставить yay:

```bash
sudo pacman -S git
cd /tmp
git clone https://aur.archlinux.org/yay.git
cd yay
makepkg -si
```

Пакеты всегда нужно ставить из репозиториев. Смысла собирать их из исходников нет, так как в AUR и так самые последние версии. Так будет меньше хлама оставаться в системе после их удаления.

В AUR много пакетов, оканчивающихся на `-git`. При их установке исходники копируются с github, а затем собираются, что занимает много времени и требуется дополнительное дисковое пространство для создания временных файлов и т.п., а еще для сборки могут потребоваться дополнительные пакеты. Поэтому лучше избегать установки таких пакетов, если есть альтернативы.

Синтаксис команды Yay аналогичен pacman. Так что будет полезным почитать справку по [pacman](https://wiki.archlinux.org/index.php/Pacman_(%D0%A0%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B9)).

Ссылки:

* [Сравнеие пакетных менеджеров](https://wiki.archlinux.org/index.php/AUR_helpers_(%D0%A0%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B9)).

# Нужные пакеты

Это список необходимых для меня пакетов:

```bash
yay -Sy linux-headers \ # нужны для компиляции некоторых программ
  wget \ # позволяет выполнять HTTP-запросы, скачивать файлы
  curl \ # делает то же самое, что и предыдущий
  adobe-source-code-pro-fonts \ # шрифт для терминала, нужен для темы Oh My Zsh! agnoster
  ttf-droid \ # шрифт по-умолчанию для VScode
  \ # шрифты по-умолчанию для Chrome
  \ # consolas-font \
  \ # ttf-ms-fonts \
  arc-gtk-theme-git \ # тема для интерфейса
  apache \ # самый популярный веб-сервер
  apache-tools \ # содержит ab, нагрузочный клиент
  \ # blender \ # самый простой 3D-редактор
  dconf-editor \ # все настройки gnome в одном месте
  dmraid \ # утилита для работы с raid-массивами дисков
  docker-compose \ # содержит docker и docker compose
  exfat-utils \ # добавляет поддержку файловой системы exfat
  firefox \ # один из лучших браузеров, единственный конкурент Chrome и единственный популярный non-chromium браузер
  flat-remix-git \ # тема с иконками
  \ # gimp \ # скромненький аналог Photoshop
  gnome-panel \ # я ставил только чтобы ярлыки из GUI создавать
  google-chrome \ # лучший браузер, противники проприетарщины предпочитают chromium
  chrome-gnome-shell \ # позволяет устанавливать расширения для Gnome
  gparted \ # графическая оболочка для разметки дисков
  htop \ # показывает запущенные процессы, загрузку cpu и потребление памяти
  \ # inkscape \ # векторный графический редактор
  \ # mariadb \ # свободная реализация самой популярной СУБД MySQL
  mc \ # аналог виндового Far + mcedit, замена nano
  \ # mongodb-bin \ # лучшая NoSQL база данных
  net-tools \ # содержит netstat
  neofetch \ # выводит в консоль информацию о системе
  nginx \ # самый быстрый веб-сервер
  ntfs-3g \ # добавляет поддержку файловой системы ntfs
  \ # nvm \ # менеджер версий для Node.js
  \ # postgresql \ # лучшая SQL база данных
  \ # pgadmin4 \ # админка для Postgres
  \ # pgmodeler \ # визуальный редактор для моделирования в Postgres
  \ # phpenv \ # менеджер версий для PHP
  \ # pyenv \ # менеджер версий для Python
  asdf-vm \ # Заменяет собой все выше перечисленные менеджеры версий + умеет управлять базами
  \ # redis \ # СУБД в оперативной памяти, используемая для межпроцессового взаимодействия
  smartmontools \ # утилита для проверки состояния SSD
  telegram-desktop-bin \ # лучший мессенджер
  texmaker \ # редактор LaTex, генерирует PDF
  tor \ # сервис, который можно использовать для подключения к сети Tor
  torsocks \ # утилита torify, которая заставляет другие программы работать через Tor
  transmission-qt \ # торрент-клиент
  thunderbird \ # email-клиент
  virtualbox \ # виртуальная машина, позволяет запускать Windows и Linux
  visual-studio-code-bin \ # лучший бесплатный текстовый редактор
  vlc \ # видеоплеер
  websocat-bin \ # утилита для тестированя вебсокетов
  woeusb \ # создание загрузочных флешек с Windows
  xclip \ # копирование файла в буффер обмена из консоли
  seahorse \ # Приложение для управления паролями, а так же PGP и SSH ключами

```

# Заменяем ядро на стабильное

Если надоело, что что-то ломается почти после каждого обновления ядра, запускаем терминал и выполняем:

```bash
yay -S linux-lts linux-headers-lts
yay -R linux linux-headers
mkinitcpio -p linux
```

# Права

4 - Чтение (r)
2 - Запись (w)
1 - Выполнение (x)

Сумма этих чисел дает разные сочетания типа:
1 + 2 + 4 = 7 или 1 + 4 = 5

Права задаются тремя числами, например, 755, где первое число – права владельца, далее: группа и остальные пользователи. Владелец может делать все  (1 + 2 + 4 = 7), другие пользователи – только читать и исполнять файлы (1 + 4 = 5).

Для работы с правами на файлы используется команда chroot:

```bash
chroot --help
```

В Python права можно записывать так:

```bash
0o755
```

```bash
$ ll
total 20K
drwxr-xr-x 3 sergey sergey 4,0K июн 20 17:22 backend
...

d         | rwx      | r-x    | r-x
тип файла | владелец | группа | остальные
```

Ссылки:

* [Права доступа к файлам и каталогам](https://www.linuxcenter.ru/lib/books/kostromin/gl_04_05.phtml)

# Добавляем путь в PATH

* Bash Shell: `~.bash_profile`, `~/.bashrc` or `~/.profile`
* Korn Shell: `~/.kshrc` or `~/.profile`
* Z Shell: `~/.zshrc` or `~/.zprofile`

```bash
export PATH=/path/to/bin:$PATH
```

# bin в домашнем каталоге

```bash
mkdir ~/bin
echo 'export PATH=$HOME/bin:$PATH' >> ~/.zprofile
# or
echo 'export PATH=$HOME/bin:$PATH' >> ~/.zshrc
```

Теперь самописные скрипты можно кидать в `~/bin`, так они будут доступны только для текущего пользователя.

`~/bin/hello`:

```bash
#!/usr/bin/env bash
function hello() {
  local name=${1:-World}
  printf "Hello, %s!\n" $name
}
hello $@
```

Сделаем скрпит исполняемым:

```bash
$ chmod +x ~/bin/hello
```

Проверка:

```bash
# Если не перелогинивались после добавления пути в ~/.zprofile, то сначала выполняем
$ source ~/.zprofile
$ hello $USER
Hello, sergey!
```

# Масштабировавние 150% как в Windows

По-умолчанию в Gnome масштабирование кратно 100. Чтобы добавить варианты масштабирования 125% и 150% нужно выполнить в терминале:

```bash
gsettings set org.gnome.mutter experimental-features "['scale-monitor-framebuffer']"
```

Отключение:

```
gsettings reset org.gnome.mutter experimental-features
```

# Расширения для Gnome

Устанавливаем [расширение](https://chrome.google.com/webstore/detail/gnome-shell-integration/gphhapmejobijbbhgpjhcjognlahblep?hl=ru) для Chrome.

![image](https://user-images.githubusercontent.com/41215002/53135292-b979bc00-358b-11e9-95df-7a540bc7b6f0.png)

Управление расширениями осуществляется через Tweaks.

![image](https://user-images.githubusercontent.com/41215002/53135669-25a8ef80-358d-11e9-9d5b-5024729dc550.png)

Расширения для установки:


| Название <img width="450"> | Описание <img width="450"> |
| -- | -- |
| [Dash to Dock](https://extensions.gnome.org/extension/307/dash-to-dock/). | Выезжающий Dash - панель с избранными приложениями |
| [Desktop Icons](https://extensions.gnome.org/extension/1465/desktop-icons/) | Иконки на рабочем столе |
| [ShellTile](https://extensions.gnome.org/extension/657/shelltile/) | Тайловый менеджер |
| [Log Out Button](https://extensions.gnome.org/extension/1143/logout-button/) | Добавляет кнопку, которая выполняет выход из системы |

# Пользовательские сочетания клавиш

В Settings → Devices → Keyboard добавляем сочетания клавиш:
* `Ctrl + Alt + T` для запуска терминала (`gnome-terminal`);
* `Ctrl + Alt + V`  для запуска Visual Code (`code`).

![image](https://user-images.githubusercontent.com/41215002/53122203-1adb6400-3567-11e9-919c-a031dce832e5.png)

# Шрифты

Шрифты надо кидать в `/usr/share/fonts` либо в `~/.fonts` или в `~/.local/share/fonts`. После выполняем:

```bash
$ fc-cache -f -v

# Чтобы проверить установлен ли шрифт
$ fc-list | grep "<name-of-font>"
```

![screenshot from 2019-02-20 23-17-46](https://user-images.githubusercontent.com/41215002/53122109-da7be600-3566-11e9-9de7-06582f3d6a53.png)

Наборы шрифтов:

* [Powrline Fonts](https://github.com/powerline/fonts);
* [Nerd Fonts](https://github.com/ryanoasis/nerd-fonts).

# Запуск исполняемых файлов по двойному клику в Nautilus

Заставляем Nautilus выполнять исполняемые файлы вместо открытия их в текстовом редакторе. Нужно нажать на три точки, а потом выбрать Preferences:

![image](https://user-images.githubusercontent.com/41215002/53286773-8bab9780-3784-11e9-8e41-44edba435356.png)

# Шаблоны файлов

Чтобы в Nautilus в контекстном меню отображался пункт `New Document`, нужно в `~/Templaytes` создать шаблоны файлов:

```bash
touch ~/Templates/{Empty\ Document,Text\ Document.txt,README.md,pyfile.py}
```

# ZSH

## Установка ZSH

```bash
$ yay -S zsh
```

Меняем shell на `/bin/zsh`:

```bash
$ chsh -s $(which zsh)
```

Чтобы изменения вступили в силу нужно залогиниться по-новой.

## [Oh My Zsh](https://github.com/robbyrussell/oh-my-zsh)

Установка:

```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
```

Пакет из репозитория ставится вне домашнего каталога, а потому требует root права при установке плагинов, что не удобно.

Так же для некоторых тем Oh My Zsh нужны шрифты наподобие Powerline:

```bash
yay -S powerline-fonts
```

Ставим must-have плагины:

```bash
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-completions ${ZSH_CUSTOM:=~/.oh-my-zsh/custom}/plugins/zsh-completions
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
```

Изменяем `.zshrc`:

```bash
ZSH_THEME="agnoster"
...
plugins=(
  command-not-found
  extract
  git
  zsh-autosuggestions
  zsh-completions
  zsh-syntax-highlighting
)

autoload -Uz compinit && compinit

source $ZSH/oh-my-zsh.sh
```

Для темы Agnoster настройках терминала выбираем шрифт `Source Code Pro Regular`, чтобы отображались стрелочки.

* [Встроенные темы](https://github.com/robbyrussell/oh-my-zsh/wiki/Themes);
* [Сторонние темы](https://github.com/robbyrussell/oh-my-zsh/wiki/External-themes).

## Темы Oh My Zsh!

### [Jovial](https://github.com/zthxxx/jovial)

```bash
# Сначала сохраняем копию zhsrc, потому как jovial изменить оригинальеный файл
$ cp ~/.zshrc ~/.zshrc.bak
$ curl -sSL git.io/jovial | sudo bash -s $USER
```

У меня эта тема упорно устанавливается в `/root/.oh-my-zsh`.

### [Powerlevel10k](https://github.com/romkatv/powerlevel10k)

Это красивая тема для ZSH.

```bash
git clone https://github.com/romkatv/powerlevel10k.git $ZSH_CUSTOM/themes/powerlevel10k
```

`~/.zshrc`:

```bash
ZSH_THEME=powerlevel10k/powerlevel10k
```

Изменим prompt:

```bash
cd && curl -fsSLO https://raw.githubusercontent.com/romkatv/dotfiles-public/master/.purepower
echo 'source ~/.purepower' >>! ~/.zshrc
```

![image](https://user-images.githubusercontent.com/12753171/60625968-d72c1d00-9dd8-11e9-902a-a0ecbe2279b1.png)

## Подробнее про ZSH

* [Приемы при работе с ZSH](http://zzapper.co.uk/zshtips.html).

# Разноцветный cat

* [ccat](https://github.com/jingweno/ccat);
* [lolcat](https://github.com/busyloop/lolcat).

# [Цветовые схемы для терминала](https://github.com/Mayccoll/Gogh)

```bash
# Интерактивная установка
bash -c  "$(wget -qO- https://git.io/vQgMr)"
# Удаление всех тем
dconf reset -f /org/gnome/terminal/legacy/profiles:/
```

Ссылки:

* [Обзор тем](https://mayccoll.github.io/Gogh/).

# Блокируем сайты с рекламой через hosts

```bash
wget -qO- https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts | sudo tee --append /etc/hosts
```

# [asdf-vm](https://github.com/asdf-vm/asdf)

Установка asdf через Git:

```bash
git clone https://github.com/asdf-vm/asdf.git ~/.asdf
cd ~/.asdf
git checkout "$(git describe --abbrev=0 --tags)"

echo -e '\n. $HOME/.asdf/asdf.sh' >> ~/.zshrc
echo -e '\n. $HOME/.asdf/completions/asdf.bash' >> ~/.zshrc
```

Установка asdf через AUR:

```bash
yay -S asdf-vm
```

В `~/.zshrc` (после compinit) добавляем строки:

```bash
. /opt/asdf-vm/asdf.sh
. /opt/asdf-vm/completions/asdf.bash
```

В `~/.zprofile`:

```bash
export PATH=/opt/asdf-vm/bin:$PATH
```

Эту строку можно и в `~/.zshrc`.

Удаление:

```bash
rm -rf ~/.asdf/ ~/.tool-versions
```

Примеры:

```bash
$ asdf plugin-add python
$ asdf install python 3.7.3
$ asdf install python 2.7.15
$ asdf list python
  2.7.15
  3.7.3
$ asdf uninstall python 2.7.15
$ asdf global python 3.7.3
# Сделать системную версию Python глобальной
$ asdf global python system
$ which python
/home/sergey/.asdf/shims/python

$ asdf plugin-add nodejs
# see: <https://github.com/asdf-vm/asdf-nodejs#install>
$ bash ~/.asdf/plugins/nodejs/bin/import-release-team-keyring
$ asdf install nodejs 10.16.0
$ asdf global nodejs 10.16.0
$ which node
/home/sergey/.asdf/shims/node
$ which npm
/home/sergey/.asdf/shims/npm
$ asdf list
golang
  1.12
nodejs
  10.16.0
postgres
  11.4
python
  2.7.15
  3.7.3
sqlite
  3.29.0
```

[Все доступные плагины](https://asdf-vm.com/#/plugins-all). При установке, использовании плагинов могут возникать проблемы. Например, плагин для Python работает поверх [pyenv](https://github.com/pyenv/pyenv) и при возникновении проблем, следует изучить страницу [«Common build problems»](https://github.com/pyenv/pyenv/wiki/common-build-problems).

> If you use pip to install a module like ipython that has a binaries. You will need to run asdf reshim python for the binary to be in your path.

После установки через pip пакетов, которые добавляют команды, чтобы те были доступны, нужно всегда выполнять `asdf reshim python`.

Ссылки:

* [Документация](https://asdf-vm.com/#/core-manage-asdf-vm).

# [NVM](https://github.com/nvm-sh/nvm)

> ⚠️ Использование [asdf-vm](#asdf-vm) предпочительнее.

Устанавливаем последнюю версию Node.js:

```bash
nvm install node
```

# Настройка Docker

```bash
sudo systemctl start docker
sudo systemctl enable docker
# sudo groupadd docker
# groupadd: group 'docker' already exists
sudo usermod -aG docker $USER
```

Нужно выйти и войти в систему, а потом проверить:

```bash
docker run hello-world
```

[Ссылка](https://docs.docker.com/install/linux/linux-postinstall/).

# Настройка Visual Code

```json
{
  "editor.fontSize": 16,
  "editor.rulers": [
    72,
    80,
    100,
    120
  ],
  "editor.tabSize": 2,
  "editor.wordWrap": "bounded",
  "editor.wordWrapColumn": 120,
  "files.insertFinalNewline": true,
  "files.trimFinalNewlines": true,
  "files.trimTrailingWhitespace": true,
  "terminal.integrated.fontFamily": "Source Code Pro"
}
```

# Гибернация

Режим гибернациии от режима сна отличается тем, что в первом случае содержимое оперативной памяти сохраняется на жесткий диск и питание полностью отключается, во втором - питание подается только на оперативку. Чем хороша гибернация? - Например, мы работаем в Linux, вошли в режим гибернации, а затем загрузились в Windows и играем. Когда мы в следующий раз загрузимся в Linux, то увидим все то, что было перед выключением. Прекрасно?! Но часто ли такое нужно?

При переходе в режим гибернации делается дамп памяти на диск, причем всей, а не только используемой, так что размер файла подкачки должен быть не меньше количества оперативки. Про гибернацию лучше почитать [здесь](https://help.ubuntu.ru/wiki/%D1%81%D0%BF%D1%8F%D1%89%D0%B8%D0%B9_%D1%80%D0%B5%D0%B6%D0%B8%D0%BC).

Режим гибернации по-умолчанию отключен. Чтобы его включить для начала нужно узнать UUID раздела, где расположен своп, а так же смещение своп-файла относительно начала раздела:

```bash
$ lsblk `df /swapfile | awk '/^\/dev/ {print $1}'` -no UUID
217df373-d154-4f2e-9497-fcac21709729
$ sudo filefrag -v /swapfile | awk 'NR == 4 {print $5}' | cut -d ':' -f 1
1423360
```

![screenshot from 2019-02-23 02-12-34](https://user-images.githubusercontent.com/41215002/53276552-8f053b80-3710-11e9-9770-5dd5e733f70a.png)

В `/etc/default/grub` прописать:

```config
GRUB_CMDLINE_LINUX_DEFAULT="quiet resume=UUID=217df373-d154-4f2e-9497-fcac21709729 resume_offset=1423360"
```

Теперь нужно обновить grub и сгенерировать initramfs:

```bash
sudo grub-mkconfig -o /boot/grub/grub.cfg
sudo mkinitcpio -p linux
```

Сам переход в режим гибернации выглядит так:

```bash
systemctl hibernate
```

Чтобы появилась кнопка для перехода в режим гибернации ставим [расширение](https://extensions.gnome.org/extension/755/hibernate-status-button/).

![image](https://user-images.githubusercontent.com/41215002/53138121-3f9b0000-3596-11e9-84c9-5e1277f80b31.png)
![image](https://user-images.githubusercontent.com/41215002/53138158-622d1900-3596-11e9-8a53-515e39382b03.png)

# RAID

В Linux RAID на аппаратном уровне называют FakeRAID. Для работы с FakeRAID  используется пакет dmraid.

Редактируем конфиг mkinitcpio:

```bash
sudo nano /etc/mkinitcpio.conf
```

В хуки добавляем dmraid:

```conf
HOOKS=(base udev autodetect modconf block lvm2 dmraid filesystems keyboard fsck)
```

И генерируем mkinitcpio:

```bash
sudo mkinitcpio -p linux
```

# LVM

## Изменение размера логического раздела

```bash
# Ключ -r выполняет resizefs
$ lvresize -r -L +10G /dev/linux/home
```

## Переименование логических разделов

```bash
$ sudo lvrename <oldname> <newname>
```

После нужно отредактировать `/etc/fstab`, изменив пути до разделов.

# Установка и настройка Postgres

```bash
[sergey@sergey-pc ~]$ sudo pacman -S postgresql
[sergey@sergey-pc ~]$ sudo chown postgres /var/lib/postgres/data
[sergey@sergey-pc ~]$ sudo -i -u postgres
[postgres@sergey-pc ~]$ initdb  -D '/var/lib/postgres/data'
[postgres@sergey-pc ~]$ logout
[sergey@sergey-pc ~]$ sudo systemctl start postgresql
[sergey@sergey-pc ~]$ sudo systemctl enable postgresql
[sergey@sergey-pc ~]$ sudo -u postgres -i initdb --locale $LANG -E UTF8 -D /var/lib/postgres/data
[sergey@sergey-pc ~]$
[postgres@sergey-pc ~]$ createuser --interactive -P
Enter name of role to add: sergey
Enter password for new role:
Enter it again:
Shall the new role be a superuser? (y/n)
Please answer "y" or "n".
Shall the new role be a superuser? (y/n) n
Shall the new role be allowed to create databases? (y/n) y
Shall the new role be allowed to create more new roles? (y/n) y
[postgres@sergey-pc ~]$ createdb -O sergey sergey # создаем пользователя и БД с именами совпадающими с пользователем системы, чтобы psql запускать без параметров
[postgres@sergey-pc ~]$ logout
[sergey@sergey-pc ~]$ psql
psql (11.1)
Type "help" for help.

sergey=>
```

# Работаем с github через ssh

Генерация нового ключа:

```bash
$ ssh-keygen -t rsa -b 4096 -C "buymethadone@gmail.com"
Generating public/private rsa key pair.
Enter file in which to save the key (/home/sergey/.ssh/id_rsa): /home/sergey/.ssh/codedumps_rsa
Created directory '/home/sergey/.ssh'.
...
```

В [настройках](https://github.com/settings/keys) нужно добавить сгенерированный ключ, скопировав содержимое pub-файла (для примера - github_rsa.pub), который лежит в `~/.ssh`.

Если уже есть проекты, которые были ранее склонированы по https, то нужно изменить `.git/config` проекта. :

```
...
[remote "origin"]
url = git@github.com:<username>/<project>.git
...
```

Правильный адрес проекта можно посмотреть на странице репозитория:

![image](https://user-images.githubusercontent.com/41215002/52008762-665b9e80-24e2-11e9-8ada-e6777df2a0ab.png)

Для проекта можно указать локальные email и имя:

```bash
git config user.email "buymethadone@gmail.com"
git config user.name "codedumps"
```

# Tor Service

Включаем Tor:

```bash
sudo systemctl start tor
sudo systemctl enable tor
```

Проверка:

```bash
$ torify curl http://httpbin.org/ip
{
  "origin": "173.244.209.5, 173.244.209.5"
}
```

# Emoji

```yay
yay -S ttf-emojione
```

# Блокировка рекламных сайтов

```bash
wget -qO- https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts | sudo tee --append /etc/hosts
```

# Редактирование DConf

DConf хранит профили терминала в `~/.config/dconf/user`, в формате GVDB [пруф](https://en.wikipedia.org/wiki/Dconf).

![image](https://user-images.githubusercontent.com/12753171/60671500-ba3c2c00-9e62-11e9-9f70-79b1bd9aed19.png)

```bash
# Делаем дамп
$ dconf dump / > /tmp/dconf
# Редактируем и загружаем
$ dconf load / < /tmp/dconf
```

---

# i3

## Описание

***i3*** &ndash; это тайловый оконный менеджер для Linux. Тут настройки под меня.

## Установка и настройка i3

```bash
$ yay -S awesome-terminal-fonts bumblebee-status compton fonts-powerline dmenu i3-gaps i3lock-fancy-git lxappearance nitrogen rofi scrot termite xclip
$ sudo nano /usr/share/xsessions/i3-custom.desktop
[Desktop Entry]
Name=i3 custom
Exec=/usr/local/bin/i3-custom
Type=Application
$ sudo nano /usr/local/bin/i3-custom
#!/bin/bash
mkdir -p ~/.config/i3/logs
export TERMINAL=termite
exec i3 -V >> ~/.config/i3/logs/$(date +'%F-%T').log 2>&1
$ sudo chmod +x /usr/local/bin/i3-custom
$ i3-config-wizard
$ cp /etc/xdg/termite/config ~/.config/termite/config
$ nano ~/.config/termite/config
[options]
# ...
font pango:Inconsolata, Font Awesome 10
# ...
[colors]
# ...
# 20% background transparency (requires a compositor)
background = rgba(63, 63, 63, 0.8)
$ cp /etc/xdg/compton.conf ~/.config
$ nano ~/.config/i3/config
# ...
font pango:Droid Sans 10
# ...
# Заменяем все Mod1 на $m и создаем переменную выше вызовов bindsym
set $m Mod1

# lockscreen
bindsym Ctrl+$m+l exec i3lock

# Pulse Audio controls
bindsym XF86AudioRaiseVolume exec --no-startup-id pactl set-sink-volume 0 +5% #increase sound volume
bindsym XF86AudioLowerVolume exec --no-startup-id pactl set-sink-volume 0 -5% #decrease sound volume
bindsym XF86AudioMute exec --no-startup-id pactl set-sink-mute 0 toggle # mute sound

# Sreen brightness controls
bindsym XF86MonBrightnessUp exec xbacklight -inc 20 # increase screen brightness
bindsym XF86MonBrightnessDown exec xbacklight -dec 20 # decrease screen brightness

# Touchpad controls
bindsym XF86TouchpadToggle exec /some/path/toggletouchpad.sh # toggle touchpad

# Media player controls
bindsym XF86AudioPlay exec playerctl play
bindsym XF86AudioPause exec playerctl pause
bindsym XF86AudioNext exec playerctl next
bindsym XF86AudioPrev exec playerctl previous

# rofi
bindsym $m+t exec "rofi -combi-modi window,drun -show combi"

# захватывает весь экран и копирует в буфер обмена
bindsym --release Print exec "scrot /tmp/%F_%T_$wx$h.png -e 'xclip -selection c -t image/png < $f && rm $f'"
# захватывает область экрана и копирует в буфер обмена
bindsym --release Shift+Print exec "scrot -s /tmp/%F_%T_$wx$h.png -e 'xclip -selection c -t image/png < $f && rm $f'"
# ...
bar {
  set $disk_format "{path}: {used}/{size}"
  status_command bumblebee-status -m nic disk:root disk:home cpu memory sensors pulseaudio datetime layout pacman -p root.left-click="nautilus /" root.format=$disk_format home.path=/home home.left-click="nautilus /home" home.format=$disk_format -t solarized-powerline
  position top
}
# ...
# отступы между окнами
gaps outer -10
gaps inner 20

floating_minimum_size 75 x 50
floating_maximum_size -1 x -1
# Убрать рамки у окон:
# 1)
# new_window pixel 0
# 2)
# for_window [class="^.*"] border none
# force floating for all new windows
# for_window [class=".*"] floating enable
for_window [class="Nautilus" instance="file_progress"] floating enable
for_window [class="^Telegram"] floating enable, resize set 800 600
# Всплывающие окна браузера
for_window [window_role="pop-up"] floating enable
# no_focus [window_role="pop-up"]
# прозрачность терминала
exec --no-startup-id compton --config ~/.config/compton.conf
# смена расскладки
exec --no-startup-id setxkbmap -model pc105 -layout us,ru -option grp:ctrl_shift_toggle
# восстановление заставки рабочего стола
exec --no-startup-id nitrogen --restore
```

Нужно выйти из сессии и выбрать в Display Manager сессию `i3 custom`.

**LXAppearance**  используется для изменения значков, шрифта по-умолчанию в приложениях.

**Nitrogen**  позволяет менять обои.

Для изменения оформления i3 &ndash; служит [i3-style](https://github.com/acrisci/i3-style):

```bash
$ yay -S i3-style
$ i3-style archlinux -o ~/.config/i3/config --reload
```

## XTerm

Вместо `Ctrl+Shift+V`  нужно использовать `Shift+Ins`, а вместо `Ctrl+Shift+C` &ndash; `Ctrl+C`. Права кнопка мыши копировать, клик по колесику &ndash; вставить.

## Termite: горячие клавиши

| Сочетание <img width=450> | Значение <img width=450> |
| -- | -- |
| `ctrl-shift-x` | activate url hints mode |
| `ctrl-shift-r` | reload configuration file |
| `ctrl-shift-c` | copy to CLIPBOARD |
| `ctrl-shift-v` | paste from CLIPBOARD |
| `ctrl-shift-u` | unicode input (standard GTK binding) |
| `ctrl-shift-e` | emoji (standard GTK binding) |
| `ctrl-tab` | start scrollback completion |
| `ctrl-shift-space` | start selection mode |
| `ctrl-shift-t` | open terminal in the current directory [1]_ |
| `ctrl-shift-up` | scroll up a line |
| `ctrl-shift-down` | scroll down a line |
| `shift-pageup` | scroll up a page |
| `shift-pagedown` | scroll down a page |
| `ctrl-shift-l` | reset and clear |
| `ctrl-+` | increase font size |
| `ctrl--` | decrease font size |
| `ctrl-=` | reset font size to default |

[Отсюда](https://github.com/thestinger/termite#keybindings).

## Цветовые схемы Termite

```bash
$ curl https://raw.githubusercontent.com/khamer/base16-termite/master/themes/base16-nord.config >> ~/.config/termite/config
$ nano ~/.config/termite/config
# 4-ое значение отвечает за прозрачность (1 - непрозрачно, 0 - абсолютная прозрачность)
background          = rgba(40, 44, 52, 0.8)
```

## Заставка lockscreen

```bash
$ yay -S i3lock-fancy-git
$ nano ~/.config/i3/config
# параметр -B делает фоном lockscreen скриншот экрана с размытием
bindsym Ctrl+$m+l exec i3lock-fancy -gpf Ubuntu -- scrot -z
```

[Репозиторий](https://github.com/khamer/base16-termite).

## Сохранение/восстановление рабочего пространства

```bash
# Сохранение
i3-save-tree --workspace 1 > ~/.i3/workspace-1.json
# Восстановление
i3-msg "workspace 1; append_layout ~/.i3/workspace-1.json"
```

Требует установки зависимостей.

[Документация](https://i3wm.org/docs/layout-saving.html).

---

# Частые проблемы

## Что делать, если каталоги открываются в VSCode?

Существует файл /usr/share/applications/mimeinfo.cache. В нем хранятся ассоциации между mime-типами и приложениями. Его редактирование исправляет проблему, НО такое решение является временным, так как этот файл генерируется при каждом обновлении системы из *.desktop файлов.

Нужно отредактировать MimeType (я его просто закомментировал) в /usr/share/applications/visual-studio-code.desktop и обновить mimeinfo.cache:

```bash
$ sudo nano /usr/share/applications/visual-studio-code.desktop
...
# MimeType=text/plain;inode/directory;
...
$ sudo update-desktop-database /usr/share/applications
```

## Enter password to unlock your login keyring

В один прекрасный день Chrome выдаст такое предупреждение, после чего перестанут сохраняться пароли и не будет работать автозаполнение форм для логина.

Решение:

```bash
# можно нажать `Super+A` и поискать приложение `passwords and keys`
$ seahorse &

# Если пакет не установлен
$ yay -S seahorse
```

![image](https://user-images.githubusercontent.com/12753171/61012059-723e6d00-a36c-11e9-8fbb-8e0b8ca26e5e.png)

Удаляем вкладку Login:

![image](https://user-images.githubusercontent.com/12753171/61012086-88e4c400-a36c-11e9-84c6-f8d17c0acc6c.png)

Другой вариант удалить все кейринги вручную:

```bash
$ rm -rf ~/.local/share/keyrings
```

Далее удаляем настройки Chrome:

```bash
$ rm -rf ~/.config/google-chrome
```

Теперь остается только перезапустить Chrome.

# Справка по командам и т.д.

## [Cheat.sh](https://github.com/chubin/cheat.sh)

Ищет на stackoverflow и других ресурсах справку по командам и языкам программирования.

Установка:

```bash
curl https://cht.sh/:cht.sh | sudo tee /usr/local/bin/cht.sh
sudo chmod +x /usr/local/bin/cht.sh

# Так же требуются пакеты xsel и rlwrap
yay -S xsel rlwrap
```

Использование:

```bash
# Интерактивный режим
$ cht.sh --shell <language>
$ cht.sh --shell bash
type 'help' for the cht.sh shell help
cht.sh/bash> for
# shell - Bash 'for' loop syntax?
#
# Replace

for (($i=0...

# with

for ((i=0;i<10;i++))

# [jman] [so/q/6854118] [cc by-sa 3.0]
cht.sh/bash>

$ cht.sh go create file
/*
 * go - Create an empty text file
 *
 * Don't try to check the existence first, since you then have a race if
 * the file is created at the same time. You can open the file with the
 * O_CREATE flag to create it if it doesn't exist:
 */

os.OpenFile(name, os.O_RDONLY|os.O_CREATE, 0666)

// [JimB] [so/q/35558787] [cc by-sa 3.0]

# Небольшой туториал по языку
$ cht.sh python :learn
```

## [Marker](https://github.com/pindexis/marker)

Установка:

```bash
$ git clone --depth=1 https://github.com/pindexis/marker ~/.marker && ~/.marker/install.py
```

* Ctrl-space: search for commands that match the current written string in the command-line.
* Ctrl-k (or marker mark): Bookmark a command.
* Ctrl-t: place the cursor at the next placeholder, identified by '{{anything}}'
* marker remove: remove a bookmark

## [TLDR](https://github.com/tldr-pages/tldr)

Этим я пользовался до cht.sh.

```bash
$ npm i tldr -g
```

Получаем краткую справку по команде:

```bash
$ tldr nvm
✔ Page not found. Updating cache...
✔ Creating index...

  nvm

  Install, uninstall or switch between Node.js versions.
  Supports version numbers like "0.12" or "v4.2", and labels like "stable", "system", etc.
  Homepage: https://github.com/creationix/nvm.

  - Install a specific version of Node.js:
    nvm install node_version

  - Use a specific version of Node.js in the current shell:
    nvm use node_version

  - Set the default Node.js version:
    nvm alias default node_version

  - List all available Node.js versions and highlight the default one:
    nvm list

  - Uninstall a given Node.js version:
    nvm uninstall node_version

  - Launch the REPL of a specific version of Node.js:
    nvm run node_version --version

  - Execute a script in a specific version of Node.js:
    nvm exec node_version node app.js


```

# Шпаргалка по командам Shell

```bash
# ==============================================================================
#
# Основы синтаксиса
#
# ==============================================================================

# $1, $2, $3, ... are the positional parameters.
# "$@" is an array-like construct of all positional parameters, {$1, $2, $3 ...}.
# "$*" is the IFS expansion of all positional parameters, $1 $2 $3 ....
# $# is the number of positional parameters.
# $- current options set for the shell.
# $$ pid of the current shell (not subshell).
# $_ most recent parameter (or the abs path of the command to start the current shell immediately after startup).
# $IFS is the (input) field separator.
# $? is the most recent foreground pipeline exit status.
# $! is the PID of the most recent background command.
# $0 is the name of the shell or shell script.

# присвоить значение переменной
x=42

# Для вывода используем echo и printf
echo "x=$x"
echo "x=${x}"
printf "x=%s\n" x

# Если переменная не задана, то присваиваем ей дефолтное значение
x=${x:-default}

# $ { varname :- word }
# If varname exists and isn’t null, return its value; otherwise return word.

# Purpose:
# Returning a default value if the variable is undefined.

# Example:
# ${count:-0} evaluates to 0 if count is undefined.

# $ { varname := word}
# If varname exists and isn’t null, return its value; otherwise set it to word and then return its value. Positional and special parameters cannot be assigned this way.

# Purpose:
# Setting a variable to a default value if it is undefined.

# Example:
# $ {count := 0} sets count to 0 if it is undefined.

# $ { varname :? message }
# If varname exists and isn’t null, return its value; otherwise print varname : followed by message, and abort the current command or script (non-interactive shells only). Omitting message produces the default message parameter null or not set.

# Purpose:
# Catching errors that result from variables being undefined.

# Example:
# {count :?” undefined! " } prints “count: undefined!” and exits if count is undefined.

# $ { varname :+word }
# If varname exists and isn’t null, return word; otherwise return null.

# Purpose:
# Testing for the existence of a variable.

# Example:
# $ {count :+ 1} returns 1 (which could mean “true”) if count is defined.


# $ { varname : offset }
# $ { varname : offset:length }

# Purpose:
# Returning parts of a string (substrings or slices).

# Example:
# If count is set to frogfootman, $ {count :4} returns footman. $ {count :4:4} returns foot.

# Экспорт глобальной переменной
export VAR=42

# Генерация строк с помощью Brace expansion
$ echo a{d,c,b}e
ade ace abe

# Массивы

arr=(Hello World)

echo ${arr[0]} ${arr[1]}

${arr[*]} # Все записи в массиве
${!arr[*]} # Все индексы в массиве
${#arr[*]} # Количество записей в массиве
${#arr[0]} # Длина первой записи (нумерация с нуля)

array=(one two three four [5]=five)

echo "Array size: ${#array[*]}"  # Выводим размер массива

echo "Array items:" # Выводим записи массива
for item in ${array[*]}
do
  printf "   %s\n" $item
done

echo "Array indexes:" # Выводим индексы массива
for index in ${!array[*]}
do
  printf "   %d\n" $index
done

echo "Array items and indexes:" # Выводим записи массива с их индексами
for index in ${!array[*]}
do
  printf "%4d: %s\n" $index ${array[$index]}
done

# Следующий пример покажет, как кавычки и конструкции без кавычек возвращают строки (особенно важно, когда в этих строках есть пробелы):

array=("first item" "second item" "third" "item")

echo "Number of items in original array: ${#array[*]}"
for ix in ${!array[*]}
do
  printf "   %s\n" "${array[$ix]}"
done
echo

arr=(${array[*]})
echo "After unquoted expansion: ${#arr[*]}"
for ix in ${!arr[*]}
do
  printf "   %s\n" "${arr[$ix]}"
done
echo

arr=("${array[*]}")
echo "After * quoted expansion: ${#arr[*]}"
for ix in ${!arr[*]}
do
  printf "   %s\n" "${arr[$ix]}"
done
echo

arr=("${array[@]}")
echo "After @ quoted expansion: ${#arr[*]}"
for ix in ${!arr[*]}
do
  printf "   %s\n" "${arr[$ix]}"
done

# Циклы

for i in $(seq 1 10);
do
  echo $i
done

for ((i = 0 ; i < max ; i++ ))
do
  echo $i
done

for i in {0..10}
do
  echo $i
done

for w in word1 word2 word3
do
  doSomething($w)
done

i=0
while (( ++i <= num )); do
  printf 'counter is at %d\n' "$i"
done

i=1
while [ "$i" -le "$num" ]; do
  printf 'counter is at %d\n' "$i"
  i=$(( i + 1 ))
done

# Условия

if [ "$seconds" -eq 0 ]; then
  timezone_string="Z"
elif [ "$seconds" -gt 0 ]; then
  timezone_string=$(printf "%02d:%02d" $((seconds/3600)) $(((seconds / 60) % 60)))
else
  echo "Unknown parameter"
fi

# В условиях нужно использовать двойные скобки

# [ is just a regular command with a weird name.
# ] is just an argument of [ that prevents further arguments from being used.

# [[ a = a && b = b ]]: true, logical and
# [ a = a && b = b ]: syntax error, && parsed as an AND command separator cmd1 && cmd2just an argument of [ that prevents further arguments from being used.

# x='a b'; [[ $x = 'a b' ]]: true, quotes not needed
# x='a b'; [ $x = 'a b' ]: syntax error, expands to [ a b = 'a b' ]

# Подробнее тут:
#   <https://stackoverflow.com/a/47576482>

# -eq
# is equal to

[ "$a" -eq "$b" ]

# -ne
# is not equal to

[ "$a" -ne "$b" ]

# -gt
# is greater than

[ "$a" -gt "$b" ]

# -ge
# is greater than or equal to

[ "$a" -ge "$b" ]

# -lt
# is less than

[ "$a" -lt "$b" ]

# -le
# is less than or equal to

[ "$a" -le "$b" ]

# <
# is less than (within double parentheses)

(("$a" < "$b"))

# <=
# is less than or equal to (within double parentheses)

(("$a" <= "$b"))

# >
# is greater than (within double parentheses)

(("$a" > "$b"))

# >=
# is greater than or equal to (within double parentheses)

(("$a" >= "$b"))

# <http://tldp.org/LDP/abs/html/comparison-ops.html>

# [ ‒ это всего лишь команда, последним аргументом которой всегда должна быть "]"! Все операторы описаны в man'е:
man [

# Это вполне себе валидное выражение
"[" 1 -eq 0 "]" || echo fail

# Строка слева всегда имя переменной
x=42; [[ "x" -eq "42" ]] || echo fail

# выражение слева всегда переменная

case $VAR in
  foo) ... ;;
  bar) ... ;;
  # Все остальные значения
  *) ... ;;
esac

# Объявление функции
foo() {
  # Аргументы функции
  $1..$N
  # Локальная переменная
  local x=42
  ...
  # Теперь в $1 будет $2, в $2 ‒ $3 и т.д.
  shift
}

# Экспорт функции
export -f foo

die() { echo "$*" 1>&2 ; exit 1; }
...
die "Kaboom"

[ "$#" -eq 2] || die "Needs 2 arguments, input and output"

# The syntax is token-level, so the meaning of the dollar sign depends on the token it's in. The expression $(command) is a modern synonym for `command` which stands for command substitution; it means, run command and put its output here. So

echo "Today is $(date). A fine day."

# Управление выводом

# Направить stdout одной программы в stdin другой
command1 | command2

# Перенаправление stdout и stderr
command1 |& command2

# Создать либо перезаписать файл, добавив строку
command > out

# Создать файл, если его не существует и дописать строку в конец
command >> out

# Направить stderr команды в файл
command 2>&1 out

# stdout 2-ой команды, является stdin для первой
command1 <<< command2

# Вывод многострочного текста
cat <<EOF
хуй
пизда
джигурда
EOF

# ==============================================================================
#
# Написание скриптов
#
# ==============================================================================

# Первой строкой скрипта идет Shebang, торый указывает какой интерпретатор использовать

#!/usr/bin/env bash

# Так же часто делают каталог скрипта рабочим (по-умолчанию рабочим является тот откуда запустили скрипт)
cd "$(dirname "$0")"

# ==============================================================================
#
# Выполнение скриптов
#
# ==============================================================================

# Сделать файл исполняемым
$ chmod +x /path/to/file

# Выполнит скрипт в текущем процессе (переменные и функции, объявленные внутри скрипта станут доступны в терминале)
$ source /path/to/file

# ==============================================================================
#
# Запуск команд
#
# ==============================================================================

# Запустить процесс и вернуть его дескриптор (при закрытии терминала будет остановлена)
$ command &

# То же самое за исключением того, что процесс не будет остановлен при закрытии терминала
$ nohup command &

# ==============================================================================
#
# Пакеты
#
# ==============================================================================

# Установить пакет
$ yay -S <package>

# Удалить пакет
$ yay -Rns <package>

# Обновить все установленные пакеты
$ yay -Syu

# Обновить в т.ч. с пакетами для разработчика
$ yay -Syu --devel --timeupdate

# Удалить все ненужные зависимости
$ yay -Yc

# Статистика по пакетами
$ yay -Ps

# Generates development package DB used for devel updates
$ yay -Y --gendb

# Ошибки с удалением зависимостей

$ yay -Rns gnome-extra
checking dependencies...
error: failed to prepare transaction (could not satisfy dependencies)
:: nautilus: removing nautilus-sendto breaks dependency 'nautilus-sendto'
$ yay -Rdd nautilus-sendto

# Теперь можно снести gnome-extra

# ==============================================================================
#
# systemd
#
# ==============================================================================

# Все сервисы

# Покажут только включенные
$ systemctl
$ systemctl list-units --type service

# + выключенные
$ systemctl list-unit-files --type service

$ sudo systemctl enable docker

$ sudo systemctl disable docker

$ sudo systemctl restart nginx.service

$ sudo systemctl start application.service

$ sudo systemctl start application.service

$ systemctl status nginx.service

# ==============================================================================
#
# Текст
#
# ==============================================================================

# Замена в тексте
$ echo "This is a test" | sed 's/test/another test/'

# Ключ -e позволяет выполнить несколько команд:
#   sed -e 's/This/That/; s/test/another test/'

# Перевод регистра
$ echo lowercase | tr '[:lower:]' '[:upper:]'
LOWERCASE

# ==============================================================================
#
# Файловая система
#
# ==============================================================================

# Список разделов
$ sudo fdisk -l

# Монтировать устройство
$ mount /dev/linux/root /mnt

# В Linux все файлы. Регулярные файлы ‒ обычные файлы, каталоги ‒ это файлы содержащие список файлов и т.д.

# Перемещение/переименование файла
$ mv <src> <dst>

# Копирование файлов
$ cp <src> <dst>

# Копировать каталог и все вложенные файлы
$ cp -r <src> <dst>

# Полный путь до файла
$ realpath example.txt
/home/username/example.txt

# Листинг каталога
$ ls
$ tldr ls

# Вывести информацию о владельце и группе файла
$ ls -ld /path/to/file
$ stat /path/to/file

# Вывести все вложенные файлы
$ ls -R <path>
$ find <path> -print
# Покажет имя и размер
$ du -a <path>

# Создание каталога
$ mkdir <target>

# Создание каталога вместе с родительскими каталогами, если тех не существует
$ mkdir -p <target>

# Создать каталог с определенными правами
$ mkdir -m 0750 <directory>

# Создание множества каталогов
$ mkdir foo bar baz
# или
$ mkdir prefix-{foo,bar,baz}

# Такой же трюк работает при создании файлов
$ touch {foo,bar,baz}.txt

# Создать мягкую ссылку на файл либо заменить ее новой
$ ln -sf path/to/new_file path/to/symlink

# Мягкая ссылка содержит путь до файла. Жесткая ссылается на inode, искомый
# файл при перемещении остается доступен по ссылке и невозможно ссылаться на
# файл на другом устройстве

# Заархивировать каталог
$ tar -czvf filename.tar.gz directory

# Для извлечения файлов проще всего пользоваться плагином Oh My ZSH extract

# Извлечь архив и удалить его (ключ -r)
$ extract -r <filename>

# Слияние файлов в один
$ paste file1.txt file2.txt > fileresults.txt

# Удалить файлы старше 5 дней
$ find /path/to/files* -mtime +5 -exec rm {} \;

# Поиск фала по имени в специальной базе
$ locate -e login.keyring
/home/sergey/.local/share/keyrings/login.keyring

# Установка
$ yay -S mlocate

# Перед первым запуском следует выполнить
$ sudo updatedb

# После установки будет доступен сервис updatedb.timer, который будет ежедневно обновлять базу

# Стастика
$ locate -S
Database /var/lib/mlocate/mlocate.db:
	157 512 directories
	1 384 522 files
	119 423 666 bytes in file names
	38 722 751 bytes used to store database

# Покажет что куда смонтировано (можно свободное место узнать)
$ df -h --total

# Узнать на каком разделе смонтирован каталог
$ df -h /tmp

# Просмотр числа inode
$ df -i

# Просмотр содержимого фйала с навигацией
$ less /path/to/file

# или более короткая версия в ZSH
$ < /path/to/file

# Просмотр логов в обратном порядке
$ tail -r /var/log/syslog | less

# Вывести строки не соответствующие шаблону
$ grep -Pv <exclude_pattern> <filename>

# Создать файл, забитый null-байтами
$ dd if=/dev/zero of=/tmp/nullbytes bs=1M count=1

# Конфертировать .md в .rst
$ pip install m2r
$ m2r --help

# Конвертировать .webp в .png
$ yay -S libwebp
$ dwebp file.webp -o file.png

# Вывод содержимого файла с подсветкой синтаксиса
$ yay -S ccat
$ ccat ./file

# Вывести файлы в каталоге, отсортировав их по времени до доступа
$ ls -ltu <path>

# Увеличиваем размер логического раздела
$ sudo lvresize -L +10GB /dev/mapper/lvm-root

# После lvresize нужно обязательно изменить размер файловой системы
$ sudo resize2fs /dev/mapper/lvm-root

# Делает то же самое, что и две команды выше
$ sudo lvresize -r -L +10GB /dev/mapper/lvm-root

# Список логических разделов LVM
$ sudo lvscan
  ACTIVE            '/dev/linux/root' [40.00 GiB] inherit
  ACTIVE            '/dev/linux/home' [20.00 GiB] inherit

# Изменить размер каталога /tmp
$ mount -o remount,size=4G /tmp/

# Подробная информация о диске
$ sudo smartctl -a /dev/nvme0

# ==============================================================================
#
# Сеть
#
# ==============================================================================

# Показать все прослушиваемые и установленные порты TCP и UDP вместе с PID
# связанного процесса
$ netstat -plantu

# Все запущенные сервера на хосте
$ netstat -lnt

# ==============================================================================
#
# Шрифты
#
# ==============================================================================

# Список установленных шрифтов
$ fc-list

# Обновить базу шрифтов после добавления/удаления их в/из `/usr/share/fonts`
# либо `~/.local/share/fonts`
$ fc-cache -f -v

# ==============================================================================
#
# Буфер обмена
#
# ==============================================================================

$ yay -S xclip

# Скопировать текст в буфер обмена
$ echo 123 | xclip -sel clip

# Копировать содержимое файла в буфер обмена
$ xclip -sel clip < ~/.ssh/github_rsa.pub

# Вывести содержимое буфера обмена
$ xclip -o -sel clip

# Конвертировать файл в base64 и скопировать в буфер обмена
$ file="test.docx"
$ base64 -w 0 $file  | xclip -selection clipboard

# ==============================================================================
#
# Git
#
# ==============================================================================

# Первоначальная настройка (без флага --global локального проекта)
$ git config --global user.name <yourname>
$ git config --global user.email <email>

# Сменить ветку
$ git checkout <branchname>

# Создать ветку и переключится на нее
$ git checkout -b <branchname>

# Объединить текущую ветку с branchname
$ git merge <branchname>

# Добавить изменения (все файлы в каталоге и вложеннхы)
$ git add .

# Закоммитить изменения (сделать описание)
$ git commit -m "Тест"

# Если не были добавлены новые файлы, а лишь производились изменения в уже добавленных, то можно использовать только одну команду
$ git commit -am "Тест"

# Обновить репозиторий на сервере
$ git push

# Выгрузить изменения с сервера (тоже самое, что git fetch + git merge)
$ git pull

# Копировать репозиторий
$ git clone https://github.com/someuser/repo.git [<assigneddirectory>]

# Посмотреть историю
$ git log --graph --oneline --decorate --all

# Посмотреть отличия по сравнения с предыдущей версией
$ git diff 871d36b [<filename>]

# Сохранить изменения
$ git stash [save "my stash message here"]

# Удалить stach и применить его
$ git stash pop [stash@{1}]

# Список stash
$ git stash list

# Посмотреть что там лежит
$ git stash show stash@{0}

$ git stash apply
$ git stash drop stash@{2}
$ git stash clear

# List all the tags:

$ git tag

# Search tags for a particular pattern:

$ git tag -l <tag-pattern>

# Show a tag data:

$ git show <tag-name>

# Create a Lightweight Tag:

$ git tag <tag-name>

# Create an Annotated Tag:

$ git tag -a <tag-name> -m <tag-message>

# Create a tag for a specific commit:

$ git tag -a <tag-name> <commit-checksome>

# Push a specific tag to remote:

$ git push origin <tag-name>

# Push all the tags to remote:

$ git push origin --tags

# Checkout a specific to local:

$ git checkout -b <branch-name> <tag-name>

# ==============================================================================
#
# Языковые настройки
#
# ==============================================================================

# Список влюченных локалей
$ locale -a

# Добавление локалей

# В этом файле находится список всех поддерживаемых локалей
# Раскомментируем нужную
$ sudo nano /etc/locale.gen

# Генерируем локали
$ sudo locale-gen

# Можно так же локали так добавлять
$ sudo locale-gen de_DE.UTF-8

# Меняем язык системы (нужно перегрузиться)
echo "LANG=de_DE.UTF-8" > /etc/locale.conf

# ==============================================================================
#
# Генерация паролей
#
# ==============================================================================

$ yay -S pwgen
$ pwgen -cnsy 10 1
1u_dr<ZLH;

$ pip install xkcdpass
$ xkcdpass -n 3 -d -
backdrop-unruly-yodel
$ xkcdpass -n 3 -d - --min 2 --max 6
shrank-trio-thong

# ==============================================================================
#
# Прочее
#
# ==============================================================================

# Перегрузить Shell
$ exec "$SHELL"

# Список всех доступных команд
$ compgen -c

# Ищем Chrome
$ compgen -c | grep chrome
google-chrome-stable
chrome-gnome-shell
google-chrome

# Просмотр логов в реальном времени
$ journalctl -f

# Изменить размер терминала
$ gnome-terminal --geometry 135x45

# Документация по командам
$ tldr cat
$ tldr --search create file

# Сделать дам базы
$ pg_dump -d test -f /tmp/schema.sql

# Мониторинг процессов
$ yay -S htop
$ htop
```

Ссылки:

* [Цвет и форматирование текста в консоли](https://misc.flogisoft.com/bash/tip_colors_and_formatting);
* [Поиск файлов на Сервере](https://www.8host.com/blog/ispolzovanie-find-i-locate-dlya-poiska-fajlov-na-servere-linux/);
* [Файловая система Linux](https://opencentr.ru/article/fajlovaya-sistema-linux/);
* [Inode](https://ru.wikipedia.org/wiki/Inode);
* [Управление разделами LVM](https://web.mit.edu/rhel-doc/5/RHEL-5-manual/Deployment_Guide-en-US/s1-disk-storage-lvm.html);
* [Часто используемые команды Git](https://carolinegabriel.com/used-git-commands-copy-paste-format/).
