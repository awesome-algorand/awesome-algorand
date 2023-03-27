# genpyteal

Converts Python to PyTeal. Your mileage will vary depending on how much you deviate from the examples.
Its quite easy to get an error by doing something not supported.  However, it often still outputs useful PyTeal that you can then
fix up.

If you appreciate this tool, you are welcome to send ALGOs to `RMONE54GR6CYOJREKZQNFCZAUGJHSPBUJNFRBTXS4NKNQL3NJQIHVCS53M`.
## Installation

`pip3 install genpyteal` or `pip install genpyteal`

### ABI 


As of this writing, if you use any ABI stuff, you will need to uninstall regular pyteal and do this:
`pip install -e git+https://github.com/algorand/pyteal@abi-types#egg=pyteal`

`b67a71a224eb1b8c477ae32b5c4d0ab01a680edb`

*Warning*: The scripts have `python3` in them because that is what works on my system. It only works with Python 3. 
There might be some system where it needs to say `python` instead.  If so, maybe just pull the code from the github repo to change it?

## Usage

To generate PyTeal:

`genpyteal thescript.py`

To generate PyTeal and do syntax highlighting (requires `pygmentize` and `boxes` to be installed):

`genpyteal thescript.py | niceout`

To generate PyTeal and then TEAL:

`genteal thescript.py`

To show the AST (FST) of a Python program (uses RedBaron .help(), and requires `ipython` installed):

`showast thescript.py`

## Supported constructs

`statement list` (= Seq), `integer const` ( = Int(n)), `if/else`, `while`, `print` (= `Log`), `+` ( = Concat(str1, str2) ), 
`True/False` (= 1/0), `and/or/not` ...
(maybe something I am forgetting).

## Details

You can use a subset of Python. For scratch variables, you will need to initialize them at the beginning of a function, such as `x = 0` or `s = "tom"`. It uses 
that to determine the type. Sometimes you may need to specify Bytes or Int still. Integer/string literals get Int/Bytes added automatically. You can use `print` instead of Log. 

Name the main function `app` to indicate a stateful application contract, or `sig` for a LogicSig contract.

For transaction fields, you can leave off the parenthesis, e.g. `Txn.sender` instead of `Txn.sender()`.

It will assume functions return `uint64` unless you specify `@bytes` or there is no return, which will automatically insert `@Subroutine(TealType.none)`

If you want to print a number in the log, you can use the numtostr function I made:

```python
from lib import util

def app():
  print("Your number is " + util.numtostr(100))

```

The best explanation is just to show the examples.

## Examples

## examples/abiadv.py 

