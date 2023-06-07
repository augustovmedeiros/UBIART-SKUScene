import struct
from py_ubi_crc import getCrc

class Serializer():
    def __init__(self, fs):
        self.fs = fs
    def uint32(self, integer):
        self.fs.write(int(integer).to_bytes(4, "big"))
    def float(self, float):
        self.fs.write(struct.pack('>f', float))
    def string(self, string):
        self.fs.write(len(string.encode('utf8')).to_bytes(4, 'big'))
        self.fs.write(string.encode('utf8'))
    def _class(self, str):
        values = {"Actor": b'\x97\xCA\x62\x8B', "JD_SongDatabaseComponent": b'\x40\x55\x79\xFB', 
                  "JD_SongDescComponent": b'\xE0\x7F\xCC\x3F', "JD_SongDatabaseSceneConfig": b'\xF8\x78\xDC\x2D'}
        self.fs.write(values[str])
    def crc32(self, string):
        self.fs.write(getCrc(string).to_bytes(4, "big"))

class Deserializer():
    def __init__(self, fs):
        self.fs = fs
    def uint32(self):
        return int.from_bytes(self.fs.read(4), "big")
    def float(self):
        return struct.unpack('>f', self.fs.read(4))[0]
    def string(self):
        strLen = int.from_bytes(self.fs.read(4), "big")
        return self.fs.read(strLen).decode("utf-8")
    def _class(self):
        values = {b'\x97\xCA\x62\x8B': "Actor", b'\x40\x55\x79\xFB': "JD_SongDatabaseComponent", 
                  b'\xE0\x7F\xCC\x3F': "JD_SongDescComponent", b'\xF8\x78\xDC\x2D': "JD_SongDatabaseSceneConfig"}
        return values[self.fs.read(4)]

class XML():
    def __init__(self, ACTORS=[]):
        self.version = 1
        self.ENGINE_VERSION = 160366
        self.GRIDUNIT = 0
        self.DEPTH_SEPARATOR = 0
        self.viewFamily = 0
        self.ACTORS = ACTORS
        self.SceneConfig = SceneConfig()
        self.CoverflowSkuSongs = []
    def Serialize(self, fs):
        serial = Serializer(fs)
        serial.uint32(self.version)
        serial.uint32(self.ENGINE_VERSION)
        serial.uint32(self.GRIDUNIT)
        serial.uint32(self.DEPTH_SEPARATOR)
        serial.uint32(self.viewFamily)
        serial.uint32(len(self.ACTORS))
        for actor in self.ACTORS:
            actor.Serialize(fs)
        self.SceneConfig.Serialize(fs)
        serial.uint32(len(self.CoverflowSkuSongs))
        for cover in self.CoverflowSkuSongs:
            cover.Serialize(fs)
        serial.uint32(0)#unk
    def Deserialize(self, fs):
        deserial = Deserializer(fs)
        self.version = deserial.uint32()
        self.ENGINE_VERSION = deserial.uint32()
        self.GRIDUNIT = deserial.uint32()
        self.DEPTH_SEPARATOR = deserial.uint32()
        self.viewFamily = deserial.uint32()
        actorsLen = deserial.uint32()
        for x in range(actorsLen):
           actor = Actor(COMPONENTS=[])
           actor.Deserialize(fs)
           self.ACTORS.append(actor)
        self.SceneConfig.Deserialize(fs)
        coverSongsLen = deserial.uint32()
        for x in range(coverSongsLen):
            coverSong = CoverflowSong()
            coverSong.Deserialize(fs)
            self.CoverflowSkuSongs.append(coverSong)
        deserial.uint32()#unk

class Path():
    def __init__(self, path=""):
        self.PATH = path
        self.fileName = path.split("/")[-1]
        self.dir = path.replace(self.fileName, "")
    def Serialize(self, fs):
        serial = Serializer(fs)
        serial.string(self.fileName)
        serial.string(self.dir)
        serial.crc32(self.PATH)
    def Deserialize(self, fs): 
        deserial = Deserializer(fs)
        self.fileName = deserial.string()
        self.dir = deserial.string()
        self.PATH = self.dir + self.fileName
        deserial.uint32()#crc32
        

