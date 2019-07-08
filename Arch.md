# Установка

## Предисловие

***Arch Linux*** &ndash; это самый современный дистрибутив Linux. В нем доступны самые последние версии пакетов, так как он использует модель роллинг-релизов. Это одновременно является его как преимуществом так и недостатком. Пересесть на него меня заставила необходимость: мое компьютерное железо (процессор ryzen 5 2600 и видеоадаптер rx 590) оказались не совместимы с версией linux kernel младше 4.20.

## Создание образа

Качаем образ с сайта и записываем его с помощью команды:

```bash
$ sudo dd if=/path/to/iso of=/dev/sdX bs=8M status=progress; sync
```

Где `sdX` &ndash; имя нашего USB устройства. Перегружаемся после удачного завершения операции.

В Windows для создания загрузочной флешки можно использовать [Rufus](https://rufus.ie/). При этом образ лучше записывать в dd режиме.

![image](https://user-images.githubusercontent.com/41215002/53678080-21867b80-3ccb-11e9-87a8-a4d028153a53.png)
![image](https://user-images.githubusercontent.com/41215002/53678082-2a774d00-3ccb-11e9-8a32-41f20d3dfd3c.png)

## Заходим в BIOS/UEFI

При загрузке системы нажимаем F2 или Del (зависит от производителя материнской платы). Во вкладке BIOS в приоритете загрузки делаем первым наше USB-устройство. Нажимаем F10 и сохраняем настройки.

## Настройка сети

При подключении от кабеля ничего настраивать не надо. Настройка wifi требует ввода пары команд:

```bash
rfkill unblock wifi
wifi-menu
```

Следует отметить, что не все usb wifi адаптеры гараниторованно поддерживаются. Например, у меня не захотел работать dexp wfa 301, а вот с tp-link все ок.

## Разметка диска

Для начала посмотрим все доступные устройства:

```bash
fdisk -l
```

Создадим новый раздел:

```bash
fdisk /dev/nvme0n1
```

В меню fdisk вводим `n` для создания нового раздела, порядковый номер раздела, потом начальное и конечные смещения. При задании конечного смещения можно отрицательное значение, например, `-10G`, так мы оставим свободными 10 Гб в конце диска. Для записи изменений на жесткий диск вводим `w` и выходим - `q`.

Теперь нужно разметить раздел по LVM. LVM очень удобная вещь и позволяет динамически менять размеры виртуальных разделов. И самое главное: если у вас в разделе с LVM заканчивается место, то вы можете просто включить в группу другой раздел (даже на другом диске) либо целый диск.

Создадим группу:

```bash
vgcreate lvm /dev/nvme0n1p5
```

Теперь создадим в ней логические разделы:

```bash
lvcreate -L 30G arch -n root
lvcreate -L 20G arch -n home
mkfs.ext4 /dev/lvm/root
mkfs.ext4 /dev/lvm/home
```

## Устанавливаем ядро

```bash
mount /dev/lvm/root /mnt
mkdir /mnt/home
mount /dev/lvm/home /mnt/home
mkdir -p /mnt/boot/efi
mount /dev/nvme0n1p2 /mnt/boot/efi
# Создаем файл подкачки
fallocate -l 2G /mnt/swapfile
# Если хотим использовать гибернацию
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
pacman -S sudo grub efibootmgr ntfs-3g os-prober alsa-utils xf86-video-ati gnome gnome-extra
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

## Завершение

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

# Настройка

## Введение

Тут описана настройка системы для использования ее в веб-разработке.

## Пакетные менеджеры

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

## Нужные пакеты

Это список необходимых для меня пакетов:

```bash
yay -Sy linux-headers \ # нужны для компиляции некоторых программ
  wget \ # позволяет выполнять HTTP-запросы, скачивать файлы
  curl \ # делает то же самое, что и предыдущий
  adobe-source-code-pro-fonts \ # шрифт для терминала, нужен для темы Oh My Zsh! agnoster
  ttf-droid \ # шрифт по-умолчанию для VScode
  \ # шрифты по-умолчанию для Chrome
  consolas-font \
  ttf-ms-fonts \
  arc-gtk-theme-git \ # тема для интерфейса
  apache \ # самый популярный веб-сервер
  apache-tools \ # содержит ab, нагрузочный клиент
  blender \ # самый простой 3D-редактор
  dconf-editor \ # все настройки gnome в одном месте
  dmraid \ # утилита для работы с raid-массивами дисков
  docker-compose \ # содержит docker и docker compose
  exfat-utils \ # добавляет поддержку файловой системы exfat
  firefox \ # один из лучших браузеров, единственный конкурент Chrome и единственный популярный non-chromium браузер
  flat-remix-git \ # тема с иконками
  gimp \ # скромненький аналог Photoshop
  gnome-panel \ # я ставил только чтобы ярлыки из GUI создавать
  google-chrome \ # лучший браузер, противники проприетарщины предпочитают chromium
  chrome-gnome-shell \ # позволяет устанавливать расширения для Gnome
  gparted \ # графическая оболочка для разметки дисков
  htop \ # показывает запущенные процессы, загрузку cpu и потребление памяти
  inkscape \ # векторный графический редактор
  mariadb \ # свободная реализация самой популярной СУБД MySQL
  mc \ # аналог виндового Far + mcedit, замена nano
  mongodb-bin \ # лучшая NoSQL база данных
  net-tools \ # содержит netstat
  neofetch \ # выводит в консоль информацию о системе
  nginx \ # самый быстрый веб-сервер
  ntfs-3g \ # добавляет поддержку файловой системы ntfs
  \ # nvm \ # менеджер версий для Node.js
  \ # postgresql \ # лучшая SQL база данных
  pgadmin4 \ # админка для Postgres
  pgmodeler \ # визуальный редактор для моделирования в Postgres
  \ # phpenv \ # менеджер версий для PHP
  \ # pyenv \ # менеджер версий для Python
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
  xclip # копирование файла в буффер обмена из консоли
```

Если забыли отменить установку гномовского браузера, выпиливаем его:

```bash
yay -Rns epiphany
```

## Масштабировавние 150% как в Windows

По-умолчанию в Gnome масштабирование кратно 100. Чтобы добавить варианты масштабирования 125% и 150% нужно выполнить в терминале:

```bash
gsettings set org.gnome.mutter experimental-features "['scale-monitor-framebuffer']"
```

Отключение:

```
gsettings reset org.gnome.mutter experimental-features
```

## Заменяем ядро на стабильное

Если надоело, что что-то ломается почти после каждого обновления ядра, запускаем терминал и выполняем:

```bash
yay -S linux-lts linux-headers-lts
yay -R linux linux-headers
mkinitcpio -p linux
```

## Пользовательские сочетания клавиш

В Settings → Devices → Keyboard добавляем сочетания клавиш:
* `Ctrl + Alt + T` для запуска терминала (`gnome-terminal`);
* `Ctrl + Alt + V`  для запуска Visual Code (`code`).

![image](https://user-images.githubusercontent.com/41215002/53122203-1adb6400-3567-11e9-919c-a031dce832e5.png)

## Шрифты

Шрифты надо кидать в `/usr/share/fonts` либо в `~/.fonts` или в `~/.local/share/fonts`. После выполняем:

```zsh
$ fc-cache -f -v

# Чтобы проверить установлен ли шрифт
$ fc-list | grep "<name-of-font>"
```

![screenshot from 2019-02-20 23-17-46](https://user-images.githubusercontent.com/41215002/53122109-da7be600-3566-11e9-9de7-06582f3d6a53.png)

Наборы шрифтов:

* [Powrline Fonts](https://github.com/powerline/fonts);
* [Nerd Fonts](https://github.com/ryanoasis/nerd-fonts).

## Запуск исполняемых файлов по двойному клику

Заставляем Nautilus выполнять исполняемые файлы вместо открытия их в текстовом редакторе. Нужно нажать на три точки, а потом выбрать Preferences:

![image](https://user-images.githubusercontent.com/41215002/53286773-8bab9780-3784-11e9-8e41-44edba435356.png)

## Шаблоны файлов

Чтобы в Nautilus в контекстном меню отображался пункт `New Document`, нужно в `~/Templaytes` создать шаблоны файлов:

```bash
touch ~/Templates/{Empty\ Document,Text\ Document.txt,README.md,pyfile.py}
```

## Расширения для Gnome

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

## ZSH

### Установка

```bash
$ yay -S zsh
```

Меняем shell на `/bin/zsh`:

```bash
$ chsh -s $(which zsh)
```

Чтобы изменения вступили в силу нужно залогиниться по-новой.



### [Oh My Zsh](https://github.com/robbyrussell/oh-my-zsh)

Установка:

```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
```

Пакет из репозитория ставится вне домашнего каталога, а потому требует root права при установке плагинов, что не удобно.

Копируем файл настроек (не нужно):

```bash
cp /usr/share/oh-my-zsh/zshrc ~/.zshrc
```

Так же для некоторых тем Oh My Zsh нужны шрифты наподобие Powerline:

```bash
yay -S powerline-fonts
```

Ставим must-have плагины:

```zsh
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

### [Powerlevel10k](https://github.com/romkatv/powerlevel10k)

Это красивая тема для ZSH.

```zsh
git clone https://github.com/romkatv/powerlevel10k.git $ZSH_CUSTOM/themes/powerlevel10k
```

`~/.zshrc`:

```zsh
ZSH_THEME=powerlevel10k/powerlevel10k
```

Изменим prompt:

```zsh
cd && curl -fsSLO https://raw.githubusercontent.com/romkatv/dotfiles-public/master/.purepower
echo 'source ~/.purepower' >>! ~/.zshrc
```

![image](https://user-images.githubusercontent.com/12753171/60625968-d72c1d00-9dd8-11e9-902a-a0ecbe2279b1.png)

### Ссылки

* [Приемы при работе с ZSH](http://zzapper.co.uk/zshtips.html).

## [Цветовые схемы для Gnome Terminal](https://github.com/Mayccoll/Gogh)

```bash
# Интерактивная установка
bash -c  "$(wget -qO- https://git.io/vQgMr)"
# Удаление всех тем
dconf reset -f /org/gnome/terminal/legacy/profiles:/
```

Ссылки:

* [Обзор тем](https://mayccoll.github.io/Gogh/).

## Блокируем сайты с рекламой через hosts

```bash
wget -qO- https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts | sudo tee --append /etc/hosts
```

## [asdf-vm](https://github.com/asdf-vm/asdf)

### Установка:

#### Git

```bash
git clone https://github.com/asdf-vm/asdf.git ~/.asdf
cd ~/.asdf
git checkout "$(git describe --abbrev=0 --tags)"

echo -e '\n. $HOME/.asdf/asdf.sh' >> ~/.zshrc
echo -e '\n. $HOME/.asdf/completions/asdf.bash' >> ~/.zshrc
```

#### AUR

```bash
yay -S asdf-vm
```

В `~/.zshrc` (после compinit) добавляем строки:

```zsh
. /opt/asdf-vm/asdf.sh
. /opt/asdf-vm/completions/asdf.bash
```

В `~/.zprofile`:

```zsh
export PATH=/opt/asdf-vm/bin:$PATH
```

Эту строку можно и в `~/.zshrc`.

### Удаление

```bash
rm -rf ~/.asdf/ ~/.tool-versions
```

### Примеры

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
```

[Все доступные плагины](https://asdf-vm.com/#/plugins-all). При установке, использовании плагинов могут возникать проблемы. Например, плагин для Python работает поверх [pyenv](https://github.com/pyenv/pyenv) и при возникновении проблем, следует изучить страницу [«Common build problems»](https://github.com/pyenv/pyenv/wiki/common-build-problems).

> If you use pip to install a module like ipython that has a binaries. You will need to run asdf reshim python for the binary to be in your path.

После установки через pip пакетов, которые добавляют команды, чтобы те были доступны, нужно всегда выполнять `asdf reshim python`.

### Ссылки

* [Документация](https://asdf-vm.com/#/core-manage-asdf-vm).

## Использование [NVM](https://github.com/nvm-sh/nvm)

Устанавливаем последнюю версию Node.js:

```bash
nvm install node
```

## [TLDR](https://github.com/tldr-pages/tldr)

```bash
npm i tldr -g
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

## Настройка Docker

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

## Настройка Visual Code

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

## Гибернация

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

## RAID

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

## Установка и настройка Postgres

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

## Работаем с github через ssh

Генерация нового ключа:

```bash
$ ssh-keygen -t rsa -b 4096 -C "buymethadone@gmail.com"
Generating public/private rsa key pair.
Enter file in which to save the key (/home/sergey/.ssh/id_rsa): /home/sergey/.ssh/codedumps_rsa
Created directory '/home/sergey/.ssh'.
...
```

В [настройках](https://github.com/settings/keys) нужно добавить сгенерированный ключ, скопировав содержимое pub-файла (для примера - codedumps_rsa.pub), который лежит в `~/.ssh`.

Если уже есть проекты, которые были ранее склонированы по https, то нужно изменить `.git/config` проекта. :

```
...
[remote "origin"]
	url = git@github.com:codedumps/pgrpc.git
...
```

Правильный адрес проекта можно посмотреть на странице репозитория:

![image](https://user-images.githubusercontent.com/41215002/52008762-665b9e80-24e2-11e9-8ada-e6777df2a0ab.png)

Для проекта можно указать локальные email и имя:

```bash
git config user.email "buymethadone@gmail.com"
git config user.name "codedumps"
```

## Tor Service

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

## Emoji

```yay
yay -S ttf-emojione
```

## Блокировка рекламных сайтов

```bash
wget -qO- https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts | sudo tee --append /etc/hosts
```

## Редактирование DConf

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

## Установка и настройка

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

# Шпаргалка по командам Shell

```bash
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

# Создать мягкую ссылку на файл либо заменить ее новой
$ ln -sf path/to/new_file path/to/symlink

# Мягкая ссылка содержит путь до файла. Жесткая ссылается на inode, искомый
# файл при перемещении остается доступен по ссылке, невозможно ссылаться на
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

# Увеличить размер логического раздела LVM
$ sudo lvresize -L +10GB /dev/mapper/lvm-root

# Покажет что куда смонтировано (можно свободное место узнать)
$ df -h --total

# Узнать на каком разделе смонтирован каталог
$ df -h /tmp

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
# Git
#
# ==============================================================================

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

# Все включенные сервисы
$ systemctl list-unit-files | grep enabled

# Просмотр логов в реальном времени
$ journalctl -f

# Изменить размер терминала
$ gnome-terminal --geometry 135x45

# Список установленных шрифтов
$ fc-list

# Обновить базу шрифтов после добавления/удаления их в/из `/usr/share/fonts`
# либо `~/.local/share/fonts`
$ fc-cache -f -v

# Скопировать текст в буфер обмена
$ echo 123 | xclip -sel clip

# Копировать содержимое файла в буфер обмена
$ xclip -sel clip < ~/.ssh/github_rsa.pub

# Вывести содержимое буфера обмена
$ xclip -o -sel clip

# Конвертировать файл в base64 и скопировать в буфер обмена
$ file="test.docx"
$ base64 -w 0 $file  | xclip -selection clipboard

# Генерация пароля
$ yay -S pwgen
$ pwgen -c 10 -s 1
wz1m3gVH5p
```
