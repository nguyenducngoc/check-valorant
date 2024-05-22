from winsound import Beep
from colorama import Fore, Style, init
from mss import base, mss
from PIL import ImageGrab, Image
from ctypes import windll
from time import perf_counter, sleep
from os import system
from keyboard import is_pressed
from hashlib import sha256
from random import random
from json import load, dump
import keyboard


__author__   = 'R3nzTheCodeGOD'
__version__  = 'v2.0.3'


S_HEIGHT, S_WIDTH  = ImageGrab.grab().size
GRABZONE           = 5
IS_HOLDKEY         = True
IS_RUNING          = True
HOLDKEY            = 'shift'
TOGGLEKEY          = '`'
SWITCH_KEY         = 'ctrl + tab'
GRABZONE_KEY_UP    = 'ctrl + up'
GRABZONE_KEY_DOWN  = 'ctrl + down'
MODS               = ('0.3s Delay', '0.25s Delay', '0.2s Delay', '0.15s Delay', '0.1s Delay', 'No Delay Full-Auto')


class FoundEnemy(Exception):
    pass


class Config:

    base = {
        'Grabzone'  : 5,
        'IsHoldKey' : False,
        'HoldKey'   : 'shift',
        'ToggleKey' : '`'
    }

    def __init__(self, configName: str = 'config.json') -> None:
        self.configName = configName
        self.config     = None


    def createBaseConfig(self) -> None:
        with open(self.configName, 'w', encoding='utf-8') as f:
            self.config = self.base
            dump(self.config, f, ensure_ascii=False)


    def cfgLoad(self) -> dict:
        try:
            with open(self.configName, 'r', encoding='utf-8') as f:
                self.config = load(f)
                return self.config
        
        except FileNotFoundError:
            self.createBaseConfig()
            self.config = self.cfgLoad()
            return self.config



    def cfgDump(self) -> None:
        with open(self.configName, 'w', encoding='utf-8') as f:
            dump({
                'Grabzone'  : GRABZONE,
                'IsHoldKey' : IS_HOLDKEY,
                'HoldKey'   : HOLDKEY,
                'ToggleKey' : TOGGLEKEY
            }, f, ensure_ascii=False)


class TriggerBot:

    def __init__(self) -> None:
        self._mode       = 1
        self._last_reac  = 0


    def switch(self) -> None:
        Beep(200, 100)
        if self._mode != 5: self._mode += 1
        else: self._mode = 0


    def color_check(self, red: int, green: int, blue: int) -> bool:
        if green >= 0xAA: return False
        if green >= 0x78: return abs(red - blue) <= 0x8 and red - green >= 0x32 and blue - green >= 0x32 and red >= 0x69 and blue >= 0x69
        
        return abs(red - blue) <= 0xD and red - green >= 0x3C and blue - green >= 0x3C and red >= 0x6E and blue >= 0x64


    def grab(self) -> Image:
        with mss() as sct:
            bbox     = (int(S_HEIGHT / 2 - GRABZONE), int(S_WIDTH / 2 - GRABZONE), int(S_HEIGHT / 2 + GRABZONE), int(S_WIDTH / 2 + GRABZONE))
            sct_img  = sct.grab(bbox)
            return Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')


    def scan(self) -> None:
        start_time  = perf_counter()
        pmap        = self.grab()

        try:
            for x in range(0, GRABZONE * 2):
                for y in range(0, GRABZONE * 2):
                    r, g, b = pmap.getpixel((x, y))
                    if self.color_check(r, g, b): raise FoundEnemy
        
        except FoundEnemy:
            self._last_reac = int((perf_counter() - start_time) * 1000)
            keyboard.press_and_release("L")
        
            if self._mode == 0: sleep(0.3)
            elif self._mode == 1: sleep(0.25)
            elif self._mode == 2: sleep(0.2)
            elif self._mode == 3: sleep(0.15)
            elif self._mode == 4: sleep(0.1)
            elif self._mode == 5: pass


def print_banner(bot: TriggerBot) -> None:
    system('cls')
    print(Style.BRIGHT + Fore.CYAN + f'{__author__} Valorant External Cheat {__version__}' + Style.RESET_ALL)
    print('====== Controls ======')
    print('Trigger Key          :', Fore.YELLOW + f'{f"HoldKey [{HOLDKEY}]" if IS_HOLDKEY else f"ToggleKey [{TOGGLEKEY}]"}' + Style.RESET_ALL)
    print('Mode Change Key      :', Fore.YELLOW + SWITCH_KEY + Style.RESET_ALL)
    print('Grab Zone Change Key :', Fore.YELLOW + GRABZONE_KEY_UP + '/' + GRABZONE_KEY_DOWN + Style.RESET_ALL)
    print('===== Information ====')
    print('Mode                 :', Fore.CYAN  + MODS[bot._mode] + Style.RESET_ALL)
    print('Grab Zone            :', Fore.CYAN  + str(GRABZONE) + 'x' + str(GRABZONE) + Style.RESET_ALL)
    print('Trigger Status       :', Fore.GREEN + f'{f"Hold down the [{HOLDKEY}] key" if IS_HOLDKEY else "Active" if IS_RUNING else Fore.RED + "Passive"}' + Style.RESET_ALL)
    print('Last React Time      :', Fore.CYAN  + str(bot._last_reac) + Style.RESET_ALL + ' ms (' + str((bot._last_reac) / (GRABZONE * GRABZONE)) + 'ms/pix)')