class Actor():
    def __init__(self, USERFRIENDLY="", PATH="", COMPONENTS=[]):
        self.NAME = "Actor"
        self.RELATIVEZ = 0.0
        self.SCALE_X = 1.0
        self.SCALE_Z = 1.0
        self.xFLIPPED = 0
        self.USERFRIENDLY = USERFRIENDLY
        self.MARKER = ""
        self.POS2D_X = 0.0
        self.POS2D_Z = 0.0
        self.ANGLE = 0.0
        self.INSTANCEDATAFILE = ""
        self.LUA = Path(PATH)
        self.COMPONENTS = COMPONENTS
    def Serialize(self, fs):
        serial = Serializer(fs)
        serial._class(self.NAME)
        serial.float(self.RELATIVEZ)
        serial.float(self.SCALE_X)
        serial.float(self.SCALE_Z)
        serial.uint32(self.xFLIPPED)
        serial.string(self.USERFRIENDLY)
        serial.string(self.MARKER)
        serial.float(self.POS2D_X)
        serial.float(self.POS2D_Z)
        serial.float(self.ANGLE)
        serial.string(self.INSTANCEDATAFILE)
        #path
        serial.uint32(4294967295)#unk?
        serial.uint32(0)#unk?
        self.LUA.Serialize(fs)
        serial.uint32(0)#unk?
        serial.uint32(0)#unk?
        #path
        serial.uint32(len(self.COMPONENTS))
        for component in self.COMPONENTS:
            serial._class(component)
    def Deserialize(self, fs):
        deserial = Deserializer(fs)
        self.NAME = deserial._class()
        self.RELATIVEZ = deserial.float()
        self.SCALE_X = deserial.float()
        self.SCALE_Z = deserial.float()
        self.xFLIPPED = deserial.uint32()
        self.USERFRIENDLY = deserial.string()
        self.MARKER = deserial.string()
        self.POS2D_X = deserial.float()
        self.POS2D_Z = deserial.float()
        self.ANGLE = deserial.float()
        self.INSTANCEDATAFILE = deserial.string()
        #path
        deserial.uint32()#unk
        deserial.uint32()#unk
        self.LUA = Path()
        self.LUA.Deserialize(fs)
        deserial.uint32()#unk
        deserial.uint32()#unk
        #path
        componentsLen = deserial.uint32()
        for x in range(componentsLen):
           self.COMPONENTS.append(deserial._class())

class SceneConfig():
    def __init__(self):
        self.UNK = 0
        self.activeSceneConfig = 0
        self.COMPONENTS = []
    def Serialize(self, fs):
        serial = Serializer(fs)
        serial.uint32(self.UNK)
        serial.uint32(self.activeSceneConfig)
        serial.uint32(len(self.COMPONENTS))
        for component in self.COMPONENTS:
            component.Serialize(fs)
    def Deserialize(self, fs):
        deserial = Deserializer(fs)
        self.UNK = deserial.uint32()
        self.activeSceneConfig = deserial.uint32()
        componentsLen = deserial.uint32()
        for x in range(componentsLen):
           comp = SceneConfigComponent()
           comp.Deserialize(fs)
           self.COMPONENTS.append(comp)

class SceneConfigComponent():
    def __init__(self):
        self.NAME = "JD_SongDatabaseSceneConfig"
        self.SKU = "X360_EMEA"
        self.Territory = "NCSA"
        self.RatingUI = Path("world/ui/screens/bootsequence/rating/rating_pegi_169.isc")
        self.ENUMS = []
    def Serialize(self, fs):
        serial = Serializer(fs)
        serial._class(self.NAME)
        serial.string(self.SKU)
        serial.string(self.Territory)
        self.RatingUI.Serialize(fs)
        serial.uint32(len(self.ENUMS))
    def Deserialize(self, fs):
        deserial = Deserializer(fs)
        self.NAME = deserial._class()
        self.SKU = deserial.string()
        self.Territory = deserial.string()
        self.RatingUI = Path()
        self.RatingUI.Deserialize(fs)
        deserial.uint32() #enum - no example from old gen games to take basis.

class CoverflowSong():
    def __init__(self):
        self.NAME = "MapName"
        self.COVER_PATH = Path("world/jd2015/mapname/menuart/actors/mapname_cover_generic.act")
        self.COMPONENTS = []
    def Serialize(self, fs):
        serial = Serializer(fs)
        serial.string(self.NAME)
        self.COVER_PATH.Serialize(fs)
        serial.uint32(0)#unk?
        serial.uint32(len(self.COMPONENTS))
        for component in self.COMPONENTS:
            serial.uint32(component)
    def Deserialize(self, fs):
        deserial = Deserializer(fs)
        self.NAME = deserial.string()
        self.COVER_PATH.Deserialize(fs)
        deserial.uint32()#unk
        componentsLen = deserial.uint32()
        for x in range(componentsLen):
            self.COMPONENTS.append(deserial.uint32())

with open("skuscene.og.ckd", "rb") as file:
    xmlFile = XML()
    xmlFile.Deserialize(file)
with open("skuscene.ckd", "wb") as file:
    xmlFile.Serialize(file)