```python
from lib.util import *

JUNK_ASSET = 575753250

fgGreen = "\033[38;5;2m"
fgYellow = "\033[38;5;11m"
fgPurple = "\033[38;5;35m"
fgWhite = "\033[38;5;15m"
fgRed = '\033[38;5;31m'
bgWhite = '\033[48;2;250;250;250m'
bgRed = '\033[48;2;250;0;0m'
resetColor = "\033[0m\033[48;2;0;0;0m"

yard = "Front Yard\nYou are standing in front of a house. It is white, with green trim."
yard_connects = "NL"
yard_conn_descr = "To the north is the front door."

living_room = """Living Room
This is a small living room with a carpet that should have been replaced 15 years ago. There is a beat-up couch to sit on."""
living_room_connects = "ESSYWD"
living_room_conn_descr = """From here you can enter the study to the east, the dining room (west), or go back outside (south)."""

study = """Study
There is an Ohio Scientific computer here from the late 1970s. A rickety bookshelf contains some old Dungeons & Dragons books."""
study_connects = "WL"
study_conn_descr = "To the west is the living room."  

dining = """Dining Room
This is a small area with an old wooden table taking up most of the space. The layers of stains on the carpet are truly breathtaking.
There is a merchant here. He has his goods spread out on the table."""
dining_connects = "EL"
dining_conn_descr = "To the east is the living room."

computer = """The screen shows the following:
\033[38;2;138;226;52m\033[48;2;0;21;0m
A>dir                             
A: MOVCPM   COM  
A: ASMAVM   COM  
A: CHIP8    COM  
\033[0m
"""

note = """
Welcome to 'Mini-Adventure'. For a list of commands, type /menu.
You probably already knew that though, or you would not have got to this point.
"""

sign = """
\033[38;5;2mSale!
Only 0.02 ALGO per item\033[0m

To buy an item (if using the 'avmloop' client), enter the following command:
\033[38;2;138;226;52m\033[48;2;0;21;0m
> /optin 23423423,/pay 0.02,buy junk\033[0m
"""

@bytes
def get_connects(l):
  if l == 'Y': return yard_connects
  if l == 'L': return living_room_connects
  if l == 'S': return study_connects
  if l == 'D': return dining_connects
  return ''

def move_(location, direction):
  connects = ""
  connects = get_connects(location)
  i = 0
  l = 0
  d = 0
  print("Trying to move " + direction)
  while i < Len(connects):
    if Extract(connects, i, 1) == direction:
      lput('location', Extract(connects, i + 1, 1))
      d = show(lgets('location'))
      return True
    i = i + 2
      
  return False

def printloc(descr, conn_descr, connects):
  print(fgWhite)
  print(descr)
  
  print(fgYellow)
  print(conn_descr)

  show_at_location_()
  
  print(fgGreen)
  print(connects)

  print(resetColor)

def show(l):
  if l == 'Y': printloc(yard, yard_conn_descr, yard_connects)    
  if l == 'L': printloc(living_room, living_room_conn_descr, living_room_connects)
  if l == 'S': printloc(study, study_conn_descr, study_connects)
  if l == 'D': printloc(dining, dining_conn_descr, dining_connects)
  return 1

def show_inventory_():
  inv = StringArray(lgets('inventory'))
  print("You are carrying:")
  print(fgYellow)

  if lgeti('junk_count') > 0:
    print(numtostr(lgeti('junk_count')) + ' Garage Sale Junk')
  
  inv.init()
  i = 0 
  while i < inv.size:
    print(abi.String(inv[i]).value)
    i = i + 1
  print(resetColor)
  return 1

def show_junk():    
  print(numtostr( asset_bal(app_address, 0)) + " Garage Sale Junk")

def show_at_location_():
  items = StringArray(ggets(lgets('location') + '_items'))
  items.init()
  if items.size == 0:
    n = 0
  else:
    print('You see the following items here:')
    print(fgPurple)
    
    i = 0 
    while i < items.size:
      print(abi.String(items[i]).value)
      i = i + 1
    
  print(resetColor)

def printitem(i):
  print(fgWhite)
  if i == 'computer': print(computer)
  if i == 'note': print(note)
  if i == 'sign': print(sign)
  print(resetColor)

def exists_item(item, loc):
  if loc == 'S' and (item == 'computer' or item == 'books'):
    return True
  if loc == 'D' and item == 'sign':
    return True
  if item == 'note':
    return True
  return False

def rolld20():
  return rnd(1, 20)

def examine_(i):
  if exists_item(i, lgets('location')):    
    printitem(i)
  else:
    s = ""
    s = i
    s = "There is no " + s
    s = s + " here."
    print(s)
  return 1

def encounter():
  print('A')
  print(Concat(fgRed, clr('Bitcoin Maximalist ', bgWhite), fgRed, resetColor))
  print('suddenly appears. He attacks you with')
  print(Concat(clr('Nonsense', fgRed), resetColor))
  print('and runs away.')
  print(Concat(clr('You lose [10] hit points', bgRed), fgWhite, resetColor)) 
  return 1

def buy_(asset, what):  
  if find_payment(20000):
    Begin()
    SetFields({
      TxnField.type_enum: TxnType.AssetTransfer,
      TxnField.sender: app_address,
      TxnField.asset_amount: 1,
      TxnField.asset_receiver: Txn.sender,
      TxnField.xfer_asset: Txn.assets[Btoi(asset)]
    })
    Submit()
    print("You bought it.")
    lput('junk_count', asset_bal(Txn.sender, 0))
    return 1
  return 0

def find_payment(amount):
  i = 0
  found = 0
  while i < Global.group_size:
    if (Gtxn[i].sender == Txn.sender and 
        Gtxn[i].receiver == Global.current_application_address and 
        Gtxn[i].amount == amount):
      found = True
    i = i + 1
      
  return found

def find_axfer(assetid):
  i = 0
  found = 0
  while i < Global.group_size:
    if (Gtxn[i].asset_id == assetid and 
        Gtxn[i].asset_receiver == Global.current_application_address and 
        Gtxn[i].asset_amount == 1):
      found = True
    i = i + 1
      
  return found
  
def offer_(asset, what):
  if what == "junk":
    Begin()
    SetFields({
      TxnField.type_enum: TxnType.AssetTransfer,
      TxnField.sender: Global.current_application_address,
      TxnField.asset_amount: 0,
      TxnField.asset_receiver: Global.current_application_address,
      TxnField.xfer_asset: Txn.assets[asset]
    })
    Submit()   
    print("The merchant will take your junk.")
    return 1
  return 0

def use_(item:bytes):
  if arr_find(lgets('inventory'), item) == NOT_FOUND:
    print('You are not carrying that.')
    return 1

  if item == 'die' or item == 'dice' or item == 'd20':
    print("Rolling d20...")
    print(fgYellow)
    roll = 0
    roll = rolld20()
    print("[ " + numtostr(roll) + " ]")
    print(resetColor)
    if roll < 10:
      return encounter()
  else:
    print("You can't use that.")
  return 1
  
def take_(what:TealType.bytes):
  inv = StringArray(lgets('inventory'))
  ind = 0
  ind =  arr_find(ggets(lgets('location')+'_items'), what)
  if ind == NOT_FOUND:
    print('You do not see that here, or it is not something you can take.')
  else:  
    inv.init()
    inv.append(abi.String.encode(what))
    lput('inventory', inv.serialize())
    gput(lgets('location')+'_items', arr_del(ggets(lgets('location')+'_items'), ind))
    
    print('You take the ' + what)
  return 1

def drop_(what:TealType.bytes):
  items = StringArray(ggets(lgets('location') + '_items'))
  ind = 0
  ind = arr_find(lgets('inventory'), what) 
  if ind == NOT_FOUND:
    print('You are not carrying that.')
  else:
    lput('inventory', arr_del(lgets('inventory'), ind))
    items.init()
    items.append(abi.String.encode(what))
    print('You dropped the ' + what)
    gput(lgets('location')+'_items', items.serialize())    
  return 1
  
def init_local_array(name):
  strarr = StringArray("")
  strarr.init()
  if name == 'inventory':
    strarr.append(abi.String.encode('note'))
  
  lput(name, strarr.serialize())

def init_global_array(name, df):
  strarr = StringArray("")
  strarr.init()
  if df != '':
    strarr.append(abi.String.encode(df))
  #if name == 'S_items':
  #  strarr.append(abi.String.encode('d20'))
  #if name == 'D_items':
  #  strarr.append(abi.String.encode('sign'))

  gput(name, strarr.serialize())


def setup_():
  lput('location', 'Y')
  lput('junk_count', 0)
  init_local_array('inventory')
  init_global_array('Y_items', '')
  init_global_array('L_items', '')
  init_global_array('S_items', 'd20')  
  init_global_array('D_items', 'sign')
  
  return 1

def look() -> abi.Uint32:
  return show(lgets('location'))

def setup() -> abi.Uint32:
  return setup_()

def move(dir: String) -> abi.Uint32:
  return move_(lgets('location'), abi.String(dir).value)

def take(what: String) -> abi.Uint32:
  return take_(abi.String(what).value)

def drop(what: String) -> abi.Uint32:
  return drop_(abi.String(what).value)

def inventory() -> StringArray:
  return lgets('inventory')

def examine(what: String) -> abi.Uint32:
  return examine_(abi.String(what).value)

def use(item: String) -> abi.Uint32:
  return use_(abi.String(item).value)

def buy(optin, pay, asset, item: String ) -> abi.Uint32:
  return buy_(asset, abi.String(item).value)    

def offer(asset, item: String) -> abi.Uint32:
  return offer_(asset, abi.String(item).value)    
```
## examples/bool.py 