if __name__ == "__main__":
    _hash = sha256(f'{random()}'.encode('utf-8')).hexdigest()
    print(_hash), system(f'title {_hash}'), sleep(0.5), init(), system('@echo off'), system('cls')

    # Config Load
    cfg        = Config().cfgLoad()
    GRABZONE   = cfg['Grabzone']
    IS_HOLDKEY = cfg['IsHoldKey']
    HOLDKEY    = cfg['HoldKey']
    TOGGLEKEY  = cfg['ToggleKey']
    bot        = TriggerBot()

    print_banner(bot)

    while True:
        if is_pressed(SWITCH_KEY):
            bot.switch()
            print_banner(bot)
            continue

        if is_pressed(GRABZONE_KEY_UP):
            GRABZONE += 1
            print_banner(bot), Beep(400, 100) 
            continue  

        if is_pressed(GRABZONE_KEY_DOWN):
            if GRABZONE != 1: GRABZONE -= 1
            print_banner(bot), Beep(300, 100)
            continue

        if IS_HOLDKEY:
            if is_pressed(HOLDKEY):
                bot.scan(), print_banner(bot)
                continue
        
        else:
            if is_pressed(TOGGLEKEY):
                IS_RUNING = not IS_RUNING
                print_banner(bot), Beep(400, 100)

            if IS_RUNING:
                bot.scan(), print_banner(bot)
                continue

        sleep(0.0025)

#895ec936373eea4a4b0abccd187d56c8
#64e7f4db146ca16443d5ebc2ea1df5fa
#d85c0c8e3140ca71c092bb854b32589d
#4ca40413adbc9d75f543296dd53adead
#c5defbfa7f4d6ea5f167894d89af59ec
#eceaf43331bea0b76431fa4bdcaf18cd
#e11c208590ce28006cbef13d7cdfbd62
#4c1e6a58afde07225bfbed21b10cc7a7
#35ecce48291f8d3e3459bd1c1b5e3af6
#757b438ee84ac947d10936ca50e78599
#5fd23af04ceed4c2405a7c824bb04f0c
#f25cef69a0e274ced80f5d3338d93275
#aa0da243ca1561913d94f390d49d5dff
#67edcddb34c1dbcbf7be1849f32f76a7
#6dec5adb09be666b6b150eabb3784bd7
#f392db9291e9bc4646de27016a9ab9ae
#665599cdbeebe61c21c97f0c94a87667
#de35a571e988f38900ce8b077c7afcf1
#d2e2c57cb01e975dbb52025b26202b48
#a61d5b098c5c0f3ece56927dac8ba05d
#9896785f938283312b2c7767876035ae
#c4b7966e787758cf929a7c358faa9f77
#ba26354edaa1708cfa5b9508ffbf7a87
#68b9404046aa3fdf1d6611a00931ec4b
#a1c020fc785afb2694229d8478123289
#e25637742c15f7b616148d0bd1746697
#30f9284acd319b5d046773a8de60a8f8
#1d7931287cb55a9190fc43c6f4394c5d

