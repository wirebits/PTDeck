![PTDeck](https://github.com/user-attachments/assets/e3d7a02c-3419-4c85-bc90-6c3623a00917)

# PTDeck
A powerful 14-key customizable macro pad powered by Raspberry Pi Pico designed for Purple Teaming.

# Key Features
- Minimal Setup.
- Store payloads in folder for better management.
- Executes multiple payloads from single button.

# Hardware Requirements
- Raspberry Pi Pico
- `14` Tacticle Push Buttons
- Male to Male Jumper Wires
- Breadboard

# Connection
- Connect each tacticle push buttons pin to the following GPIO Pins :
  `0`,`1`,`2`,`3`,`4`,`5`,`6`,`7`,`8`,`9`,`10`,`11`,`12`,`13`
- Connect each tacticle push buttons pin to the ground.

# Connection Diagram
![PTDeck Connection Diagram](https://github.com/user-attachments/assets/f5ef53d9-2fc3-45ad-b91a-9dce64e69834)

# Setup of Raspberry Pi Pico
1. Download latest circuit python `.uf2` file for Raspberry Pi Pico from [here](https://circuitpython.org/board/raspberry_pi_pico/).
2. Connect Raspberry Pi Pico with a USB cable.
3. Press and hold the `BOOTSEL` button and then connect to the PC/Laptop.
   - When it connects, then Raspberry Pi Pico W show as a removable storage device named `RPI-RP2`.
   - When `RPI-RP2` is showing, then release the `BOOTSEL` button.
4. Copy the `.uf2` file in the `RPI-RP2`.
   - When it is copied, then it disconnects automatically and reconnect as `CIRCUITPY`.
   - It means circuit python is successfully flashed in the Raspberry Pi Pico.
5. Open `CIRCUITPY`.
   - There are two important things in it : `lib` folder and `code.py` file.
6. Download latest Adafruit CircuitPython Bundle from [here](https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases).
7. Extarct the ZIP file.
8. Go to the `lib` folder in the extracted ZIP file.
9. Copy `adafruit_hid` folder in the `lib` folder of `CIRCUITPY`.
10. Create a folder named `payloads` in `CIRCUITPY`.
11. Done! Now, Raspberry Pi Pico board is ready to use as a PTDeck.

# CIRCUITPY Directory Structure
- **CIRCUITPY/**
  - **lib/**
      - `adafruit_hid`
  - `code.py`
  - `pins.conf`
  - **payloads/**
    - `payload-X.txt`
  - where `X` is a number like `0`,`1`,`2`,`3` etc.

# Install and Run
1. Download or Clone the Repository.
2. Open the folder.
3. Make sure that your Raspberry Pi Pico board is connected to your PC/Laptop.
5. Copy `code.py` and `pins.conf` in the `CIRCUITPY`.
   - It ask for replacement of `code.py` file, then replace it.
   - It will overwrite in the `code.py` file.

# Payload Files
1. Open Notepad or any other text editor.
2. Write your payload in it.
3. When saving the file, select `CIRCUITPY`.
4. Then go to the `payloads` folder.
5. Name the payload as `payload-1`, `payload-2` etc.
   - It is saved by default as `.txt` files.

# CONF File
- It contain `3` variables : `PIN`,`PRESS_COUNT` and `PAYLOAD_COUNT`.
- `PIN` contains pin number of Raspberry Pi Pico.
- There are usable pins in PTDeck are `0`,`1`,`2`,`3`,`4`,`5`,`6`,`7`,`8`,`9`,`10`,`11`,`12`,`13`.
- Replace `PIN_NUMBER` with above values only.
- `PRESS_COUNT` contain how many times the button of that pin pressed.
- Replace `PRESS_COUNT_NUMBER` with values start from `2`.
- `PAYLOAD_COUNT` contains payload number in `payloads` folder.
- Replace `PAYLOAD_NUMBER` with values atarts from `15`.

# Note for CONF File
- Default payload numbers is from `1` to `14`.
- Default press count is `1`.

# Use Case Of CONF File
- If you want to execute payload number `15` by press `2` times on pin number `0`, then conf file is set like :
```
PIN=0
PRESS_COUNT=2
PAYLOAD_COUNT=15
```
- If want to execute payload number `18` by press `3` times on pin number `0` without removing previous configuration, then conf file is set like :
```
PIN=0
PRESS_COUNT=2
PAYLOAD_COUNT=15

PIN=0
PRESS_COUNT=3
PAYLOAD_COUNT=18
```

# Mnemonic Table
| Mnemonics | Description | Example  |
|-----------|-------------|----------|
| WAIT      | It add time in the code.<br>Time is in milliseconds.<br>1000 ms = 1 second. | WAIT 1000 |
| TYPE      | It add text want to type in the code. | TYPE Hello World! |
| LOOP      | It runs commands for a certain number of times.<br> Synatx is `LOOP number-of-times commands` | LOOP 3<br>TYPE Hello World!<br>EXIT<br><br>LOOP 4<br>TAB<br>EXIT<br><br>LOOP 1<br>CTRL S<br>EXIT<br><br>LOOP 1<br>CTRL SHIFT N<br>EXIT<br> |
| INF       | It run commans infinitely.<br>Syntax is `INF commands` | INF<br>TYPE Hello World!<br>EXIT<br><br>INF<br>TAB<br>EXIT<br> |

# Special Symbols
1. `-`
- It is used to put the cursor in the next line.
- It is only used with TYPE.
- Example : `TYPE Hello World!-`
- If TYPE contain any command and then `-` then it run automatically without `ENTER` key.

# Supported Mnemonics
## Alphabet Keys
`A` `B` `C` `D` `E` `F` `G` `H` `I` `J` `K` `L` `M` `N` `O`
`P` `Q` `R` `S` `T` `U` `V` `W` `X` `Y` `Z`
## Function Keys
`F1` `F2` `F3` `F4` `F5` `F6` `F7` `F8` `F9` `F10` `F11` `F12`
## Navigation Keys
`LEFT` `UP` `RIGHT` `DOWN` `TAB` `HOME` `END` `PGUP` `PGDN`
## Lock Keys
`CAPS` `NUM` `SCROLL`
## System and GUI Keys
`GUI` `ESC` `PRTSCR` `PAUSE`
## Editing Keys
`INSERT` `DEL` `BKSP` `ENTER`
## Modifier Keys
`CTRL` `SHIFT` `ALT`
## ASCII Characters
`` ` `` `!` `@` `#` `$` `%` `^` `&` `*` `(` `)` `-` `=` `[` `]` `\` `;` 
`'` `,` `.` `/` `SPACE` `~` `_` `+` `{` `}` `|` `:` `"` `<` `>` `?` `0`
`1` `2` `3` `4` `5` `6` `7` `8` `9`

# Examples
## Open notepad and type Hello World!

```
WAIT 1000
GUI R
WAIT 1000
TYPE notepad
WAIT 1000
ENTER
WAIT 1000
TYPE Hello World!
```
## Open CMD as Administrator Mode

```
WAIT 1000
GUI R
WAIT 1000
TYPE cmd
WAIT 1000
CTRL SHIFT ENTER
WAIT 1300
ALT Y
```
## Create A New Folder
```
WAIT 1000
CTRL SHIFT N
WAIT 1200
TYPE hello
WAIT 1100
ENTER
```
## Open notepad and type Hello World! 6 times in different lines
```
WAIT 1000
GUI R
WAIT 1000
TYPE notepad
WAIT 1000
ENTER
WAIT 1000
LOOP 6
TYPE Hello World!-
EXIT
```