```python
def app():
  amt = 15
  return amt > 10 and amt < 20 or amt == 0
```
## examples/callscratch.py 

```python
def g(x):
    return 3

def f(n):
    return g(n)

def app():
    x = f(30)
    name = "Bob"
    print(name)
    return 100
```
## examples/checkgroup.py 

```python
PAYTO = Addr('6ZHGHH5Z5CTPCF5WCESXMGRSVK7QJETR63M3NY5FJCUYDHO57VTCMJOBGY')
FEE = 10 * 1000000
ZERO = Global.zero_address()

def no_close_to(i):
  Assert( Gtxn[i].close_remainder_to == ZERO )

def no_rekey(i):
  Assert( Gtxn[i].rekey_to == ZERO )

def verify_payment(i):
  Assert( Gtxn[i].receiver == PAYTO and
          Gtxn[i].amount == Int(FEE) and
          Gtxn[i].type_enum == TxnType.Payment )
         
def app():
  Assert( Global.group_size == 2 )
  
  no_close_to(1)
  no_rekey(1)

  verify_payment(1)

  App.globalPut('lastPaymentFrom', Gtxn[1].sender)
  Approve()
```
## examples/ifseq.py 

```python

def foo(b):
  x = b

def app():
  foo(10)
  if 1 == 1:
    return 1
  else:
    return 0
```
## examples/inner.py 