#6e0dbe9f0ab5a8cefd25fead0673eaea
#4158c7ad2560ce6126cb5534c568d4b0
#22d46386164b056da229022246345c59
#dc725340770c8dae3d5613a47173dc20
#0657646e0235a58ab61c1768d9e9256a
#c3978818f50b1edcd745a428f38a6073
#8c174ac46dc9a402d870147bfb009554
#c6c4009b25d322cbab88d1acfe5ec863
#e4c0417e32dc578f5039dc7d2dcda851
#b70eb2e02bd90d4b5010fcec31fc0c3d
#f404518e959d00a7fed54f45255a36ca
#00292f225aa1cdfd08c36d679e64380b
#93c61a1dd9f109986ebbd29314f87deb
#b4e44b649cd2aa38f767a79333299436
#abb4270f441fff56992af207859045bc
#cde83d259b2fc3d40673406e3cca5f07
#a2b36676c9d88f743d3b53f0f83eece7
#a1c86669138aa494460eb4c518fbe316
#eebe7395a1d0f6a5056c6d507bacde8a
#9c5155e22d6c172150a979e9eb0a81e4
#87706ccc031f10af0ee0ceae94349174
#9c191efb7fc18d8e6b3b60e9ca9c2487
#444ce342f1094908cc3afef401330a82
#39c3a5f2490f767c738100e6faebe00c
#9621de1e02338d349051788cfc03814c
#46ab08253773e0b2887d3d9b1587280d
#2cc6c1391fdb7fb0f88158f485b31f94
#3de114edda34c071c1d9dcd50fb41bcf
#187afacac78c76fe0ef329ab3dfa16a0
#c18d0a447732697fa0d9f15b2c172861
#c14cb847b22901075ce61f1c327a8e2f
#1f2db83dc1cc97311c7150bbae6eb978
#e4ac1abe1e4b32efbb1f658d234a05f5
#88b5dd5ecdaa4004cf4ec6352b939f04
#75473374a93343581ac1c24a4a7fd393
#2f37510a27694bdb4fce81c7adc59219
#4d843654c8f6578873f4be3710680e95
#ca12d41f21b7b338af8e7458b1b3afcb
#e302f4e1eb6fb66321aa3e0072ae1985
#77be9b9883afc5a6670ce067b688d2b7
#9717fcb317a54ebc45657aab3ea91c77
#53c55002997d0490c252adba3c4daa4f
#8d1f65453346d4658770bcd23651d7ca
#7f23e9e7058ace8fc24cdb1d9990d66b
#bc81a4b5e7770e2209efd2be2426a3da
#863472f64496d9dbc3c5e0a56e54e749
#dd4e604321a10b64d85a3c8328f33db0
#026ee73c734e891177d04dfea3bb0b6f
#a5fecbe4d374669ff6c0b92b8e02d024
#d4fd72b90b30d014bcb6c1b42dfc367f
#ae61313ebd8bd9238133b2a7504ff4dc
#2eeb957c6be003ce590e3acc3bd5b75f
#f35ef12e6185014c8c2c566b5cb9b73d
#6def203de180d528f2c7e42764e592e9
#8ba5a42a09ba90ef532fd995d87e77e0
#03be015b2da3647146267e51a9598288
#2b28423046a8d2719662341ae1abb929
#6a44cf4ce990c17fc6baf6e52e4d9999
#a0abe1fc3f182c40d23ed2f2a28ff26c
#69b63a3e1cfde0e42cab044c6fb93c83
#3207b69aa045e7a66413f3c43b603df3
#868d54abed4a001d1ed58a50e6d88dc4
#b9f26b14f4f00d6b8a77a9a4bb7535e2
#a6700e69c083770b5c9ef2fad6f8ed6c
#c8ceb268819acf06b8f367481662cdb2
#a5a6a00d2b8e5fe0cb077076cb62b3e9
#258725131bfe1edfff4d407584122670
#0eca113f26975a9ce0b28edae01cb661
#dff49574c761691adf2a9e3c353ba957
#d4cc12043669a6b2e1d8c6d788c78b6f
#cd14b6a7e84d8749f34d3fa2e4385bbf
#049edc2eb6a92075a620fc8eae8198e8
#7444ae80ff64f6e417b779ea9b5c1c54
#56c66b73f627af8b09430038467df31a
#aed34e6fb09e2aa48a9237353b51ee8b
#0b5827d1a49e3d75f1cf931f4d95a115
#d504346287389f24c01ed250c4e5d291
#b883f0b18b3b22856fd881e90a033813
#f32fb87ddb70c4cc8c02a7769e69ac86
#64955d7854a38929c766a64e03ab5041
#1216153e5fbb26dd71b47cec91aaaa21
#61c03493d5bce7e67f57b0f6a4c92e6d
#43da717d4ea882b0b5858c6aa9a967ee
#7d0ab22ca8dce33841ae3f1605c2cbc5
#9207f405b05033e4f3defee60323018f
#a6bcd40a8ac4e9fa2450add69912489d
#1d966cfd25af6dcd1ce8daa7d1ee76e8
#700c4f7e7e1c657cb59bd41710d7ed35
#1e2cd52dddd6394741e532f38ab9523e
#6f6a00d79d83ebd55bb18de5a37792b8
#ec847ab7ace8cc4dfd6a502e3b845ef5
#e4d4c89e40c05b43199af7d47f70ccaa
#786a8032528e7bea74b16b18cb814080
#8439e9f6882dba5c8dae5dd0cc64b953
#fe3faf0dfe4b40a5912c30ddd5e4bfb4
#5a2ae06dabbf43bf9f1eb2383973ca40
#a3fdee949dde481fb5ae346940225fe1
#5e655b01c329c082cc53d2fa459f0849
#e3c721e9f97e408af1e02cdd39179cb1
#14b11e6ed103207ed31853e28da923e2
#8b1f314f1b86adc2ad93243df75e3b64
#f32302b3bf0137a48e7ad65e545bc7d8
#b2bcb6e92fa30fdc71a14886787b3a1d
#05a7e5c51d05823996ca1b6b8733202f
#1b3474be132f87b448ff92bf6e0cf495
#446b9ef72384c5a533d2018a4b2062cf
#7745391db566d498762d309c65385866
#551bc8e76e54387efd83399b1072cc1b
#45c84278cd2f3127be778c2aa10b7e88
#6de6650967db8b5c7a51f57ef9d8428c
#643be5147b3e20cb8554444d4f13382e
#80a15442bffe235b6060347013a01bc0
#79f55bcfc01a6f849738f6d350b51dd3
#9edc123634527c6a681887f28396f208
#cb4ca51ece025c2dabfced9f0412c33f
#f0cedb5f67e2561ab7a31964d6c8562d
#2e746a7a877c10f72d74af0973c98b95
#6f8a997f3db5948ea85546d0ff57c416
#7ca83cbba64a0616debbcfb2f1ed8db6
#4394ec6f90fa815e519755ad25ece6a4
#620fa634a159574c691412e16838cc26
#e5334f63d5eee8cf33db0629c04256c1
#14f9fbe3768455d59cebd1be52b8159f
#0dddf30f9642e3343f78cc102a3a6124
#a1ef8d0f368f4f059ed1a2c191dd6005
#cef2bdbb9e7a523346b90fde9c4ffc20
#279ea0f0559d059ac04d00f51cc723fa
#ebe05db3557438d6073eeb20acab2ea6
#019ce50d90be4f3aa6f37d0ab54a69e0
#c3b467afe4d10467a01c9446dd01e523
#710916c7afb76e738ccde6718844796e
#4afb1d26883297f44062f455e3e260c5
#1d6580214378b3d1930e65c04a95f6b0
#41c3f85b6403672d62cd0497644dfc5f
#14d114ec01e45d90a66606c0617c3fcc
#8f3a183f17e3dab5d54fe12e6b1cd3e2
#56bb86d270cc8bb08729084af38da2a9
#c845d3794f7da53cc2d7420f5a51595c
#66727b9503ec499550b6d1a7c66a94d6
#2dbd9151da6c1df8c0bbd84a9cf4ea3f
#7fd3f3b12c452ea85d974d4c81aca204
#f51aec4f21dec12ca38bff22ebde4402
#846d6d32a1157588ca1ff89c8f5c5de4
#eaef873587bbc5f26abe84d9be991ffa
#a834c580810515d7d0ccd027369f7648
#c0d7641a1042b7a0294ad986f12ddb3a
#1354b8cc83315924d935f97648c3d481
#453ae17a628f4aae6695758651b4a429
#32c473561f135245d121dbbdeb4dbd32
#7bf2c5efb2834089bf95a74e4dbcfd1c
#ab8a9b17ab5aa30c5806810eeabc327f
#7fc5a1adefc1fbe5be3e46a9d8daed83
#2663399d25b6ccfd643fffa1924c86fc
#3784f03bd348a789d59cc6b13897daa8
#709d368e8bb2ab0f2d55e8accc17a5a4
#a4356a5d43fdc52402bf79b4b5f5c0c9
#ad922a1998a883e331f928f9efccc04d
#45557bd74245826308cc1c72342d948e
#e3ffa3a132556d8c4b8ffe7bd79a0c3c
#afef78641e1e2f4ea6afe53a9055b53b
#6497e02eb09e9772e8888d280c2ae32a
#48f0a43b471ec1dfa9ce66c6fdf06437
#73ab48148aac28018f2ceea2a4d130c1
#d1f0ae64ebea134d77c4099f4f7072b9
#eaf452d4666841f4959da402decb9b5e
#6a461a76f5c28c345922c3624c105d57
#24edabcf5ed14a8b38fa7c4e6d455d39
#1f742aa55d2c49eb9bea3c909f0d9f40
#7ce44cbcfc820e4138967958e9eb8e9f
#b7284a7f5bede8ed79eb34bd6299621d
#a793629b00b2f8e5be65680ae21033af
#307c9b13fdd3cdba6ca9a83710d37f42
#ec15828af9eca96e5cbc68ad53acf4d2
#ce73c6121fb5353248fa1b1322a877e8
#69d33fde8c4233c8b843b7f21986ef1d
#dcc6900b1a8c8240ca4d6195fe879e57
#0c7fb695072d29fc59554a424658d86b
#ad9ae18cd4e78d788246cbfcb476b7d2
#b00e45abe9c1188b66ef5defc3754366
#35ee77bba512796263442b82964bf617
#705df33367659a56a436511aa3c4f812
#6857cdfacd6fd301d479f1923f5df382
#6c72fb02b9a54678731deb7d723fe538
#d857dd2b530762a1da628b3cd11dc417
#49afc4ea6436b3e5aca46032d685fdc0
#60c46d1786d5693664a5106490f7c359
#95a9ccba14f68e808b727bc90d44093e
#4c1d5032e45ebbbaf752028ec993431e
#aec6897ac10fe6e8bb7694c34f1e2c3a
#3bd894c867f33ceaabede45d7111597b
#637575dad89b5e0ed3d9e9dd1356edce
#1e6af73658d63d1bc7b2f97f20d51c4e
#3c2441576908c7cf67f1109a8b85ea9d
#ea0300cea6009e3b8644e8c3294d1ea0
#51c789ab0260118179c72304d20d4e4d
#33005593826a31f300b4de34f147763f
#e6d03b0a6d58666b3cf41dda0d39ff47
#a4f760b48b9c77f0b08469ed8623c607
#a6e644ff7f8789e75906996980b390a9
#dcbfe6edc44481404e53cab8eded7563
#fba439633259983c747313332e759394
#b690f510d729e422ba85f426a5f1ecd2
#848ee9d0c7b1cada23e86f84602aaa90
#8e7d968a2670fa2b5f6725d299e918bc
#03285d362a939b79ccabc3cbbafb1371
#5966343972099354e4a3f92810500ede
#bc18f90097610e6cc397437cb1f3241f
#48e5d0ad5343157823ff76209ecc93f1
#450d6842cab454d67f035224a7245b88
#cd1ebe3fee0d6368f58ce1fca3c1a6c3
#6937a0a96157c17e0e9b1eed9d845b31
#f4edcae6e248c2e8ac674b6ceb1fd872
#50ce443ca62a705a5bc28b78a7c3ca13
#aa04098f4d6738a3b11f3410912be171
#e0381db82f674dd40e188bcc52d97541
#64a8aa3404233a511368c890f1158f34
#bd5766e3f21c67b47418436e41f1759e
#5066d320935f2a485236bf7088bb6147
#03f3bb4b7cc5ee458d91553fb7d65801
#5032f2e125aa9e5a32d1ff0d3296a598
#22b6ae4a917791a1a6c44f0b3ebd11d5
#ffa4f0b786902852da22a47d2d9662ed
#4b58c72b88ccc793613b76be8c11439b
#a912232776d8c80cf31378a6fcad3e9b
#b3bced3c7c7f4d0639b2e05108abfe73
#54943597250f45069a16ce73e78b1c6f
#ca77362a6fb899ac96c85dce1c6c7074
#b5f83b53ea931bf7f8b2bed2b33ab561
#d4db6e39913328667d75ac5e6ccf8e12
#54489859723cc3fdc4dc73015a21d918
#b675e8e06a84fa5d49be0a994498e6cb
#5ac3c1ffc1425a001d90d5f1c141fc5a
#567bb3128556159072bd32acfdebf77b
#9285b1b7c24348e09f75c008a6575b6b
#0004035a4f20dc90de7f60b3fde497f9
#cc954fba00eda3f8f449059afa198509
#88abbf4609c5945bcfafe333c77f3585
#a771afc02bc1a634da2de4125938292e
#13f276befa282752f6cb03825136443c
#0952bec54d90b74990ff602f4683f2df
#6709015131771e12fd2b9c27f13155fd
#92137b71f22b6fa0de94f07a9e1f04a3
#ebad33f59dd8622e16ae1f5b1bbbf746
#3767c2ca9a0fa4fa438039ae0654f395
#86144b98fc5de9d00eb760536da08c74
#372b5f74953129d3624e801355b2ad9e
#7454c1ca58e516f1ca82d5eef41c65e4
#92d65aad5fbcdbe53947463ceca06b4f
#bbc4994ff686944b72e67043ce2c9a43
#542da7ac03d400bfd41dee958d60d4e7
#1a6ff1fb221d0a5f78634ff968d2a0a9
#fd6893fa20f0a71f0268e91388768a71
#66fd5c342af3d32c869344110fa749d0
#f92e23a7eb880bd52ffb96df38a0e8a0
#fb1394edf6ff7daea19f5dff3134b2ef
#424fbd51be9792e441695e625e67f414
#917988c8e927cbe4331212ff91e054b3
#99e73ddab7c96a16e6956257e021c884
#50ca165e0290b92b8189de47629b5872
#b03190f56378aa3c96b8c45f38f6fd8f
#19dce5ea7fca5b9df405950a9df2ca4f
#452d5cc14e94699bd5ee02669d6d6f4e
#b044d906ea32d8a2189c200edd25dd81
#bfe0868b4f07016ebd8636994deaeb88
#cbaa9d537fa1008064c7c63e8eca9935
#b2a2b1944c5c3de2afb90dfb8171ce01
#8ba3196f2b580ee78d08a5d4fe68c92f
#14dfae0e7385310c7b4164d5f910e514
#b985f9f93607cc30c9aaa88436de72af
#e2cb248511084bcd42fa1136b7f0541a
#43ea7533c5ebedf276783ab1ba1bc672
#edae5684b4bc5b0606c4ce0125a03aea
#8e69abe864d96751db2602de6adbb0d3
#01891acf713024cf47bb21c5e8f5cab4
#b5187e5922e8e7669604f6d7f91b0d6c
#56e1f61eacac8233ee615139fe44aa3e
#1bfc8abd294bb3d88af219f4bcf482a6
#820481da9f50fffa136032464a54a07c
#c67b35f2277a1961cc9504434e4f4684
#d43962c8674702586a7bc9f73116a023
#fe5b32c9dff99d0438ff00fa11777b3a
#2368e38347d4766487c6f00257521798
#acf8e6bc052088efeb02bfa51dd77569
#444cc6d1ca8469d19bac85a48f7c0b44
#5dfa1c6e35295c19bbc59b9c9f2b0d35
#e706f3c8ba598f185eeaa1ae430f2142
#bf1efa5c11f6a0a3f6980b0b370270cd
#936f746595c574677a02d847a05b8c90
#96f847860eeb241b1920a6e75aae775d
#ea950809d15d81aa3f77c22c5d1373fe
#5b6fced89af872e52d768739aaa7fd70
#2d19d8efa3b14176a24c19991c679750
#372705e956bd7a82f911bf39eabc7151
#d19489783147f9388993055f275ebd41
#492c972d5cf7e1361fa581dd052d935e
#a6b9365969f148066a8590fe8e143bfb
#05a1cca77edeb14d33895d265abfcb48
#63b2ad2303aae482b1a53d1ebe3d3bfc
#57cae31436854f245484bd097146c958
#65830de310edad89a25c2826e953ce76
#b6155cb2fdf83e652dc005867acb4fb1
#2831a6fdad87910405cb99bec8f030d8
#fe7694f07524b33d8be85080ce941482
#f27c6d56f3f647cf2ead87f508e2f857
#f3d641475066eb0960cfa98d94dc298b
#d041c4daf516424f2ce61b98a35ed94a
#ac9d4b2fac82a813fd811a4270848a6a
#494239987010d8118d1d256532b600c1
#d6c15814ce45affd8184f497e4b84155
#1849dbb1c23c486f188809b943704a20
#2f7a8ea91dd07471ca20d709bb9ffa2f
#104a659328197878bb2b47d460ae6b04
#28e7df8e1ddf32919e1e8c2b1516a068
#a191052f346b4bf55c379a9b63e4d485
#8dbd2c1dc5fc1542943d9124255b961f
#0304ac86ff18cc2baa55028de4919744
#ca3b10cf3264757402130787e2d98a1b
#f15e3f410557f809ba773a1123df0182
#0241f91d5d4e981be2d5e3db48c1e2d3
#d8cc2e23d847c213333129ffed380bf9
#2d9d8493fdcd8cad0be0ac89da2c1d86
#d0e09f2dc8135d98390a25e3e2ec3746
#99e9002bea89a273e259506a0b935ece
#3d905b9fbbe39b2fc3bdae20688bd7f0
#7d3de0eec283d6368258a7c521f3afdd
#03bd794398f32808f9e4f97a8f42920e
#7df576f2ce1a2729be1a2039a936c5c2
#25d90685bd4a9e0364f5cba06ad87390
#6cd926b687abeee24e6d25851051eedd
#40e25b6b0212f62a1d022e18a2b0fc02
#ff9aad396e614b14ea553cebbe9d1bbc
#f2c6babec60f2f01ed3bd7bff466e190
#f228e22e81928fbef7add082fe5f7312
#01aa94d20dded1d7000a6f670300344c
#f6312b6ca3743fd34db6f61a47812559
#102f8313041ed9afb84ecafde47ad562
#ebae9d28e3f954c970442c95bf197d51
#303d127211f9931d2483f33b5ec32915
#d74c9c67b97c56774798461ee1e03caf
#f9986562040470c3beba1c69ec71aa46
#f69eaab9e4b097fe2f790307304c6809
#7869441f89c633eefc451bc0aadee445
#d3c199407d6f7d3481aed45c4e56cab9
#27212eb2667b41cf67094b5038782def
#f4a5a5d3897d071874d19974f06ebec5
#21f2ae3c3a6d208a80e600876da42d73
#7daa3b8b3073f07b20f4bfec360ce41d
#3ec67046182bb5625702e92d8f3ff697
#c9cd91359ec4d91bb1ef0906030418c4
#f25ba72df5a60cd8f061815c007ee807
#6c88be593dd65fc1c5662c913369cbb3
#c121c6e9e5a87849cc9bec2a8b38b517
#794b5a513a575c6b67b8c250ca83c75f
#0222089b2757f4b715f6a1196f8e3809
#288e777ba386ec5f31f1fa8155e74f55
#f382ac584f15c1f139d1385c33658940
#e7d8c1869dca6d7521f7d2850aacf0b9
#d4b32c2d8d2a2a352cffd8902f00095c
#9be2b6809f131d1dcb007fd3b2a95b6b
#a69027305d984d8adf5a0cb8b45acf68
#daa5cbe689b70a59da8aceb21a90109c
#7d96d4f6ac4776020e15438f3bc85651
#c746b6f4e6c86e1184599d440fa3ab63
#82f33712d1d0a1f891a3d4daa0516c69
#378500428fc7f2193c5177cfaebc92e3
#1a150f1376ab4c251914efd8fd1c0dac
#3969679cd0b11ff58d98247b02ccf5aa
#feb078ecefce99abb0f109dd8b800c99
#316c7e05f70051900cdbc6f6e86fa9d5
#7b0328b51cd9fe76c2942eea8e908ccd
#9184573bba4a4be659c11eb6204096fd
#9dbd0b8374fa03c0a4b9a3c7f1bcd1f4
#47eba054821a127c295512495f510e35
#68a20c470e39182e409788d8236a8c68
#8e06146c0978137c8afc8e97d446ef13
#1b1f2b7a8364c9c23a1f65465f42501d
#ce20a29b82ca04b29468408a6a645e3f
#da9d30db7cd05dc685edb5b3a72eb58c
#0a45fe16b0ddf13c92934f036fb924db
#49f99ff02bd2072db2928a50c15b2bd8
#360a6953301128b5427a5e624c95e048
#6f1633768435a52c9fe236b330b24bd5
#30b5a6741ab75046e088878f158c8b29
#57c919f9771b3b920f02064fd2fd3f6b
#b4520ef2a4e2a5a80677aefea65977b6
#0d6e76b461082d2ca987c6190ad06146
#974b56d2980f7d76c07074078c8e7402
#eefac9ba4ca01d5693d7893f6bc3293f
#6f6278f07f932be1e6bb6cb3e8f84725
#3291994b35e9dd633954f548421d2533
#a4f9a314dd1fc81ccbd97d3e9da5338f
#9bc2c757ab218c24bf20af3dc61d676b
#fd11bab134e32297c7050c43d0cc1ad1
#0477c97be5031e4a04e4d193a14201cf
#c2629cf941d0099291d7884a86766d57
#8ef37423bf5a3286260019ba88742b5b
#043259007cb3b19cbf2b8becac9f2378
#f866bbb02f9cda7098ce719505d210fd
#266c1e27a00a3302db314190439849f9
#9578501297397b2782f3ca9633e23805
#4e2ecfaf00f27c35e5a58df1440cc46a
#0ecd73e8a9a00efa6298c4576d33da81
#1a859a00f15601a0e7de7438dc2030d2
#50edf63c42975cfe6435465b3056c788
#ea605567e6a7e369084300b035e6500c
#64d6dfb9bff6c6f03412dd0322c56622
#4ff1e1ae8c5a878ccf5d2421baa761c9
#5443fb598c54258f262b63c918e691e4
#df278bdcdb99b87a008ace09d72af259
#1593e946e68a6b366b69509b346512d8
#c5d52246ba2431edcac81c10fade1a04
#055b7f57032d60914e3d75f1530b504b
#d08bc10a61d27df06f7665a0a895a631
#8b1f2b4dd9559efef4239636d4f00574
#f3a11c5241dd244570d7afab01cdac66
#53786c304c6f7e50bd15c8baff4c8086
#1e11627c79a352bb7f0c32af65059b22
#5255fe929cdf39ae166bf20546d86937
#647113829b08d61c4ed061011bd4d757
#69698ff4d47f5ca116e4a2d9a1d1b933
#63e935f813dfa8567118855c46c5e642
#0e16910ca9792d95c17516e5cdfe1428
#fb244158823016b812df6ad3c40d3ac5
#438207e97b013336fe04f139ca83bd2c
#13281f05d8a90df46d71ded44e45dcaa
#7adab523dd68081abeea11f4ed76cf8f
#4fe61fd1c1af4f40a4de86b0bc12e0d7
#721199e7566e6143b3db95f6396541da
#d1ee6fe782199342a1896eb1f09cf81d
#ec0e3e4023f09103ce1448afdc4dad07
#05eee8a7e504a3919b5f30a6be045160
#6560d5b0b8d642d16ae3b5478117643a
#7aa23533d2057083ed122b6ac7e2b2be
#04fdd4681f0ab65a53a76ae36f7fcce0
#658b24b787c1709efd546c17bca68c53
#48f4bc083767b1aa7edc02528ce60a61
#663a669cfb5a356cc0706d0e22c658f9
#98a0999d637ff5678d0ee5be4acf023f
#8d7029ed04401e0ff4637d8441478da7
#6d4a696ffe352024ceb203a0cfec64e9
#f7d4da13a7cf1f18804bfdf5963ed42a
#620e0ea7d441d1939d7d49ea974ef974
#8fdb36a6d7f42279227f986ff258c554
#3f77da1df7b349fe54a2a340c113b0ce
#628fc803657d134ee3823d1380048e33
#df29c4a6685856b615343f45f7a1e056
#54afac7ed1815d28e1fa0d2fcc108982
#f32ae5528929208c14743aedd2d9e36b
#b77f2da21120ed21f9fb7007b19171b6
#1adca09eb2877ff4dfe87f556f7f54d3
#73963c91437e76e1c1cb6ef372089c42
#eb1bf4bef20e9685afee2f3b46976753
#1a0b0cab5d8388563eb01482634ecf12
#c7076035e428d8be00632565c99404ee
#142fd11903ff184266de803b54314b88
#b5ac8a1f1fc63b1a269d83cc9736a452
#aefc106c995bbd568621a63c1af660ea
#66640738a2856dcfd555d9f949bcae24
#eb8a26a229bb3586e1b2fcc929294d84
#54e9d462765b81d3e5485782643eff14
#942748138c9a9e53fbfb72ac8c71e57d
#ae34e0c3bc60e9697b04d2944ae87e0d
#1b0dc30c135034f09f811e2723ab433b
#5748e65cdea769bb7491f30522ecaa87
#31f34b48c97043c638f543c6046bc8f7
#d7790298308a4ee7b5832370fdf878ef
#e43bea554eb91ad7a016273b5f258450
#b406f02860927b26c5cd675618906990
#84311a3de6ece96c292b5a4c7b283df6
#f6cd816a2a5280e2dc133a2eaab8824e
#f718ed2726635b494126a02df011524b
#ddc0645276c3fa2b74c0bd3fae1eef69
#658f25841c3a8209446d836e6997088c
#74dc3264f571fa5e230962300ecf23ca
#d618280a98ff0bb2863f41dab1cc2103
#1e4dbd61ed25fc0827e682a2a6b4a12c
#e4359f4b74cce57663a3a31b3d60b9f5
#ae1e19c4d7900f04c7b3a25fca516be4
#69266c22e4c43c50d93ae8f7eabf3e3a
#cbf308d2abd99ab371eb7588fd0b5c59
#e13be6fbf1df33b3f9c89b3705b1e25a
#5234cfe13aa362d3089506303e2dd7ef
#0738d3fbf4cd95d10ae37c1836360dd1
#e6308d1b10d7b7805ce6f228ca113885
#a0192481f1a3e8eecbc80aeb741ccac7
#cb839f30ece8d7b932f2b5ee71aa92b9
#4c4e39645077471d90ef9d6144db44e1
#e323ea78bfc9dc862f858da37283072d
#580681785277ca88a63af3eb83fe0159
#cf9665cc314674a9214f1a3d2126faad
#858d020ca73f9092c70307c31957fe33
#fcb310a5513f92eb3a14ef6082fb96ee
#4c3478d52eff47c934646f8d3358f124
#880762ab74c91746b667ec05d68dff9f
#ec6c9e7b49fdbb6ddc5968e2829be33f
#c3ae43c9845a7d85f972698f2b166a78
#f030783cda372cfc49a237d195483992
#a2fbbef2a74e3f73447259c85ae2b731
#d2af23f46c2ab4d33200a133b372c53f
#73d65b271be6a1a31b956ed3fc372e16
#8cba5aae83e9f8a06764f55bbceafc04
#90c7da33399e2912266bffe8036278e8
#2a6c4c3b9b1f387f8e6464c70092c599
#ebee1f3695aa4ee0113334ed246a1792
#a826b48351585ece401f253552df06b4
#39661144a5c1868a6a78d1df486376ea
#aaa900795b8f2e4a8c574a73a6f05e53
#f7dedc82cfb22aee269191d67870a882
#012a4b220b6e88bb99d9cc298dc1c04a
#824ac6d8103cfbb4ec1835f8a94b1a37
#8c2829bbb8580b9cf0f084b3458b728a
#a9baf469a294a00ae1435e710736d368
#de91e4eecb2633d5884a29dbe9069916
#128d2e1edb022c7fdf7e9001772096de
#54fee735cb5df663bda5736d7a032c46
#4448d411b26f321481699c480effacd2
#7eff60089d0a4b6aae215c441e4046a5
#dd40f20da82c62c4985d5735d157045d
#3309614362dcf4195db68b4f4c5e66d3
#44e784c711c4e91b9f101ba6f18ef47d
#183caf79921d6387bb79b9dd75f70bb2
#624e5d536091016372204fc1d32b74b4
#20ff21ad5cd44deeff1d33ed0c951b03
#6d544411342d5860584004f40906c476
#d1ab4477242ab72ee60d8ac1f0c8815d
#d64158e0ba29a0633af9786729290887
#43aee43a75e67b87894be76a0a460297
#719a1646c418683c61ddc6b5e171d7a0
#8f207a58137355e2b94851633ec8b6d5
#7504df53693f3da6f18b47519797c068
#f1b1d3f02fa207c8e35f5095248020ea
#7f42501f37c0854e484b65dc2e397f17
#fa27d10fd9b800160174184c978e5522
#e5bec0610cfef6a8c27121cf3b10e2db
#6c723552143b4560e9b6044cf5811e83
#0a1289af41d154e46bcc6b88352c4e86
#a44f0acb358c619f2f6a01976f2bcd49
#ec3dc39dc859da101af7efe3f805f5fd
#39f9b8da26ef279e3e42d830b1ee3e76
#a60cc2cad882e7a2f25ba143b848e63b
#62a5f6d0a71797de3df86a5571953a8e
#af38f6b2b572a7ede5a1b900b1b72628
#44f236a4f17f0f0cbeed632530c5487f
#8036334a8be65491b3238a1b8a84f1bb
#39b388eeb04a51855a17cc96182e7a3d
#f42d7aa3d36378ef355cf4a8fe9da68d
#5674ca72f7afd62664fd6903a51f1680
#506530df933e4727694c122b07470cf0
#c9202c2fbcdbd49e77e64cf3a769b177
#da0e07c5554c658119d6ed0f7fd104fa
#18aae571e89d9a0cef57cd86a69b05dd
#928ad750d83bdba6c599f7116b373e0a
#5367a8c81057a0edf8b7e517a6d9c5d8
#43289a717cb7f6d69bb8b2457077d642
#65c5b00d383585c9d96883a74e545f91
#148e9ddf2aaead04bca61359cd1d5fc1
#1997c636b70195fda27d9e5b3d78eb6f
#38bc7662a97beaade110b2e711e9a376
#2e540c14da371042efdef0d27145c374
#598fa3261a95f0f24ed8eaf922690ec2
#b9b1539f3d5f60bb5a7138854effda3b
#d2e621d794ca1d2832679d88ccec3674
#22b84d92efb4971710c140e08d1150cf
#3e545e8ccd2e61e36a2f5d06e64a00c8
#1c0f7899bd7af22aa98fc5c2fa8d30f1
#3d8193b56445ab387887046e1bef5cb1
#423cd73e0deaf07775f8f1db96adf065
#af01dde3ac2d6c833470f558e36004f2
#5d31f0771769752b3bcf93fb6720732b
#a30c1521a92f673a51b2fe10d6fd088a
#603deddf55202b5f501bd172aab4eff8
#522172e2ab7db9f0ae94cb8aceb1f8e0
#ddacea7b9fe73acaef9d433dd0675efc
#fd383ef9f68904aa20ec7af4a09f5c7c
#c0e35ce1c5636c538841a82ed52ab11f
#e9dc2c738a7c57284069343b41288474
#ab78bb77353e34f22cb8fe67d254003b
#60b6ae6e79e53d844a896f8c14d97bc9
#ab852e22c2e590905b47b2be1de5ab55
#9dac2591fa4208ab727718d789c2203b
#ddb1c86e66452ac13462143dd7e7eb1c
#b2db95cdeb07edcd19c18e71475ff28a
#d90ea8d8423a9d1cf9f71af28d71364c
#df0e3ea29b9a47af42b0ede1437252e1
#0347c923320c1b7fb2648192a050f176
#45c0737253285624cfb6029622a01863
#8b1cf5a173cf35747d20eae70272bdef
#a33ec67a2ab906a54cc9df011c4d7143
#a6a30147111e3c523bec09f7551c15ea
#2f5c1538d5c04d5b7c950855922e380f
#7569f0cc08d0b798ea21d619ef90b39c
#1111a094509647c3f2d568eaa7ccf07c
#3152781b4c201b7e732f31285152e99a
#117a22babe1a7269d434794476373759
#879feee696983fc7c5498b7386413f58
#52f7355e3ace46463a0f3ca8a226a762
#dabfc9117160ad04cff59578b97fed4e
#0bc915883a041e62925c32c6587ff8b6
#b33f4451cbabe48d8d6c825b1687939e
#767ae9a9bd09dab52d3c12b9535c4b68
#da9644b179fb261ff496faa1c49e3da4
#78297b9805b59a55cb12eba7d102bce9
#a72e21844b6a2875f07f982c419a8bbd
#91afdf804b9f224693123d7a7a53ea28
#b8430ea1ec03cfa43382397894f0e930
#570efcf5f72568e880f3e07b6f4d8c11
#0fa4adce5443f119a69ac759d28337a7
#ec1875575dc135877377bf87d65d6adc
#a5e464482c81851b5d69b85af576ff03
#6eabb9e05287e00075473cb982e37d3a
#762909bd3b8dc437809818b9e6b750ee
#044802772cbe76bf5f066e9e96c0f613
#740beb90933860bfd7078433be94a211
#6cac4e48b4fda753c2e4401bc7713976
#94f922510b9071fc16c359f4456ec51b
#45e0e1fc76e9fd6acb03ad292270637b
#2c47fedbebb78ee32e3d88e0fd310d99
#a97cc61f4e28f29f0f252811ec650953
#ebeb644327f23a0d973a912a4c9190bf
#fdbb090c1d736f918a6507febac76c7f
#0dcb9e8cd254b9d87c9401851b715612
#f0586fad773a9fd4a80b813dfadd32ae
#723f79bed23dc58b5d189d9ea2709951
#1575134d37a159a00d119f9e69b0d496
#7c4da88b09bab19a66e4926e693b1372
#2c311cd725e9ac2a705d255d928df2ae
#3a98b19d0d9e59fd9ead7068986f2948
#7f8948e94081dc53f9c83837f0e3b3e3
#510ba5bab5583d45835e23e18d90708c
#72cf8f5458f02f558efb48b8688be7d0
#2138e4dc819441e2b5a2d8a73a66d485
#a895abcc6f50037d1d620383f39c1fe2
#d8154299de4981a22b28162299fda24e
#e9a1ed210b72f4b6d5d896e0b3d96c08
#4cac80d547a1446189b21b9292bdcbf7
#1619e61c323d64683149e168854fb3d4
#837019e57092fd7924245004fc24cc88
#5fbbc4ca1048806a0841d0504cfc26f2
#cd9510444479730d468a6b51f48e7f39
#d79ab5d74e6cbb1eb7ca9db7892893ea
#6b49e2709e23a5ee18720fe26ca4b58c
#f953a56a0bd3dcfea38f771c1e324628
#8c8bf2a01936a2d4ab5d34a3ff461cc2
#44014e9f74af32b1dd75f356480161a4
#48d775f09fb6ff07d7a6b1eb41a336be
#7e8a605c192c75b8b08bbaabcb1795a5
#3876838524b57ec0e5665112fecf1f91
#6ef1f44edb333801e893171ecc6aad6a
#5125c12777b7069177689a1bd2452649
#d1f903c20cd78ed29679d6318c4374c1
#6dbe064463904c07de36a5e6b6b7c5ae
#6583ab81d41fa5cfc4edd53d5bc1fa1a
#09055d168144eed30728cbe44c9cd46b
#2065df1cf1e2944ccf49c2ac573a1295
#a8ecca679b5521ab948c69ea418b51f0
#5cecea505eaaf9f9f75849e94d9ea022
#305d4ff1c0dac0d492f1fb859895818c
#0ef5aa52daeebd302b1483a7649a2980
#50c590bf427d364f67fb3ae1b6c7c1ed
#58a5060a41d65d0d67bfec0c3d358123
#942794e99be1f4f14452131d357162c1
#c30d9a1b865fd32c1277534ec09c7de8
#112d7455bcbb145260651fd12e6eaf25
#e808c6bd5d4d32eda1746f72daeda0d8