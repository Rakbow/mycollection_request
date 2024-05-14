class ItemDetail:
    def __init__(self):
        self.name: str = ''
        self.category: str = ''
        self.origins: list[Entry] = []
        self.classifications: list[Entry] = []
        self.characters: list[Entry] = []
        self.companies: list[Entry] = []
        self.artists: list[Entry] = []
        self.events: list[Entry] = []
        self.materials: list[Entry] = []
        self.releaseDetail: str = ''
        self.dimensions: str = ''
        self.images: list[ItemImage] = []


class Entry:
    def __init__(self, id: int, name: str, nameEn: str, role: str):
        self.id = id
        self.name = name
        self.nameEn = nameEn
        self.role = role


class ItemImage:
    def __init__(self, imgType: int, url: str):
        # 0-thumb 100-main
        # 1-figures 2-various 3-bootlegs 4-collections 5-official 6-spaces
        # 7-chan 8-loots&boxes 10-banners 11- kits&customs 12-items 14-exposition 19-customization
        self.imgType = imgType
        self.url = url
