# Vax the Sat

I couldn't resist the [Vax the Sat](https://quals.2020.hackasat.com/scoreboard/challenge/20) there is just something about obsolete computer architectures. Unfortunately, we didn't quite finish this one in time for the live challenge, but the organizers left the system running so we were able to complete this challenge after the qualifiers ended.

The problem description takes us back to the 1970s and asks us to find the flag:

> It's still the 70's in my ground station network, login to it and see if you can get a flag from it.

After downloading the challenge files, we ended up with a *server.s* disassembly file, probably from running objdump from a VAX gcc toolchain and a VaxtheSAT.md file with additional info:

> # VAXtheSAT
>
> ## Mission overview
> Your mission is to hijack a satellite by pointing it to *34.916944*, *-117.376667*, an abandoned USAF radio station in the middle of the desert.
>
> You have obtained access to a client machine in the ground station, which conveniently has a post-it note on it with the following useful information:
>
> ```
> login: root
> Password: vaxthesat!
> ```
>
> ## Network configuration
> Machines in the base station communicate through an internal network. You own a client machine on this network, but you need to connect to the server that actually communicates with the satellite.
>
> ```
> .--.                 .--.                                     }-O-{
> |__| .--------.      |__| .--------.      ,--..Y   ) ) )       [^]
> |=.| |.------.|      |=.| |.------.|      \   /`.        _____/o o\_____
> |--| ||CLIENT|| <--> |--| ||SERVER|| <-->  \.    \      ^""""":{o}:"""""^
> |  | |'------'|      |  | |'------'|       |"""--'             /.\
> |__|~')______('      |__|~')______('       / \                 \_/
>      10.0.0.21            10.0.0.20
> ```
>
> There is a client program on the client machine. Just type ***client***.
>
> ## Resources
> Ressources are available on the client machine in the directory ***/root/client/***
>
> You have obtained the server disassembly from a trustworthy source: [link to server.s].

Seems pretty basic right? We are given a foothold on a network, provided the client used to talk to the server that commands the satellite. Just have to figure out how to enter a coordinate to point the satellite at. How hard could that be? Oh, yea there is that VAX assembly file...

## Information Gathering  

We have a user credentials, network diagrams, and instructions on running the client. Let's go connect and see what we can see! We connect to the host and start seeing a log of OpenBSD booting:

```
~/D/C/H/Vax the Sat> nc vax.satellitesabove.me 5035
Ticket please:
ticket{xxxxxxxxxxx}
DEBUG:vax_common.vax_base:Challenge id: 51

VAX simulator V3.9-0
NVR: buffering file in memory
Eth: opened OS device lo
sh: 1: ifconfig: not found
sh: 1: ifconfig: not found
XQ, address=20001920-2000192F*, vector=250, MAC=AA:00:04:00:15:04, type=DELQA-T,mode=DELQA, poll=100, attached to lo

^[[?1;2c
KA655X-B V5.3, VMB 2.7
Performing normal system tests.
40..39..38..37..36..35..34..33..32..31..30..29..28..27..26..25..
24..23..22..21..20..19..18..17..16..15..14..13..12..11..10..09..
08..07..06..05..04..03..
Tests completed.
Loading system software.
(BOOT/R5:0 DUA0



  2..
-DUA0
  1..0..


>> OpenBSD/vax boot [1.18] <<
>> Press enter to autoboot now, or any other key to abort: 0
> boot bsd
1984796+422624 [72+135984+120043]=0x28a5fc
[ using 256512 bytes of bsd ELF symbol table ]
Copyright (c) 1982, 1986, 1989, 1991, 1993
	The Regents of the University of California.  All rights reserved.
Copyright (c) 1995-2015 OpenBSD. All rights reserved.  http://www.OpenBSD.org

OpenBSD 5.8 (GENERIC) #117: Sun Aug 16 06:42:12 MDT 2015
    deraadt@vax.openbsd.org:/usr/src/sys/arch/vax/compi
...
Copying files for vaxthesat challenge
/root/client/CLIENT was renamed to /root/client/client
/root/client/CLIENT.S was renamed to /root/client/client.s
/root/client/SERVER was renamed to /root/client/server
/root/client/SERVER.S was renamed to /root/client/server.s


Directories and files with new names in lowercase letters
/root/client/server
/root/client/server.s
/root/client/client
/root/client/client.s
/root/client
...
login: root
root
Password:vaxthesat!

Last login: Wed May  6 22:14:14 on console
OpenBSD 5.8 (GENERIC) #117: Sun Aug 16 06:42:12 MDT 2015

Welcome to OpenBSD: The proactively secure Unix-like operating system.

Please use the sendbug(1) utility to report bugs in the system.
Before reporting a bug, please try to reproduce it with the latest
version of the code.  With bug reports, please try to ensure that
enough information to reproduce the problem is enclosed, and if a
known fix for it exists, include that as well.

You have mail.
#                                                                       
```

Nice, we are logged into the compromised client as root! And the challenge logged that it copied both the server and the client programs and disassembles of them both to /root/client/. We should have noted the importance of having the binaries right now... but we were sleep deprived and it wasn't until after the challenge finished that we realized we could use them to debug our attacks...

Ok, lets run the client app and connect to the sever and see what is there:

```
# client 10.0.0.20                                                      
client 10.0.0.20
Socket successfully created.
connected to the server..
##############################################################################
#                # RSSI -80dBm               .-"-.         #                 #
# EPS STAT:  [1] #                          /     \        # OBC STAT:  [1]  #
#   COM  PWR [*] #                 }--O--{  |#    |        #                 #
#   OBC  PWR [*] #                   [^]     \___/         #                 #
#   ADCS PWR [ ] #                  /ooo\     ^\           #                 #
#                #  ______________:/o   o\:_____)________  #                 #
#                # |=|=|=|=|=|=|:A|":|||:"|A:|=|=|=|=|=|=| #                 #
#                # ^--------------!::{o}::!--------------^ #                 #
# COM STAT:  [1] #                 \     / /               # ADCS STAT: [3]  #
#                #       ____       \.../ )     ____       #                 #
#                #      |\/\/|=======|*|=======|\/\/|      #                 #
#                #      :----"       /-\       "----:      #                 #
#                #                  /ooo\                  #                 #
#                #                 #|ooo|#                 #                 #
#                #                  \___/                  #                 #
#                # LAT: 38.897789      LONG: -77.036301    #                 #
##############################################################################
# HELP  ADCS RST  ADCS NOOP  ADCS STATE  ADCS CFG  ADCS CFG_POS  EPS RST     #
# EPS NOOP  EPS STATE  EPS CFG COM RST COM NOOP COM STATE  OBC RST  OBC NOOP #
# INFO:                                                                      #
# ERROR:                                                                     #
##############################################################################
COMMAND $ 
```

Nice! We have a pretty nifty ASCII UI! It even has help!

### Help

Lets see what help gets us:

```
COMMAND $ help
##############################################################################
#                # RSSI -80dBm               .-"-.         #                 #
# EPS STAT:  [1] #                          /     \        # OBC STAT:  [1]  #
#   COM  PWR [*] #                 }--O--{  |#    |        #                 #
#   OBC  PWR [*] #                   [^]     \___/         #                 #
#   ADCS PWR [ ] #                  /ooo\     ^\           #                 #
#                #  ______________:/o   o\:_____)________  #                 #
#                # |=|=|=|=|=|=|:A|":|||:"|A:|=|=|=|=|=|=| #                 #
#                # ^--------------!::{o}::!--------------^ #                 #
# COM STAT:  [1] #                 \     / /               # ADCS STAT: [3]  #
#                #       ____       \.../ )     ____       #                 #
#                #      |\/\/|=======|*|=======|\/\/|      #                 #
#                #      :----"       /-\       "----:      #                 #
#                #                  /ooo\                  #                 #
#                #                 #|ooo|#                 #                 #
#                #                  \___/                  #                 #
#                # LAT: 38.897789      LONG: -77.036301    #                 #
##############################################################################
# HELP  ADCS RST  ADCS NOOP  ADCS STATE  ADCS CFG  ADCS CFG_POS  EPS RST     #
# EPS NOOP  EPS STATE  EPS CFG COM RST COM NOOP COM STATE  OBC RST  OBC NOOP #
# INFO:                                                                      #
# ERROR: BAD CHARACTER                                                       #
##############################################################################
COMMAND $
```

Oops! Guess we are case sensitive... Lets try that again:

```
COMMAND $ HELP
##############################################################################
#                # RSSI -80dBm               .-"-.         #                 #
# EPS STAT:  [1] #                          /     \        # OBC STAT:  [1]  #
#   COM  PWR [*] #                 }--O--{  |#    |        #                 #
#   OBC  PWR [*] #                   [^]     \___/         #                 #
#   ADCS PWR [ ] #                  /ooo\     ^\           #                 #
#                #  ______________:/o   o\:_____)________  #                 #
#                # |=|=|=|=|=|=|:A|":|||:"|A:|=|=|=|=|=|=| #                 #
#                # ^--------------!::{o}::!--------------^ #                 #
# COM STAT:  [1] #                 \     / /               # ADCS STAT: [3]  #
#                #       ____       \.../ )     ____       #                 #
#                #      |\/\/|=======|*|=======|\/\/|      #                 #
#                #      :----"       /-\       "----:      #                 #
#                #                  /ooo\                  #                 #
#                #                 #|ooo|#                 #                 #
#                #                  \___/                  #                 #
#                # LAT: 38.897789      LONG: -77.036301    #                 #
##############################################################################
# HELP  ADCS RST  ADCS NOOP  ADCS STATE  ADCS CFG  ADCS CFG_POS  EPS RST     #
# EPS NOOP  EPS STATE  EPS CFG COM RST COM NOOP COM STATE  OBC RST  OBC NOOP #
# INFO: USAGE: HELP [TOPIC]                                                  #
# ERROR:                                                                     #
##############################################################################
```

Working now... We now ran **HELP** on all the commands and will spare you the outputs. The following commands had useful help strings:

```
ADCS STATE [ACTIVE/CONFIG/DISABLED]
ADCS CFG_POS [4 BYTES LAT] [4 BYTES LON] [16 BYTES CHECKSUM]
EPS STATE [ACTIVE/CONFIG/DISABLED]
EPS CFG [ADCS/COM/OBC] [ON/OFF]
COM STATE [ACTIVE/CONFIG/DISABLED]
```

### Setting the ADCS CFG_POS

From the help strings, it is clear we need to call the **ADCS CFG_POS**. Let's try it and see what happens. It looks like we also have to specify bytes rather than floats for the LAT and LON, so just going to assume we need to supply the packed float values as a HEX string. May as well try to point it at the coordinates from the README, *34.916944*, *-117.376667*:

```
COMMAND $ ADCS CFG_POS F3AA0B42 DAC0EA42 AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
##############################################################################
#                # RSSI -80dBm               .-"-.         #                 #
# EPS STAT:  [1] #                          /     \        # OBC STAT:  [1]  #
#   COM  PWR [*] #                 }--O--{  |#    |        #                 #
#   OBC  PWR [*] #                   [^]     \___/         #                 #
#   ADCS PWR [ ] #                  /ooo\     ^\           #                 #
#                #  ______________:/o   o\:_____)________  #                 #
#                # |=|=|=|=|=|=|:A|":|||:"|A:|=|=|=|=|=|=| #                 #
#                # ^--------------!::{o}::!--------------^ #                 #
# COM STAT:  [1] #                 \     / /               # ADCS STAT: [3]  #
#                #       ____       \.../ )     ____       #                 #
#                #      |\/\/|=======|*|=======|\/\/|      #                 #
#                #      :----"       /-\       "----:      #                 #
#                #                  /ooo\                  #                 #
#                #                 #|ooo|#                 #                 #
#                #                  \___/                  #                 #
#                # LAT: 38.897789      LONG: -77.036301    #                 #
##############################################################################
# HELP  ADCS RST  ADCS NOOP  ADCS STATE  ADCS CFG  ADCS CFG_POS  EPS RST     #
# EPS NOOP  EPS STATE  EPS CFG COM RST COM NOOP COM STATE  OBC RST  OBC NOOP #
# INFO:                                                                      #
# ERROR: ADCS ERROR                                                          #
##############################################################################
COMMAND $
```

Hmm... ADCS ERROR... that is not a very helpful error, but if we have learned anything from these challenges, it is that when doing mission control changes there is a procedure to do things. First take care of power and then ensure the satellite is in the proper state to accept the command you are trying to execute. We can see in the upper left under *EPS STAT* that there are a number of power options and `ADCS PWR [ ]` doesn't have a mark. Probably the ADCS unit is powered down.

After some trial and error we came up with the following commands to power up the ADCS system and put it into a state to accept an **ADCS CFG_POS** command:

```
EPS STATE CONFIG
EPS CFG ADCS ON
EPS STATE ACTIVE
ADCS STATE CONFIG
```

After running those commands we get the following status screen:

```
##############################################################################
#                # RSSI -80dBm               .-"-.         #                 #
# EPS STAT:  [1] #                          /     \        # OBC STAT:  [1]  #
#   COM  PWR [*] #                 }--O--{  |#    |        #                 #
#   OBC  PWR [*] #                   [^]     \___/         #                 #
#   ADCS PWR [*] #                  /ooo\     ^\           #                 #
#                #  ______________:/o   o\:_____)________  #                 #
#                # |=|=|=|=|=|=|:A|":|||:"|A:|=|=|=|=|=|=| #                 #
#                # ^--------------!::{o}::!--------------^ #                 #
# COM STAT:  [1] #                 \     / /               # ADCS STAT: [2]  #
#                #       ____       \.../ )     ____       #                 #
#                #      |\/\/|=======|*|=======|\/\/|      #                 #
#                #      :----"       /-\       "----:      #                 #
#                #                  /ooo\                  #                 #
#                #                 #|ooo|#                 #                 #
#                #                  \___/                  #                 #
#                # LAT: 38.897789      LONG: -77.036301    #                 #
##############################################################################
# HELP  ADCS RST  ADCS NOOP  ADCS STATE  ADCS CFG  ADCS CFG_POS  EPS RST     #
# EPS NOOP  EPS STATE  EPS CFG COM RST COM NOOP COM STATE  OBC RST  OBC NOOP #
# INFO: ACDS STATE OK                                                        #
# ERROR:                                                                     #
##############################################################################
```

ADCS is powered up `ADCS PWR [*]` and its status is in config mode `ADCS STAT: [2]`! Now lets give setting a position a try:

```
COMMAND $ ADCS CFG_POS F3AA0B42 DAC0EA42 AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
<delay, then disconnected...>
```

No go, although rather than getting an error we had a short delay and then was disconnected from the sever. We just assumed that we had successfully invoked the command and the server didn't like our checksum and disconnected us...  So we connected again, went through the process and used a slightly different **ADCS CFG_POS** command and got an **ADCS ERROR** message. So we shrugged off the unusual behavior of delaying after sending the command. We would come to severely regret this oversight later on... But that is for later on, next up is reverse engineering the checksum.

## Reverse Engineering

Having enumerated the UI we moved onto reverse engineering the *server.s* file. Ideally we would use a disassembler, such as [IDA Pro](https://www.hex-rays.com), but IDA does not support VAX, so unfortunately we were stuck with just the text disassembly. Thankfully, the challenge creators did not strip the binary, so the names of the function were preserved in the disassembly.

### VAX Review

First off, a quick review of the VAX architecture, which really is not too hard to understand. Anyone familiar with x86 (32-bit) should have no problem reading and understanding VAX.

**Registers**

VAX has 15 32-bit registers and a status register, four of those registers have special purposes:

* **R0-R11** - General purpose registers
* **AP (R12)** - Argument Pointer, points to the base of the function's arguments. Unlike x86 where both the arguments and the local stack frame are referenced from *ebp*, VAX uses *AP/R12* for the references. It does make it easy to identify arguments vs local variables!
* **FP(R13)** - Frame Pointer, the base of the function's local variables on the stack. Works the same way as *ebp* on x86.
* **SP(P14)** - Stack Pointer, current location on the stack, same as the x86 *esp*.
* **PC(R15)** - Program Counter, pointer to the currently executing instruction

**Calling Convention**

VAX passes arguments on the stack, so when calling a function, arguments are pushed onto the stack and then the function call; returned values are returned via *r0*:

```
   110c3:	9f ef b5 c2 	pushab 2d37e <__fini+0x1080c>	# r
   110c7:	01 00 
   110c9:	9f ef b1 c2 	pushab 2d380 <__fini+0x1080e>	# passphrase.txt
   110cd:	01 00 
   110cf:	fb 02 ef 10 	calls $0x2,14fe6 <fopen>
   110d3:	3f 00 00 
   110d6:	d0 50 cd a0 	movl r0,0xfffffda0(fp)
```

This snipped calls *fopen()* by first pushing the address of two strings ("passphrase.txt" and "r") to the stack, the result of the *fopen()* function is then returned in *r0* and saved to a local variable at an offset from the *fp* register.

**Addressing Modes**

The VAX instructions interpret the operands from left to right, that is the right most (last) operand is the destination. So `addl3 r1, r2, r3` would store the result of adding *r1* to *r2* into the *r3* register.

VAX is a complex instruction set and opcodes could be:

* Immediate Values
* **Rn** - Register Values
* **(Rn)** - Deferred register, dereferences the address in *Rn*
* **dis(Rn)** - Displacement, adds the displacement, *dis*, to *Rn* and dereferences the result
* **base-mode[Rx]** - Indexes into an array pointed to by the *base-mode* (could be a register, deference value, etc). The size of the elements in the array is based on the instruction. Using the index addressing mode with a *movl* uses 4-byte entries.

**Renaming**

One of the most useful features of [IDA Pro](https://www.hex-rays.com), is the ability to rename memory address and following cross-references. To emulate the ability rename memory address and offsets we copied interesting functions to their own text file and then used a global search and replace to "rename" numbers to more meaningful labels. For example `0xfffffda0(fp)` becomes `file_object(fp)`. Code snippets in the rest of this document will have the renamed labels.

**VAX Reference**

We found the [VAX MACRO and Instruction Set Reference Manual](https://www.itec.suny.edu/scsys/vms/ovmsdoc073/v73/4515/4515pro_contents.html) to be useful in order to lookup any instructions we need more help with.

### Global/Constant Data

The *server.s* disassembly file disassembled everything! Including any global data and constants, such a strings:

```
   5ef38:	43 01 00 00 	subf3 $0x1 [f-float],$0x0 [f-float],$0x0 [f-float]
   5ef3c:	4e 01 00    	cvtlf $0x1,$0x0 [f-float]
   5ef3f:	00          	halt
   5ef40:	4d 01 00    	cvtwf $0x1,$0x0 [f-float]
   5ef43:	00          	halt
```

This makes searching for strings and other global data very difficult. To work around this, we wrote a little script to pull the bytes listed after the address and before the instruction decoding into a file. We could then use a hex editor to jump to an offset and see the data/strings:

![server bin](server%20bin.png)

This is the script we made: [asm_to_bin.py](https://github.com/ACMEPharm/hack-a-sat-ctf-quals-2020/blob/master/Vax%20the%20Sat/asm_to_bin.py)

### Checksum Finding

First up identify the checksum code. At this point we had assumed the challenge was going to be locating the checksum function, reverse engineer it, and create some tool to generate a checksum for the targeted coordinates. We were only partly correct. We had to figure out how the checksum is being created, but only the first byte of the checksum turned out to be relevant. To find the checksum algorithm we first search *server.s* for "checksum", "hash", etc... and found nothing. 

Finally, we just started searching for "float" and came across the *uint2IEEE754()* function. Since we had to specify the latitude and longitude coordinates as HEX encoded integers, calling a function used to convert a "uint" into an "IEEE754" floating point number is probably somewhere around where the checksumming code is. So we searched for *uint2IEEE754* and found:

```
00010d74 <ADCS_module>:
...
   11250:	dd cd b4 fd 	pushl 0xfffffdb4(fp)            
   11254:	fb 01 ef 81 	calls $0x1,105dc <uint2IEEE754>
   11258:	f3 ff ff 
   1125b:	50 50 a6 04 	movf r0,0x4(r6)
   1125f:	d0 cd 88 fd 	movl 0xfffffd88(fp),r6
   11263:	56 
   11264:	dd cd b0 fd 	pushl 0xfffffdb0(fp)
   11268:	fb 01 ef 6d 	calls $0x1,105dc <uint2IEEE754>
```

Nice! Two calls to *uint2IEEE754* within an *ADCS_module()* function! Our checksum code should be around here somewhere! Since we probably convert to float after the checksum verification lets look up. Scrolling up we find some code that tests hex inputs:

```
   10eb6:	dd 08       	pushl $0x8
   10eb8:	d0 cd 8c fd 	movl 0xfffffd8c(fp),r0
   10ebc:	50 
   10ebd:	dd a0 08    	pushl 0x8(r0)
   10ec0:	fb 02 ef 0f 	calls $0x2,103d6 <testHex>
   10ec4:	f5 ff ff 
   10ec7:	d5 50       	tstl r0
   10ec9:	13 19       	beql 10ee4 <ADCS_module+0x170>
   10ecb:	9f ef 2b c4 	pushab 2d2fc <__fini+0x1078a>	# 'ADCS CFG_POS ERROR: LATITUDE BAD CHARACTER'
   10ecf:	01 00 
   10ed1:	dd cd 88 fd 	pushl 0xfffffd88(fp)
   10ed5:	fb 02 ef 14 	calls $0x2,10cf0 <error>
   10ed9:	fe ff ff 
   10edc:	d2 00 cd 84 	mcoml $0x0,0xfffffd84(fp)
   10ee0:	fd 
   10ee1:	31 0e 06    	brw 114f2 <ADCS_module+0x77e>
   10ee4:	dd 08       	pushl $0x8
   10ee6:	d0 cd 8c fd 	movl 0xfffffd8c(fp),r0
   10eea:	50 
   10eeb:	dd a0 0c    	pushl 0xc(r0)
   10eee:	fb 02 ef e1 	calls $0x2,103d6 <testHex>
   10ef2:	f4 ff ff 
   10ef5:	d5 50       	tstl r0
   10ef7:	13 19       	beql 10f12 <ADCS_module+0x19e>
   10ef9:	9f ef 28 c4 	pushab 2d327 <__fini+0x107b5> # 'ADCS CFG_POS ERROR: LONGITUDE BAD CHARACTER'
   10efd:	01 00 
   10eff:	dd cd 88 fd 	pushl 0xfffffd88(fp)
   10f03:	fb 02 ef e6 	calls $0x2,10cf0 <error>
   10f07:	fd ff ff 
   10f0a:	d2 00 cd 84 	mcoml $0x0,0xfffffd84(fp)
   10f0e:	fd 
   10f0f:	31 e0 05    	brw 114f2 <ADCS_module+0x77e>
   10f12:	dd 20       	pushl $0x20
   10f14:	d0 cd 8c fd 	movl 0xfffffd8c(fp),r0
   10f18:	50 
   10f19:	dd a0 10    	pushl 0x10(r0)
   10f1c:	fb 02 ef b3 	calls $0x2,103d6 <testHex>
   10f20:	f4 ff ff 
   10f23:	d5 50       	tstl r0
   10f25:	13 19       	beql 10f40 <ADCS_module+0x1cc>
   10f27:	9f ef 26 c4 	pushab 2d353 <__fini+0x107e1>	# 'ADCS CFG_POS ERROR: CHECKSUM BAD CHARACTER'
   10f2b:	01 00 
   10f2d:	dd cd 88 fd 	pushl 0xfffffd88(fp)
   10f31:	fb 02 ef b8 	calls $0x2,10cf0 <error>
```

This code is verifying that the latitude, longitude, and checksum all contain valid hex characters. Too far! Checksum code must be between these two areas. Looking down, we see some calls to *strtoul()* to convert the hex strings to integers:

```
   10f44:	d0 cd 8c fd 	movl cmd_args(fp),r0
   10f48:	50 
   10f49:	dd a0 08    	pushl 0x8(r0)
   10f4c:	fb 03 ef 57 	calls $0x3,125aa <strtoul>	# convert hex to uint
   10f50:	16 00 00 
   10f53:	d0 50 cd b4 	movl r0,lat_as_uint(fp)
   10f57:	fd 
   10f58:	dd 10       	pushl $0x10
   10f5a:	d4 7e       	clrf -(sp)
   10f5c:	d0 cd 8c fd 	movl cmd_args(fp),r0
   10f60:	50 
   10f61:	dd a0 0c    	pushl 0xc(r0)
   10f64:	fb 03 ef 3f 	calls $0x3,125aa <strtoul>	# convert hex to uint
   10f68:	16 00 00 
   10f6b:	d0 50 cd b0 	movl r0,long_as_uint(fp)
```

Those are the two latitude and longitude values, a bit further on (after some copies to temporary strings) are the *strtoul()* calls to convert the checksum as four 32-bit unsigned integers:

```
   1100c:	9e cd 60 fe 	movab 0xfffffe60(fp),r0
   11010:	50 
   11011:	dd 50       	pushl r0
   11013:	fb 03 ef 90 	calls $0x3,125aa <strtoul> # convert 4 bytes of checksum
   11017:	15 00 00 
   1101a:	d0 50 cd 50 	movl r0,coords_checksum(fp)
   1101e:	fe 
   1101f:	dd 10       	pushl $0x10
   11021:	d4 7e       	clrf -(sp)
   11023:	9e cd 60 fe 	movab 0xfffffe60(fp),r0
   11027:	50 
   11028:	c0 09 50    	addl2 $0x9,r0
   1102b:	dd 50       	pushl r0
   1102d:	fb 03 ef 76 	calls $0x3,125aa <strtoul> # convert 4 bytes of checksum
   11031:	15 00 00 
   11034:	d0 50 cd 54 	movl r0,0xfffffe54(fp)
   11038:	fe 
   11039:	dd 10       	pushl $0x10
   1103b:	d4 7e       	clrf -(sp)
   1103d:	9e cd 60 fe 	movab 0xfffffe60(fp),r0
   11041:	50 
   11042:	c0 12 50    	addl2 $0x12,r0
   11045:	dd 50       	pushl r0
   11047:	fb 03 ef 5c 	calls $0x3,125aa <strtoul> # convert 4 bytes of checksum
   1104b:	15 00 00 
   1104e:	d0 50 cd 58 	movl r0,0xfffffe58(fp)
   11052:	fe 
   11053:	dd 10       	pushl $0x10
   11055:	d4 7e       	clrf -(sp)
   11057:	9e cd 60 fe 	movab 0xfffffe60(fp),r0
   1105b:	50 
   1105c:	c0 1b 50    	addl2 $0x1b,r0
   1105f:	dd 50       	pushl r0
   11061:	fb 03 ef 42 	calls $0x3,125aa <strtoul> # convert 4 bytes of checksum
   11065:	15 00 00 
   11068:	d0 50 cd 5c 	movl r0,0xfffffe5c(fp)
```

After all the hex to integer conversions we come to two function calls that probably implement the checksumming the first appears to format the data into a buffer:

```
   1106d:	9e cd 50 fe 	movab coords_checksum(fp),r0
   11071:	50 
   11072:	dd 50       	pushl r0
   11074:	dd cd b4 fd 	pushl lat_as_uint(fp)
   11078:	dd cd b0 fd 	pushl long_as_uint(fp)
   1107c:	9e cd e4 fd 	movab coords_breakdown_result(fp),r0
   11080:	50 
   11081:	dd 50       	pushl r0
   11083:	fb 04 ef 18 	calls $0x4,123a2 <breakdown_coordinates>
```

To call the *breakdown_coordinates()* function this code first pushes the address of the checksum, the two latitude and longitude values, and then an address we haven't seen before. Since this address wasn't references before, we assumed this would contain the formatted buffer that will be checksummed.

Immediately after the call to *breakdown_coordinates()*, there is a call to *execute_operation()*:

```
   1109c:	dd cd a4 fd 	pushl const_0xa264(fp)
   110a0:	dd cd a8 fd 	pushl const_0x40(fp)
   110a4:	dd cd ac fd 	pushl const_0x2c(fp)
   110a8:	9e cd e4 fd 	movab coords_breakdown_result(fp),r0
   110ac:	50 
   110ad:	dd 50       	pushl r0
   110af:	9e cd 24 fe 	movab calculated_checksum(fp),r0
   110b3:	50 
   110b4:	dd 50       	pushl r0
   110b6:	9f ef a0 dd 	pushab 5ee5c <op>
   110ba:	04 00 
   110bc:	fb 06 ef 3b 	calls $0x6,121fe <execute_operation>
```

The const_* variables were local variables that had been initialized to constant values. We renamed them from something like `0xfffffd88(fp)` to the more readable `const_0xa264(fp)` and to remind us what value was actually stored at that memory address. This code pushes a number of constants, the result of the *breakdown_coordinates()*, an address of a buffer that was not yet referenced, which again we assumed to be a buffer to store the output, and a pointer to global data. Initially, we figured this was something like a CRC table or some lookup table for a custom checksum algorithm...

### The Flaw!

Ok, we think we identified where the checksum is being calculated, let's look a little farther down and see how the code verifies the checksum. Usually we would see code calculate a checksum and then check that checksum against the transmitted checksum and verify that they match. That is what we were expecting! But we were wrong! The first twist in this saga. The first code after the checksum calculation opens and reads a file called 'passphrase.txt':

```
   110c3:	9f ef b5 c2 	pushab 2d37e <__fini+0x1080c>	# 'r'
   110c7:	01 00 
   110c9:	9f ef b1 c2 	pushab 2d380 <__fini+0x1080e>	# 'passphrase.txt'
   110cd:	01 00 
   110cf:	fb 02 ef 10 	calls $0x2,14fe6 <fopen>
   110d6:	d0 50 cd a0 	movl r0,file_object(fp)
   ... <error checking code>
   110fa:	dd cd a0 fd 	pushl file_object(fp)
   110fe:	dd 2c       	pushl $0x2c
   11100:	dd 01       	pushl $0x1
   11102:	9e cd b8 fd 	movab passphrase(fp),r0	
   11106:	50 
   11107:	dd 50       	pushl r0
   11109:	fb 04 ef 7e 	calls $0x4,1508e <fread>
```

This was unexpected... Did they read a specific checksum from a file? Do we have to find some coordinates that would create a checksum to match this unknown value? Yikes! Brute forcing this will probably be impractical... Do we have to find another bug to leak the contents of 'passphrase.txt'? Lots of panicked thoughts at this point... but scroll down a bit and we saw a classic *strncmp()* and *strlen()* flaw:

```
   11139:	dd 2c       	pushl $0x2c
   1113b:	9e cd 24 fe 	movab calculated_checksum(fp),r0
   1113f:	50 
   11140:	dd 50       	pushl r0
   11142:	fb 02 ef 65 	calls $0x2,1b1ae <strnlen>
   11146:	a0 00 00 
   11149:	dd 50       	pushl r0
   1114b:	9e cd 24 fe 	movab calculated_checksum(fp),r0
   1114f:	50 
   11150:	dd 50       	pushl r0
   11152:	9e cd b8 fd 	movab passphrase(fp),r0
   11156:	50 
   11157:	dd 50       	pushl r0
   11159:	fb 03 ef a8 	calls $0x3,15408 <strncmp>		# flaw! using the length of the calculate checksum to check against the phassphrase
   ... <code that opens a flag.txt file and prints the flag>
```

The *strncmp()* is a great function, security wise it can be used to ensure we don't read beyond the end of a string, but 'n' shouldn't rely on just the length of the source! As it is in this case. If I can control length of the source data and I can make it an empty string. The length of an empty string is zero, so 'n' is zero. When comparing zero length strings the *strncmp()* function will always return that the strings match ("" == "")!

To get the server to send us the flag we need to find an input (the coordinates and checksum data) that will result in a calculated checksum where the first byte is the null terminator (0x00). Phew, this should be much more simple than trying to figure out the passphrase stored in the phasephrase.txt file!

### breakdown_coordinates()

Now that we know what we need to do, let's break down the functions that go into creating the checksum starting with the function that formats the input into a buffer that can be checksummed.

This function contained three loops, the first two were almost identical and converted the latitude and longitude values:

```
   123b8:	d0 ad f8 56 	movl counter(fp),r6
   123bc:	d0 ac 08 50 	movl log_uint(ap),r0
   123c0:	dd ad f0    	pushl const_0x100(fp)
   123c3:	dd 50       	pushl r0
   123c5:	fb 02 ef b8 	calls $0x2,1ad84 <__urem>
   123c9:	89 00 00 
   123cc:	d0 50 46 bc 	movl r0,*out_data(ap)[r6]
   123d0:	04 
   123d1:	dd ad f0    	pushl const_0x100(fp)
   123d4:	dd ac 08    	pushl log_bytes(ap)
   123d7:	fb 02 ef 4a 	calls $0x2,1ad28 <__udiv>
   123db:	89 00 00 
   123de:	d0 50 ac 08 	movl r0,log_uint(ap)
   123e2:	d6 ad f8    	incl counter(fp)
   123e5:	11 c9       	brb 123b0 <breakdown_coordinates+0xe>
```

This code looks scary with the calls to *__urem()* and *__udiv()* but it is really quite simple. All it is doing is taking the four bytes of input, starting with the low byte, and expanding it so that each byte is stored in its own 32-bit word. The equivalent C code would look something like this:

```c
// output is an (unsigned int*)
int i = 0
for(; i < 4; i++) {
  output[i] = log_uint % 256;
  log_uint = log_uint / 256;
}
```

The next block of code does a similar thing, but for the latitude. Note the index variable 'i' is continued on, so this is being appended:

```c
for(; i < 4; i++) {
  output[i] = lat_uint % 256;
  log_uint = lat_uint / 256;
}
```

The checksum copying code looks like this:

```
   1242b:	d1 ad f4 03 	cmpl counter2(fp),$0x3 $ copies the 16-byte checksum to the end of this
   1242f:	15 02       	bleq 12433 <breakdown_coordinates+0x91>
   12431:	11 1b       	brb 1244e <breakdown_coordinates+0xac>
   12433:	d0 ad f4 50 	movl counter2(fp),r0
   12437:	c4 04 50    	mull2 $0x4,r0
   1243a:	c1 50 ac 04 	addl3 r0,out_data(ap),r1
   1243e:	51 
   1243f:	d0 ad f4 50 	movl counter2(fp),r0
   12443:	d0 40 bc 10 	movl *checksum(ap)[r0],0x20(r1)
   12447:	a1 20 
   12449:	d6 ad f4    	incl counter2(fp)
   1244c:	11 dd       	brb 1242b <breakdown_coordinates+0x89>
```

And just copies the data with 4 32-bit moves:

```c
for(int j = 0; j < 4; j++) {
  output[8 + j] = checksum[j];
}
```

Note: the ASM used 0x20(r1) to calculate the offset into the output, since we defined output to be a pointer to unsigned int in our "C" code, we have to divide by four to calculate the correct array index.

Basically, this code just explodes the each four byte coordinate into four 32-bit values. So calling this function with the following inputs:

```
LOG: 0x11223344
LAT: 0x55667788
CHECKSUM: 01020304111213142122232431323334
```

Results in a buffer looking like:

```
44 00 00 00 33 00 00 00 22 00 00 00 11 00 00 00
88 00 00 00 77 00 00 00 66 00 00 00 55 00 00 00
01 02 03 04 11 12 13 14 21 22 23 24 31 32 33 34
```

### execute_operation()

We must be getting close to the real checksum algorithm! Not quite yet, that is yet another function down, but this function does setup some critical data structures.

First off we malloc a buffer and make a copy of the incoming 'op' data:

```
   1221b:	dd ac 18    	pushl const_0xa264(ap)	# make our buffr
   1221e:	fb 01 ef 75 	calls $0x1,13e9a <malloc>
   12222:	1c 00 00 
   12225:	d0 50 ad f8 	movl r0,buffer(fp)
   
   12229:	dd ac 18    	pushl const_0xa264(ap)	# copy something big from data
   1222c:	dd ac 04    	pushl op(ap)
   1222f:	dd ad f8    	pushl buffer(fp)
   12232:	fb 03 ef f9 	calls $0x3,1b732 <memcpy>
   12236:	94 00 00 
   12239:	d0 ad f8 ac 	movl buffer(fp),op(ap)	# replace op with our copy
```

The 'op' pointer and the constant 0xa264 were passed into this function fro the main *ADCS_module()* function, and we renamed the unfriendly hex offsets from the *ap* register to more friendly names. Initially, the importance of the name 'op' was lost to us, but we soon realized what it meant. The equivalent C code mallocs the buffer, copies op, and replaces the op argument to point to our new buffer:

```c
our_op = malloc(0xa264)
memcopy(our_op, op, 0xa264);
op = our_op;
```

Next up was a loop that copied the exploded data from the *breakdown_coordinates()* function into our 'op' data:

```
   1224d:	d0 ad ec ad 	movl const_0x03f0(fp),counter(fp)
   12251:	e4 
   
   12252:	c1 ad ec ac 	addl3 const_0x03f0(fp),const_0x40_exploded_size(ap),r0
   12256:	14 50 
   12258:	d1 ad e4 50 	cmpl counter(fp),r0
   1225c:	19 02       	blss 12260 <execute_operation+0x62>
   1225e:	11 16       	brb 12276 <execute_operation+0x78>
   12260:	c1 ac 04 ad 	addl3 op(ap),counter(fp),r1
   12264:	e4 51 
   12266:	c3 ad ec ad 	subl3 const_0x03f0(fp),counter(fp),r0 # after maths r0 = counter
   1226a:	e4 50 
   1226c:	90 40 bc 0c 	movb *exploded_data(ap)[r0],(r1)	# copy our exploded data to op + 0x03f0 (copies 0x40 bytes)
   12270:	61 
   12271:	d6 ad e4    	incl counter(fp)
   12274:	11 dc       	brb 12252 <execute_operation+0x54>
```

The equivalent C code:

```c
for(int i = 0; i < 0x40; i++) {
	op[0x3f0 + i] = exploded_data[i];
}
```

Next up was another loop that cleared data:

```
   12277:	d0 ac 14 ad 	movl const_0x40_exploded_size(ap),local_const_0x40(fp)
   1227b:	d4 
   1227c:	d0 ad d4 ad 	movl local_const_0x40(fp),0xffffffd0(fp)
   12280:	d0 
   12281:	d5 ad d0    	tstl 0xffffffd0(fp)	
   12284:	18 04       	bgeq 1228a <execute_operation+0x8c>
   12286:	c0 03 ad d0 	addl2 $0x3,0xffffffd0(fp) # = 0x40 + 3 (from the test I don't think we do this one)
   1228a:	78 8f fe ad 	ashl $0xfe,0xffffffd0(fp),r0 	# 0x40 >> 2
   1228e:	d0 50 
   12290:	c4 04 50    	mull2 $0x4,r0	# 0x10 * 4 = 0x40.... ? right back, maybe the above word aligns the size
   12293:	c3 50 ad d4 	subl3 r0,local_const_0x40(fp),r0	# r0 = 0 ?
   12297:	50 
   12298:	c3 50 ac 14 	subl3 r0,const_0x40_exploded_size(ap),r0			# r0 = 0x40
   1229c:	50 
   1229d:	c0 04 50    	addl2 $0x4,r0						# r0 = 0x44
   122a0:	d1 ad e4 50 	cmpl counter(fp),r0
   122a4:	19 02       	blss 122a8 <execute_operation+0xaa>
   122a6:	11 0d       	brb 122b5 <execute_operation+0xb7>
   122a8:	c1 ac 04 ad 	addl3 op(ap),counter(fp),r0
   122ac:	e4 50 
   122ae:	94 60       	clrb (r0)							# clear data after op + 0x03f0, not sure yet where we end
   122b0:	d6 ad e4    	incl counter(fp)
   122b3:	11 c2       	brb 12277 <execute_operation+0x79>
```

It looks scary, but all it really did was word align the length of the input data and clear an extra word. Since this function was called with a constant for the size of the input data that was always word aligned and this code only cleared one extra word. The C code would look something like this:

```c
for (/* i continues from previous loop */; i < 0x44; i++) {
	op[0x3f0 + i] = 0;
}
```

Next was another loop that cleared data:

```
   122b5:	d0 ad e8 ad 	movl const_0x0244(fp),counter(fp)
   122b9:	e4 
   122ba:	c1 ad e8 ac 	addl3 const_0x0244(fp),const_0x2c_output_size(ap),const_0x270(fp)
   122be:	10 ad cc 
   122c1:	d0 ac 14 ad 	movl const_0x40_exploded_size(ap),local_const_0x40_2(fp)
   122c5:	c8 
   122c6:	d0 ad c8 ad 	movl local_const_0x40_2(fp),0xffffffc4(fp)
   122ca:	c4 
   122cb:	d5 ad c4    	tstl 0xffffffc4(fp)
   122ce:	18 04       	bgeq 122d4 <execute_operation+0xd6>
   122d0:	c0 03 ad c4 	addl2 $0x3,0xffffffc4(fp)
   122d4:	78 8f fe ad 	ashl $0xfe,0xffffffc4(fp),r0
   122d8:	c4 50 
   122da:	c4 04 50    	mull2 $0x4,r0						# r0 = 0x40 again?
   122dd:	c3 50 ad c8 	subl3 r0,local_const_0x40_2(fp),r0	# r0 = 0x0
   122e1:	50 
   122e2:	c3 50 ad cc 	subl3 r0,const_0x270(fp),r0			# r0 = 0x270
   122e6:	50 
   122e7:	c0 04 50    	addl2 $0x4,r0						# r0 = 0x274
   122ea:	d1 ad e4 50 	cmpl counter(fp),r0
   122ee:	19 02       	blss 122f2 <execute_operation+0xf4>
   122f0:	11 0d       	brb 122ff <execute_operation+0x101>
   122f2:	c1 ac 04 ad 	addl3 op(ap),counter(fp),r0
   122f6:	e4 50 
   122f8:	94 60       	clrb (r0)
   122fa:	d6 ad e4    	incl counter(fp)					# more mem clearing
   122fd:	11 bb       	brb 122ba <execute_operation+0xbc>
```

Again, the counter math makes it look more intimidating than it is. All this code did was clear 0x30 bytes of data at offset 0x244 into the 'op' buffer. The counter math is there to word align the size of the expected output, which was passed as a constant 0x2c, and add an extra word. The equivalent C code is:

```c
for (int i = 0; i < 0x30; i++) {
	op[0x244 + i] = 0;
}
```

We can also make an assumption here, offset 0x244 into the 'op' array, will contain the output of the checksum calculation. Why else would the code clear a buffer here and not reference it again until the end of the function, where it reads from this offset?

Then we had a series of 32-bit writes to specific addresses. This writes encoded specific information such as the size of the input and outputs and the offsets into the op array:

```
   12309:	d0 ad e0 51 	movl const_0xc8(fp),r1
   1230d:	d0 ac 10 50 	movl const_0x2c_output_size(ap),r0
   12311:	c6 04 50    	divl2 $0x4,r0
   12314:	d0 50 41 bc 	movl r0,*op(ap)[r1]			# op[0xc8] = 0xb	# output_size in words	[1]
   12318:	04 
   12319:	d0 ad dc 51 	movl const_0xc9(fp),r1
   1231d:	d0 ac 14 50 	movl const_0x40_exploded_size(ap),r0
   12321:	c6 04 50    	divl2 $0x4,r0
   12324:	d0 50 41 bc 	movl r0,*op(ap)[r1]			# op[0xc9] = 0x10	# exploded size in words
   12328:	04 
   12329:	d0 ac 04 51 	movl op(ap),r1
   1232d:	d0 ad e8 50 	movl const_0x0244(fp),r0
   12331:	c6 04 50    	divl2 $0x4,r0				# r0 = 0x91
   12334:	d0 50 a1 04 	movl r0,0x4(r1)				# op[4] = 0x91		# output checksum offset in words
   12338:	d0 ac 04 51 	movl op(ap),r1
   1233c:	d0 ad ec 50 	movl const_0x03f0(fp),r0
   12340:	c6 04 50    	divl2 $0x4,r0				# 0xfc
   12343:	d0 50 a1 08 	movl r0,0x8(r1)				# op[0x8] = 0xfc	# exploded offset in words
   12347:	d0 ac 04 51 	movl op(ap),r1
   1234b:	d0 ad e0 50 	movl const_0xc8(fp),r0
   1234f:	c6 04 50    	divl2 $0x4,r0
   12352:	d0 50 a1 0c 	movl r0,0xc(r1)				# op[0xc] = 0x32	# offset to [1] in words
   12356:	d0 ac 04 51 	movl op(ap),r1
   1235a:	d0 ad dc 50 	movl const_0xc9(fp),r0
   1235e:	c6 04 50    	divl2 $0x4,r0
   12361:	d0 50 a1 10 	movl r0,0x10(r1)			# op[0x10] = 0x32	# offset to exploded size in words? we truncate the result here...
```

Since all these variables were passed in as constants we know the values that will be placed into the op buffer. The op buffer will be updated with the following values:

```
000:          91000000 fc000000 32000000
010: 32000000
...
320: 0b000000 10000000
```

After all the setup, we finally have a call to *executor()*:

```
   12365:	dd ac 18    	pushl const_0xa264(ap)
   12368:	dd ac 04    	pushl op(ap)
   1236b:	fb 02 ef 80 	calls $0x2,120f2 <executor>
   1236f:	fd ff ff 
```

We are just passing the 'op' buffer and the size of the buffer... Hmm, that is an unusual name for a checksum function. Executor? Variable name of 'op'?... Hey is this some sort of VM with op containing a program that is being emulated to calculate the checksum? Why, yes of course... how else would you calculate a checksum? With a lookup table?

### executor()

Well, this is the last challenge in the Ground Segment category. We can't have a normal checksum algorithm here, so of course we have to have a VM and emulate something. At least the function is small!

The first thing this function does is locate the initial *PC* (Program Counter) this is the last 32-bit word in the input image:

```
   120f7:	c1 ac 04 ac 	addl3 op(ap),const_0xa264_op_size(ap),r0
   120fb:	08 50 
   120fd:	c2 04 50    	subl2 $0x4,r0
   12100:	d0 60 ad e8 	movl (r0),curr_pc(fp)
   12104:	dd ad e8    	pushl curr_pc(fp)
   12107:	dd ac 08    	pushl const_0xa264_op_size(ap)
   1210a:	9f ef c4 b7 	pushab 2d8d4 <__fini+0x10d62>	# 'file size at pc:%lu:%u'
   1210e:	01 00 
   12110:	fb 03 ef c7 	calls $0x3,129de <printf>
   12114:	08 00 00 
```

There is even a helpful *printf()* that logs the PC value. The string also made it easy to figure out what this code did and to confirm that we are indeed emulating something. The equivalent C code would be:

```c
uint32_t pc = ((uint32_t*)op)[op_size - 1];
```

Then we have the start of a while loop, that just checks to make sure that the *PC* doesn't go beyond the end of the input image:

```
   1211a:	d0 ac 08 52 	movl const_0xa264_op_size(ap),r2
   1211e:	d0 02 51    	movl $0x2,r1
   12121:	83 51 20 50 	subb3 r1,$0x20,r0	# r0 = 0x1e
   12125:	ef 51 50 52 	extzv r1,r0,r2,r0			# end check case basically a div by 4? maybe pc is in words
   12129:	50 
   1212a:	d1 ad e8 50 	cmpl curr_pc(fp),r0		# make sure we haven't run to the end
   1212e:	1f 03       	blssu 12133 <executor+0x41>
   12130:	31 ba 00    	brw 121ed <executor+0xfb>
```

The extzv instruction is a bit confusing, but it is just selecting 30 bits starting at bit 2 and shifting to the right by two, aka a divide by four:

```c
while (pc < op_size / 4) {
  ...
}
```

Next the code reads four 32-bit values starting from the *PC* offset. We called this values operand_0 - operand_3:

```
   12136:	d0 ad e8 50 	movl curr_pc(fp),r0
   1213a:	d0 40 bc 04 	movl *op(ap)[r0],operand_0(fp)	# op0 = op[pc * 4]
   1213e:	ad f4 
   12140:	d0 ad e8 50 	movl curr_pc(fp),r0
   12144:	c4 04 50    	mull2 $0x4,r0
   12147:	c0 ac 04 50 	addl2 op(ap),r0
   1214b:	d0 a0 04 ad 	movl 0x4(r0),operand_1(fp)		# op1 = op[pc * 4 + 4]
   1214f:	f0 
   12150:	d0 ad e8 50 	movl curr_pc(fp),r0
   12154:	c4 04 50    	mull2 $0x4,r0
   12157:	c0 ac 04 50 	addl2 op(ap),r0
   1215b:	d0 a0 08 ad 	movl 0x8(r0),operand_2(fp)		# op2 = op[pc * 4 + 8]
   1215f:	f8 
   12160:	d0 ad e8 50 	movl curr_pc(fp),r0
   12164:	c4 04 50    	mull2 $0x4,r0
   12167:	c0 ac 04 50 	addl2 op(ap),r0
   1216b:	d0 a0 0c ad 	movl 0xc(r0),operand_3(fp)		# op3 = op[pc * 4 + 0xc]
   1216f:	ec 
```

The C equivalent would be (we created a second array op_int32 that points to the same op data, so we can index into an array of 32-bit elements):

```c
	int32_t op_int32* = (int32_t*)op;
  
	int operand_0 = op_int32[0];
	int operand_1 = op_int32[1];
	int operand_2 = op_int32[2];
	int operand_3 = op_int32[3];
```

Up next was a check for the 'stop' instruction (which we never actually saw...):

```
   12170:	d1 ad f8 8f 	cmpl operand_2(fp),$0xffffffff
   12174:	ff ff ff ff 
   12178:	12 16       	bneq 12190 <executor+0x9e>
   1217a:	d1 ad f0 8f 	cmpl operand_1(fp),$0xffffffff
   1217e:	ff ff ff ff 
   12182:	12 0c       	bneq 12190 <executor+0x9e>
   12184:	d1 ad f4 8f 	cmpl operand_0(fp),$0xffffffff
   12188:	ff ff ff ff 
   1218c:	12 02       	bneq 12190 <executor+0x9e>
   1218e:	11 5d       	brb 121ed <executor+0xfb>
```

```c
	if (operand_2 == 0xffffffff || operand_1 == 0xffffffff || operand_0 == 0xffffffff) {
    break;
  }
```

Next we finally did some checksumming! Looks like the code is using the operands as offset into op to create an additive checksum:

```
   12190:	d0 ad f8 52 	movl operand_2(fp),r2
   12194:	d0 ad f8 51 	movl operand_2(fp),r1
   12198:	d0 ad f0 50 	movl operand_1(fp),r0
   1219c:	c1 41 bc 04 	addl3 *op(ap)[r1],*op(ap)[r0],*op(ap)[r2]	# op[op2] = op[op1] + op[op2]
   121a0:	40 bc 04 42 
   121a4:	bc 04 
```

```c
	op_int32[operand_2] = op_int32[operand_1] + op_int32[operand_2]
```

So operands 2 and 1 are offsets into the op array and the instruction will add values at those offsets and store them into an offset specified by operand_2. Presumably there will be instructions that reference the input data with operand_1, and some instructions where operand_2 will point into the op area reserved for outputs. By the time the vm has stopped execution the input bytes would have been included and the output bytes would be filled with the calculated checksum.

Up next is a sequence of compares that will eventually result in either 4 being added to the *PC* or operand_3 being added. What happens depends on the data pointed to by the offsets:

```
   121a6:	d0 ad f0 50 	movl operand_1(fp),r0
   121aa:	d5 40 bc 04 	tstl *op(ap)[r0]
   121ae:	19 11       	blss 121c1 <executor+0xcf>
   121b0:	d0 ad f8 51 	movl operand_2(fp),r1
   121b4:	d0 ad f4 50 	movl operand_0(fp),r0
   121b8:	d1 41 bc 04 	cmpl *op(ap)[r1],*op(ap)[r0]	# cmp op[op2], op[op0]
   121bc:	40 bc 04 
   121bf:	15 1d       	bleq 121de <executor+0xec>	# do the pc + op3
   
   121c1:	d0 ad f0 50 	movl operand_1(fp),r0
   121c5:	d5 40 bc 04 	tstl *op(ap)[r0]
   121c9:	18 1b       	bgeq 121e6 <executor+0xf4>
   121cb:	d0 ad f8 51 	movl operand_2(fp),r1
   121cf:	d0 ad f4 50 	movl operand_0(fp),r0
   121d3:	d1 41 bc 04 	cmpl *op(ap)[r1],*op(ap)[r0]	# cmp op[op2], op[op0]=
   121d7:	40 bc 04 
   121da:	18 02       	bgeq 121de <executor+0xec>	# do the pc + op3
   121dc:	11 08       	brb 121e6 <executor+0xf4>
   121de:	c0 ad ec ad 	addl2 operand_3(fp),curr_pc(fp)	# pc = pc + op3
   121e2:	e8 
   121e3:	31 34 ff    	brw 1211a <executor+0x28>
   121e6:	c0 04 ad e8 	addl2 $0x4,curr_pc(fp)			# pc += 4
   121ea:	31 2d ff    	brw 1211a <executor+0x28>
```

After unpacking the comparisons, the C equivalent of this code is:

```c
	if ((op_int32[operand_1] >= 0 && op_int32[operand_2] <= op_int32[operand_2]) ||
			(op_int32[operand_1] <  0 && op_int32[operand_2] >= op_int32[operand_2]) {
		pc = pc + op3 
  } else {
		pc = pc + 4
}  // end of while loop           
```

That's it! Simple virtual machine. 

## Checksum Simulator

With the reverse engineering done, let's make our own checksumming code so we can try to figure out the magic input that results in a checksum starting with a null byte!

### Basic Simulator

First, we made a basic python script that implemented the *executor()* function:

```python
#!/usr/bin/env python3

import argparse
import numpy
import binascii

OUTPUT_OFFSET = 0x244
OUTPUT_SIZE = 0x2c

parser = argparse.ArgumentParser()
parser.add_argument("op_input", type=argparse.FileType("rb"))
args = parser.parse_args()

def hexlify(d):
    return str(binascii.hexlify(d), "ascii").upper()

op_data = bytearray(args.op_input.read())
op_int = numpy.frombuffer(op_data, dtype=numpy.int32)

pc = op_int[-1]
step_count = 0
while pc < len(op_int):
    op0, op1, op2, op3 = op_int[pc:pc+4]
    step_count += 1

    print("PC = {:08x}({:08x}) OP: {:08x} {:08x} {:08x} {:08x}".format(pc, pc*4, op0, op1, op2, op3))

    if op2 == 0xffffffff and op1 == 0xffffffff and op0 == 0xffffffff:
        print("Stop instruction?")
        break

    op_int[op2] = op_int[op2] + op_int[op1]
    print("\top[{:08x}] = op[{:08x}] + op[{:08x}]".format(op2, op2, op1))

    
    if  (op_int[op1] >= 0 and op_int[op2] <= op_int[op0]) or \
        (op_int[op1] < 0 and op_int[op2] >= op_int[op0]):
        pc = pc + op3
    else:
        pc = pc + 4

print(f"Ran for {step_count} steps")
print("Output:", hexlify(op_data[OUTPUT_OFFSET:OUTPUT_OFFSET+OUTPUT_SIZE:4]))
```

Nothing too fancy here. To make it easier to access arrays of data we used [NumPy](https://numpy.org) to overlay an array of ints over the data we read in. Both op_data and op_int reference the same buffer so changes in either array affect both.

Running the script using an op.bin file extracted from the *server.s* disassembly we ran for 193941 steps before exiting:

```
> ./checksum.py op.bin
PC = 00000110(00000440) OP: 0000006b 0000006c 00000036 00000010
        op[00000036] = op[00000036] + op[0000006c]
PC = 00000114(00000450) OP: 0000006e 0000006b 00000036 -0000004
        op[00000036] = op[00000036] + op[0000006b]
PC = 00000118(00000460) OP: 0000006b 0000006c 00000036 -0000008
        op[00000036] = op[00000036] + op[0000006c]
<...> 
PC = 00002878(0000a1e0) OP: 0000006e 0000006c 0000006e 0000001c
	op[0000006e] = op[0000006e] + op[0000006c]
PC = 00002894(0000a250) OP: 0000006e 0000006e 0000006e 0000006e
	op[0000006e] = op[0000006e] + op[0000006e]
Ran for 193941 steps
Output: E6F7E7EEEBF5F6A2E8E3F0
```

Ok, nice! We are well on our way to trying to find the coords to give us our null checksum! Or at least we thought we were...

### Adding Input/Configuration Data

The basic simulator pretty much just covered null data. Lets add in the code to insert the coordinates, the checksum, and the constants following the actions of *breakdown_coordinates()* and *execute_operation()*.

First, some additional constants to specify the offsets into the op data. We included both byte offsets and offsets in 32-bit words, since the VM operates on words not bytes:

```python
COORDS_OFFSET = 0x3f0
COORDS_OFFSET_PC = COORDS_OFFSET // 4
COORDS_SIZE = 4 * 4 * 2
COORDS_SIZE_PC = COORDS_SIZE // 4
CHECKSUM_OFFSET = COORDS_OFFSET + COORDS_SIZE
CHECKSUM_OFFSET_PC = CHECKSUM_OFFSET // 4
CHECKSUM_SIZE = 16
CHECKSUM_SIZE = CHECKSUM_SIZE // 4
OUTPUT_OFFSET = 0x244
OUTPUT_OFFSET_PC = OUTPUT_OFFSET // 4
OUTPUT_SIZE = 0x2c
OUTPUT_SIZE_PC = OUTPUT_SIZE // 4
```

Lets hard code in some data for the coordinates and checksum for now:

```python
LAT_LONG_BYTES = struct.pack("<II", 0x11223344, 0x55667788)
CHECKSUM = binascii.unhexlify('01020304111213142122232431323334')
```

And insert the input data into the op data:

```python
# copy in the coords
for i in range(len(LAT_LONG_BYTES)):
    op_int[COORDS_OFFSET_PC + i] = LAT_LONG_BYTES[i]

# Copy in the checksum
for i in range(len(CHECKSUM)):
    op_data[CHECKSUM_OFFSET + i] = CHECKSUM[i]
```

The *server.s* code cleared some memory, but the op image was already zeros in those areas, so we skipped those operations. 

Ok lets run this and see what happens:

```
> ./checksum.py op.bin
PC = 00000110(00000440) OP: 0000006b 0000006c 00000036 00000010
        op[00000036] = op[00000036] + op[0000006c]
PC = 00000114(00000450) OP: 0000006e 0000006b 00000036 -0000004
        op[00000036] = op[00000036] + op[0000006b]
PC = 00000118(00000460) OP: 0000006b 0000006c 00000036 -0000008
        op[00000036] = op[00000036] + op[0000006c]
PC = 00000110(00000440) OP: 0000006b 0000006c 00000036 00000010
        op[00000036] = op[00000036] + op[0000006c]
<... never ending ...>
```

Hmm... oops! The simulator never exited the checksum loop. Ok, our bad we must have done something wrong got a condition backwards, and offset wrong, the sign of the compare wrong, something... Cue up and imagine the next few hours of hackers look at code through various online communication methods and getting depressed... 

This was the state that we were left in at the end of the live competition. Our simulator was going into an infinite loop and we couldn't figure out why! At this point in the contest we were pretty sleep deprived... or at least that is the excuse we give ourselves. :) We should have noticed that, Hey! The server also goes into an infinite loop on this input! But we didn't, we thought there was something wrong with our simulator...

### Debugging the Server

This part isn't necessary to solve the challenge, but a few days after the contest when revising this we were still convinced we did something wrong with the simulator. Staring at the *server.s* assembly wasn't getting us anywhere when we realized, hey the client has the server binary too! I wonder if we can't run gdb on the server!

```
# gdb /root/client/server
gdb /root/client/server
GNU gdb 6.3
Copyright 2004 Free Software Foundation, Inc.
GDB is free software, covered by the GNU General Public License, and you are
welcome to change it and/or distribute copies of it under certain conditions.
Type "show copying" to see the conditions.
There is absolutely no warranty for GDB.  Type "show warranty" for details.
This GDB was configured as "vax-unknown-openbsd5.8"...
(no debugging symbols found)

(gdb)
```

Nice! Ok lets run the server and get the client to join.

```
(gdb) r
r
Starting program: /root/client/server 
Start...
Socket successfully created.
Socket successfully binded..
Server listening..
```

Ok, lets hit CTRL-Z to suspend gdb and start the client... um wait hmm CTRL-Z isn't working... We initially did some terrible things to call server functions directly from gdb. Later we made up some simple scripts that we would echo into /tmp to execute the client after a delay and connect to the server process we started with the debugger:

```
echo "EPS STATE CONFIG" >> /tmp/cmd.txt
echo "EPS CFG ADCS ON" >> /tmp/cmd.txt
echo "EPS STATE ACTIVE" >> /tmp/cmd.txt
echo "ADCS STATE CONFIG" >> /tmp/cmd.txt
echo "ADCS CFG_POS 00000000 00000000 0000000000000000E600000000000000" >> /tmp/cmd.txt

echo "sleep 15" >> /tmp/runner.sh
echo "client 127.0.0.1 < /tmp/cmd.txt" >> /tmp/runner.sh

sh /tmp/runner.sh &
```

We would then start gdb and set a breakpoint where we wanted:

```
# gdb /root/client/server
GNU gdb 6.3
Copyright 2004 Free Software Foundation, Inc.
GDB is free software, covered by the GNU General Public License, and you are
welcome to change it and/or distribute copies of it under certain conditions.
Type "show copying" to see the conditions.
There is absolutely no warranty for GDB.  Type "show warranty" for details.
This GDB was configured as "vax-unknown-openbsd5.8"...
(no debugging symbols found)

(gdb) b executor
(gdb) r
Starting program: /root/client/server 
Start...
Socket successfully created.
Socket successfully binded..
Server listening..
Socket successfully created.
server accept the client...
connected to the server..
##############################################################################
#                # RSSI -80dBm               .-"-.         #                 #
# EPS STAT:  [1] #                          /     \        # OBC STAT:  [1]  #
#   COM  PWR [*] #                 }--O--{  |#    |        #                 #
#   OBC  PWR [*] #                   [^]     \___/         #                 #
#   ADCS PWR [ ] #                  /ooo\     ^\           #                 #
#                #  ______________:/o   o\:_____)________  #                 #
#                # |=|=|=|=|=|=|:A|":|||:"|A:|=|=|=|=|=|=| #                 #
#                # ^--------------!::{o}::!--------------^ #                 #
# COM STAT:  [1] #                 \     / /               # ADCS STAT: [3]  #
#                #       ____       \.../ )     ____       #                 #
#                #      |\/\/|=======|*|=======|\/\/|      #                 #
#                #      :----"       /-\       "----:      #                 #
#                #                  /ooo\                  #                 #
#                #                 #|ooo|#                 #                 #
#                #                  \___/                  #                 #
#                # LAT: 38.897789      LONG: -77.036301    #                 #
##############################################################################
# HELP  ADCS RST  ADCS NOOP  ADCS STATE  ADCS CFG  ADCS CFG_POS  EPS RST     #
# EPS NOOP  EPS STATE  EPS CFG COM RST COM NOOP COM STATE  OBC RST  OBC NOOP #
# INFO:                                                                      #
# ERROR:                                                                     #
##############################################################################
<...>
Breakpoint 1, 0x000120f7 in executor (17166336, 41572)
(gdb)
```

We could then start debugging the executor. We double checked to make sure our code was working correctly. Both the simulator and the formatting of the input. We had one issue, the 4 32-bit words in the checksum are being byte swapped. Simple enough change.

But still infinite loop.... but the server also entered an infinite loop! Checked the state of the checksum calculation on the server and the state of our simulator and they matched perfectly... Nothing was wrong with the simulator! Just that the checksum calculator enters an infinite loop on most of the inputs! Who would have thought that?

### Solving the Challenge

Ok, so there are two constraints we need to meet to solve the challenge:

1. Our input must generate a checksum where the leading byte is 0x00.
2. The input must cause the checksum algorithm to finish in a reasonable about of time.

We had one run, where the simulator did successfully exit, let's go back to that state. This is an input of all zeros:

```
ADCS CFG_POS 00000000 00000000 00000000000000000000000000000000
```

We double checked on the server and that input did result in the simulator exiting and via gdb we could see that our simulator calculated the same output value `E6F7E7EEEBF5F6A2E8E3F0`. Ok, so we are satisfying (2), let's work on (1). Let's see if there are any operations that operate on the first byte of checksum and lets modify the logging of the script to only print out operations that are updating the first byte of the output:

```python
    if op2 == OUTPUT_OFFSET_PC:
        print("PC = {:08x}({:08x}) OP: {:08x} {:08x} {:08x} {:08x}".format(pc, pc*4, op0, op1, op2, op3))
```

Now when we execute the simulator, we get a list of instructions that had updated the output:

```
> ./checksum.py op.bin
PC = 00002364(00008d90) OP: 0000006c 00000023 00000091 00000004
PC = 0000245c(00009170) OP: 0000006c 00000022 00000091 00000004
PC = 00002554(00009550) OP: 0000006c 00000021 00000091 00000004
PC = 0000264c(00009930) OP: 0000006c 00000020 00000091 00000004
PC = 00002700(00009c00) OP: 0000006b 0000006c 00000091 00000010
PC = 00002710(00009c40) OP: 0000006b 0000006e 00000091 00000000
PC = 00002710(00009c40) OP: 0000006b 0000006e 00000091 00000000
PC = 00002710(00009c40) OP: 0000006b 0000006e 00000091 00000000
PC = 00002710(00009c40) OP: 0000006b 0000006e 00000091 00000000
PC = 00002710(00009c40) OP: 0000006b 0000006e 00000091 00000000
...
PC = 00002890(0000a240) OP: 0000006d 0000006c 00000091 -0000154
PC = 00002890(0000a240) OP: 0000006d 0000006c 00000091 -0000154
PC = 00002890(0000a240) OP: 0000006d 0000006c 00000091 -0000154
Ran for 193941 steps
Output: E6F7E7EEEBF5F6A2E8E3F0
```

Those are a lot of instructions! But, none of them directly accessed our data... The input data has offsets from 0xfc - 0x107. Most of the instructions used offset 0x6c and 0x6e. Thankfully, the values at those offsets were zero, so those instructions had no effect on the output value.

Hmm, nothing we control here yet. Guess we have to go up a level, maybe there are some instructions that updated offsets 0x20 - 0x23 first? Lets add more parameters to the logging starting with logging any writes to 0x20 as well:

```python
    if op2 in (OUTPUT_OFFSET_PC, 0x20):
        print("PC = {:08x}({:08x}) OP: {:08x} {:08x} {:08x} {:08x}".format(pc, pc*4, op0, op1, op2, op3))
```

```
> ./checksum.py op.bin
PC = 000002d8(00000b60) OP: 0000006b 0000006c 00000020 00000010
PC = 000002dc(00000b70) OP: 0000006e 0000006b 00000020 -0000004
PC = 000002e0(00000b80) OP: 0000006b 0000006c 00000020 -0000008
PC = 000002d8(00000b60) OP: 0000006b 0000006c 00000020 00000010
PC = 000002e8(00000ba0) OP: 0000006b 0000006e 00000020 00000000
PC = 00000398(00000e60) OP: 0000006c 00000107 00000020 00000004
PC = 00002364(00008d90) OP: 0000006c 00000023 00000091 00000004
PC = 0000245c(00009170) OP: 0000006c 00000022 00000091 00000004
PC = 00002554(00009550) OP: 0000006c 00000021 00000091 00000004
PC = 00002640(00009900) OP: 0000006c 0000006e 00000020 00000004
PC = 00002644(00009910) OP: 0000006c 0000001f 00000020 00000004
PC = 00002648(00009920) OP: 0000006c 0000001e 00000020 00000004
PC = 0000264c(00009930) OP: 0000006c 00000020 00000091 00000004
PC = 00002700(00009c00) OP: 0000006b 0000006c 00000091 00000010
...
```

Excellent! We have some writes to the 0x20 and one of them even used one of our inputs!

```
PC = 00000398(00000e60) OP: 0000006c 00000107 00000020 00000004
```

Lets go change the value at that offset and see what happens:

```python
op_int[0x00000107] = 1
```

```
> ./checksum.py op.bin
Ran for 193566 steps
Output: E5F6E6EDEAF4F5A1E7E2EF
```

Nice! We changed the value of the first byte (subtracted one from it) and the simulator exited! Since setting offset 0x107 to 1 caused the first byte to decrease by one, lets set it to 0xe6 and see what happens:

```
> ./checksum.py op.bin
Ran for 107691 steps
Output: 00110108050F10BC02FD0A
```

Excellent! We have met our two goals, null byte in the first character of the checksum and the simulator exited!!!!

Now we just have to format the **ADCS CFG_POS** command. Lets just make the script do that for us:

```
checksum = op_data[CHECKSUM_OFFSET:CHECKSUM_OFFSET + CHECKSUM_SIZE]
print("CMD: ADCS CFG_POS {:08x} {:08x} {}".format(0, 0, hexlify(checksum)))
```

```
> ./checksum.py op.bin
Ran for 107691 steps
Output: 00110108050F10BC02FD0A
CMD: ADCS CFG_POS 00000000 00000000 000000000000000000000000E6000000
```

Armed with the command lets go run it against the real system! Infinite loop... Dang... What's going on? Back to gdb, checked the input to *executor()*, oops! Byteswaping. The *server.s* disassembly used strtoul to convert the checksum in 4 32-bit chunks. VAX is little endian so this byte swapped our data. Quick change to emulate the byte swapping:

```
checksum = op_data[CHECKSUM_OFFSET:CHECKSUM_OFFSET + CHECKSUM_SIZE]
checksum = struct.pack(">IIII", *struct.unpack("<IIII", checksum))
print("CMD: ADCS CFG_POS {:08x} {:08x} {}".format(0, 0, hexlify(checksum)))
```

```
> ./checksum.py op.bin
Ran for 107691 steps
Output: 00110108050F10BC02FD0A
CMD: ADCS CFG_POS 00000000 00000000 000000000000000000000000000000E6
```

Success, at last!!!!!

```
COMMAND $ ADCS CFG_POS 00000000 00000000 000000000000000000000000000000E6
##############################################################################
#                # RSSI -80dBm               .-"-.         #                 #
# EPS STAT:  [1] #                          /     \        # OBC STAT:  [1]  #
#   COM  PWR [*] #                 }--O--{  |#    |        #                 #
#   OBC  PWR [*] #                   [^]     \___/         #                 #
#   ADCS PWR [*] #                  /ooo\     ^\           #                 #
#                #  ______________:/o   o\:_____)________  #                 #
#                # |=|=|=|=|=|=|:A|":|||:"|A:|=|=|=|=|=|=| #                 #
#                # ^--------------!::{o}::!--------------^ #                 #
# COM STAT:  [1] #                 \     / /               # ADCS STAT: [2]  #
#                #       ____       \.../ )     ____       #                 #
#                #      |\/\/|=======|*|=======|\/\/|      #                 #
#                #      :----"       /-\       "----:      #                 #
#                #                  /ooo\                  #                 #
#                #                 #|ooo|#                 #                 #
#                #                  \___/                  #                 #
#                # LAT: 0.000000       LONG: 0.000000      #                 #
##############################################################################
# HELP  ADCS RST  ADCS NOOP  ADCS STATE  ADCS CFG  ADCS CFG_POS  EPS RST     #
# EPS NOOP  EPS STATE  EPS CFG COM RST COM NOOP COM STATE  OBC RST  OBC NOOP #
# FLAG=flag{xxxxx..................xxxxx}                                    #
##############################################################################
```

### Code

The simulator code is available here: [checksum.py](https://github.com/ACMEPharm/hack-a-sat-ctf-quals-2020/blob/master/Vax%20the%20Sat/checksum.py) and the [op.bin](https://github.com/ACMEPharm/hack-a-sat-ctf-quals-2020/blob/master/Vax%20the%20Sat/op.bin) required to run the script.