```python

def pay(amount: uint64, receiver: bytes):
    Begin()
    SetFields({
        TxnField.type_enum: TxnType.Payment,
        TxnField.sender: Global.current_application_address,
        TxnField.amount: amount,
        TxnField.receiver: receiver
        })
    Submit()

def app():
    pay(10, Addr('6ZHGHH5Z5CTPCF5WCESXMGRSVK7QJETR63M3NY5FJCUYDHO57VTCMJOBGY'))
    result = 0
    if Txn.first_valid > 1000000:
        result = 1
    return result

```
## examples/strargs.py 

```python
def app():
  name = ""
  name = Txn.application_args[0]
  age = Btoi(Txn.application_args[1])
  if age > 65:
    print("User " + name + " is at retirement age.")
    return 1
  else:
    print("User " + name + " is still young.")
    return 0
```
## examples/swap.py 

```python
"""Atomic Swap"""

alice = Addr("6ZHGHH5Z5CTPCF5WCESXMGRSVK7QJETR63M3NY5FJCUYDHO57VTCMJOBGY")
bob = Addr("7Z5PWO2C6LFNQFGHWKSK5H47IQP5OJW2M3HA2QPXTY3WTNP5NU2MHBW27M")
secret = Bytes("base32", "2323232323232323")
timeout = 3000
ZERO_ADDR = Global.zero_address()

def sig(
    tmpl_seller=alice,
    tmpl_buyer=bob,
    tmpl_fee=1000,
    tmpl_secret=secret,
    tmpl_hash_fn=Sha256,
    tmpl_timeout=timeout,
):
    fee_cond = Txn.fee < Int(tmpl_fee)
    is_payment = Txn.type_enum == TxnType.Payment
    no_closeto = Txn.close_remainder_to == ZERO_ADDR
    no_rekeyto = Txn.rekey_to == ZERO_ADDR
    safety_cond = is_payment and no_rekeyto and no_closeto
    
    recv_cond = (Txn.receiver == tmpl_seller) and (tmpl_hash_fn(Arg(0)) == tmpl_secret)
    esc_cond = (Txn.receiver == tmpl_buyer) and (Txn.first_valid > Int(tmpl_timeout))

    return (fee_cond and safety_cond) and (recv_cond or esc_cond)
```
## examples/usenumtostr.py 

