# Documentation

The base class.

param email

  - : Your Tuya account email. (Account will be created if it doesn't  
    exist)

param password

: Your Tuya account password

returns

: A TuyaAPI instance. (Used for TuyaDevice() class)

requestapi(command, data, needsid = False)

Make a request to the Tuya API.

param command

  - The API command. ex  
    tuya.m.device.list

param data

: API postData. (dictionary)

param needsid

  - : Whether or not the command requires a valid user login. (All
    methods  
    but login() require True)

returns

: API response as dictionary

requestdev(data)

Make a request to a device to setup.

param data

: Data to be sent

returns

: None

login()

Log the user in. (Called automatically in \_\_init\_\_ of class. Only
call after call of logout())

returns

: None

logout()

Log the user out.

returns

: None

gentok()

Generate a new device token. (Used when setting up a new device)

returns

  - dictionary  
    {'token': token, 'secret': secret}

Return Values

:

\> - **token** - Generated token \> - **secret** - Token secret

setupdev(ssid, password, token, secret)

Set up a device that is in AP setup mode. (Must be connected to devices
AP. SSID usually looks something like "SmartLife\_xxxx")

param ssid

: The SSID of the WiFi network the device should connect to

param password

: The password of the WiFi network the device should connect to

param token

: A device token. (Get by calling gentok())

param secret

: That tokens secret. (Get by calling gentok())

returns

: None

ldevbytok(token)

Get the id of the device tied to a token.

param token

: The token to check

returns

: Device ID tied to token

ldevbyuser()

List users devices.

returns

  - array  
    \[{'devid': devid, 'sws': sws, 'name': name}\]

Return Values

:

\> - **devid** - Device ID \> - **sws** - Number of switches on device
\> - **name** - Device name

getsws(devid)

Get number of switches on device.

param devid

: Device ID

returns

: Number of switches on device

getdevname(devid)

Get device name.

param devid

: Device ID

returns

: Device's name

setdevname(devid, name)

Set device name.

param devid

: Device ID

param name

: New name

returns

: None

getdps(devid)

Get device status.

param devid

: Device ID

returns

  - dictionary  
    {swid: state}

Return Values

:

\> - **swid** - Switch ID \> - **state** - Switch State

setdps(devid, dps)

Set device status.

param devid

: Device ID

param dps

  - Status. (ex  
    {'1': True})

returns

: None

Represents a Tuya device.

param tapi

: An instance of TuyaAPI()

param devid

: Device ID

returns

: None

getsws()

Get number of switches on device.

returns

: Number of switches on device.

getname()

Get the device name.

returns

: Device's name

setname(name)

Set the device name.

param name

: New name

returns

: None

getstate(swid = 1)

Get device state.

param swid

: Switch ID

returns

: Switch state

setstate(state, swid = 1)

Set device state.

param state

: State

param swid

: Switch ID

returns

: None