```python
from lib import util

def app():
  print("The best number is " + util.numtostr(42))
  return True
```
## examples/usestrarr.py 

```python
from lib.util import *

def show_inventory_():
  inv = StringArray(lgets('inventory'))
  inv.init()
  i = 0  
  while i < inv.size:
    print(abi.String(inv[i]).value)
    i = i + 1
  return 1

def pickup_(item):
  inv = StringArray(lgets('inventory'))
  inv.init()
  inv.append(item)
  lput('inventory', inv.serialize())
  return show_inventory_()

def init_():
  inv = StringArray("")
  inv.init()
  lput('inventory', inv.serialize())
  return 1
  
def init() -> abi.Uint32:
  return init_()

def get_inventory() -> StringArray:
  return lgets('inventory')

def pickup(item: String) -> abi.Uint32:
  return pickup_(item)

def show_inventory() -> abi.Uint32:
  return show_inventory_()

```
## examples/whilecallif.py 

```python
from lib.util import *

def proc(n):
  return n * 2

def acceptable(n, target):
  if n >= target:
    print("Acceptable. Diff is " + numtostr(n - target))
    return True
  else:
    return False


def app():
  total = 1
  i = 0
  while not acceptable(total, Btoi(Txn.application_args[0])):
    total = proc(total)
    i += 1
  return i
```
## examples/whilesum.py 

```python
def app():  
  totalFees = 0
  i = 0
  while i < Global.group_size:
    totalFees = totalFees + Gtxn[i].fee
    i = i + 1
  return 1
```

## lib/util.py
```python
from typing import Tuple

from pyteal import *

from pytealutils import abi

from .libex import *

StringArray = abi.DynamicArray[abi.String]

NOT_FOUND = Int(999)

asset = abi.Uint8
account = abi.Uint8
application = abi.Uint8

@bytes
def clr(s, ansi):
  return Concat(ansi, s)

def arr_find(str_arr_bytes:bytes, item:bytes):
  str_arr = StringArray(str_arr_bytes)
  str_arr.init()
  i = 0
  while i < str_arr.size.load():
    if str_arr[i] == abi.String.encode(item):
      return i
    i = i +1
  return NOT_FOUND

@bytes
def arr_del(str_arr_bytes, index_to_remove):
  str_arr = StringArray(str_arr_bytes)
  new_arr = StringArray("")
  new_arr.init()
  str_arr.init()
  i = 0
  while i < index_to_remove:
    new_arr.append(str_arr[i])
    i = i + 1
  i = i + 1
  while i < str_arr.size.load():
    new_arr.append(str_arr[i])
    i = i + 1
  return new_arr.serialize()

def rnd(min_, max_):
  hash_ = ""
  rndcnt = 0
  rndcnt = App.globalGet('rndcnt')
  hash_ = Sha256(Concat(Txn.tx_id, Itob(Global.latest_timestamp)))  
  bigRand = Btoi(Extract(hash_ ,rndcnt, 7)) + Global.latest_timestamp % 100000
  rndcnt = rndcnt + 1
  App.globalPut('rndcnt', rndcnt)
  return min_ + bigRand % (max_ - min_ + 1)

@bytes
def numtostr(num):
  out = "             "
  i = 0
  digit = 0
  n = num
  done = False
  while not done:
    digit = n % 10
    out = SetByte(out, 12-i, digit+48)
    n = n / 10		
    if n == 0: done = True
    i = i + 1
  return Extract(out, 12 - i + Int(1), i)


```
