import re


def coerce(val):
    return min(max(int(val), 0), 255)


class Color:
    # Used to convert RGB colors to xterm-256 colors
    # I recommend minimizing this if your editor has such a functionality
    # If it doesn't, stop using a garbage editor and switch to Sublime
    _RGB_TO_TERM = {  # color look-up table
        # Primary 3-bit (8 colors). Unique representation!
        0x000000: 0,
        0x800000: 1,
        0x008000: 2,
        0x808000: 3,
        0x000080: 4,
        0x800080: 5,
        0x008080: 6,
        0xc0c0c0: 7,

        # Equivalent "bright" versions of original 8 colors.
        0x808080: 8,
        0xff0000: 9,
        0x00ff00: 10,
        0xffff00: 11,
        0x0000ff: 12,
        0xff00ff: 13,
        0x00ffff: 14,
        0xffffff: 15,

        # Strictly ascending.
        0x000000: 16,
        0x00005f: 17,
        0x000087: 18,
        0x0000af: 19,
        0x0000d7: 20,
        0x0000ff: 21,
        0x005f00: 22,
        0x005f5f: 23,
        0x005f87: 24,
        0x005faf: 25,
        0x005fd7: 26,
        0x005fff: 27,
        0x008700: 28,
        0x00875f: 29,
        0x008787: 30,
        0x0087af: 31,
        0x0087d7: 32,
        0x0087ff: 33,
        0x00af00: 34,
        0x00af5f: 35,
        0x00af87: 36,
        0x00afaf: 37,
        0x00afd7: 38,
        0x00afff: 39,
        0x00d700: 40,
        0x00d75f: 41,
        0x00d787: 42,
        0x00d7af: 43,
        0x00d7d7: 44,
        0x00d7ff: 45,
        0x00ff00: 46,
        0x00ff5f: 47,
        0x00ff87: 48,
        0x00ffaf: 49,
        0x00ffd7: 50,
        0x00ffff: 51,
        0x5f0000: 52,
        0x5f005f: 53,
        0x5f0087: 54,
        0x5f00af: 55,
        0x5f00d7: 56,
        0x5f00ff: 57,
        0x5f5f00: 58,
        0x5f5f5f: 59,
        0x5f5f87: 60,
        0x5f5faf: 61,
        0x5f5fd7: 62,
        0x5f5fff: 63,
        0x5f8700: 64,
        0x5f875f: 65,
        0x5f8787: 66,
        0x5f87af: 67,
        0x5f87d7: 68,
        0x5f87ff: 69,
        0x5faf00: 70,
        0x5faf5f: 71,
        0x5faf87: 72,
        0x5fafaf: 73,
        0x5fafd7: 74,
        0x5fafff: 75,
        0x5fd700: 76,
        0x5fd75f: 77,
        0x5fd787: 78,
        0x5fd7af: 79,
        0x5fd7d7: 80,
        0x5fd7ff: 81,
        0x5fff00: 82,
        0x5fff5f: 83,
        0x5fff87: 84,
        0x5fffaf: 85,
        0x5fffd7: 86,
        0x5fffff: 87,
        0x870000: 88,
        0x87005f: 89,
        0x870087: 90,
        0x8700af: 91,
        0x8700d7: 92,
        0x8700ff: 93,
        0x875f00: 94,
        0x875f5f: 95,
        0x875f87: 96,
        0x875faf: 97,
        0x875fd7: 98,
        0x875fff: 99,
        0x878700: 100,
        0x87875f: 101,
        0x878787: 102,
        0x8787af: 103,
        0x8787d7: 104,
        0x8787ff: 105,
        0x87af00: 106,
        0x87af5f: 107,
        0x87af87: 108,
        0x87afaf: 109,
        0x87afd7: 110,
        0x87afff: 111,
        0x87d700: 112,
        0x87d75f: 113,
        0x87d787: 114,
        0x87d7af: 115,
        0x87d7d7: 116,
        0x87d7ff: 117,
        0x87ff00: 118,
        0x87ff5f: 119,
        0x87ff87: 120,
        0x87ffaf: 121,
        0x87ffd7: 122,
        0x87ffff: 123,
        0xaf0000: 124,
        0xaf005f: 125,
        0xaf0087: 126,
        0xaf00af: 127,
        0xaf00d7: 128,
        0xaf00ff: 129,
        0xaf5f00: 130,
        0xaf5f5f: 131,
        0xaf5f87: 132,
        0xaf5faf: 133,
        0xaf5fd7: 134,
        0xaf5fff: 135,
        0xaf8700: 136,
        0xaf875f: 137,
        0xaf8787: 138,
        0xaf87af: 139,
        0xaf87d7: 140,
        0xaf87ff: 141,
        0xafaf00: 142,
        0xafaf5f: 143,
        0xafaf87: 144,
        0xafafaf: 145,
        0xafafd7: 146,
        0xafafff: 147,
        0xafd700: 148,
        0xafd75f: 149,
        0xafd787: 150,
        0xafd7af: 151,
        0xafd7d7: 152,
        0xafd7ff: 153,
        0xafff00: 154,
        0xafff5f: 155,
        0xafff87: 156,
        0xafffaf: 157,
        0xafffd7: 158,
        0xafffff: 159,
        0xd70000: 160,
        0xd7005f: 161,
        0xd70087: 162,
        0xd700af: 163,
        0xd700d7: 164,
        0xd700ff: 165,
        0xd75f00: 166,
        0xd75f5f: 167,
        0xd75f87: 168,
        0xd75faf: 169,
        0xd75fd7: 170,
        0xd75fff: 171,
        0xd78700: 172,
        0xd7875f: 173,
        0xd78787: 174,
        0xd787af: 175,
        0xd787d7: 176,
        0xd787ff: 177,
        0xd7af00: 178,
        0xd7af5f: 179,
        0xd7af87: 180,
        0xd7afaf: 181,
        0xd7afd7: 182,
        0xd7afff: 183,
        0xd7d700: 184,
        0xd7d75f: 185,
        0xd7d787: 186,
        0xd7d7af: 187,
        0xd7d7d7: 188,
        0xd7d7ff: 189,
        0xd7ff00: 190,
        0xd7ff5f: 191,
        0xd7ff87: 192,
        0xd7ffaf: 193,
        0xd7ffd7: 194,
        0xd7ffff: 195,
        0xff0000: 196,
        0xff005f: 197,
        0xff0087: 198,
        0xff00af: 199,
        0xff00d7: 200,
        0xff00ff: 201,
        0xff5f00: 202,
        0xff5f5f: 203,
        0xff5f87: 204,
        0xff5faf: 205,
        0xff5fd7: 206,
        0xff5fff: 207,
        0xff8700: 208,
        0xff875f: 209,
        0xff8787: 210,
        0xff87af: 211,
        0xff87d7: 212,
        0xff87ff: 213,
        0xffaf00: 214,
        0xffaf5f: 215,
        0xffaf87: 216,
        0xffafaf: 217,
        0xffafd7: 218,
        0xffafff: 219,
        0xffd700: 220,
        0xffd75f: 221,
        0xffd787: 222,
        0xffd7af: 223,
        0xffd7d7: 224,
        0xffd7ff: 225,
        0xffff00: 226,
        0xffff5f: 227,
        0xffff87: 228,
        0xffffaf: 229,
        0xffffd7: 230,
        0xffffff: 231,

        # Gray-scale range.
        0x080808: 232,
        0x121212: 233,
        0x1c1c1c: 234,
        0x262626: 235,
        0x303030: 236,
        0x3a3a3a: 237,
        0x444444: 238,
        0x4e4e4e: 239,
        0x585858: 240,
        0x626262: 241,
        0x6c6c6c: 242,
        0x767676: 243,
        0x808080: 244,
        0x8a8a8a: 245,
        0x949494: 246,
        0x9e9e9e: 247,
        0xa8a8a8: 248,
        0xb2b2b2: 249,
        0xbcbcbc: 250,
        0xc6c6c6: 251,
        0xd0d0d0: 252,
        0xdadada: 253,
        0xe4e4e4: 254,
        0xeeeeee: 255,
    }

    def __init__(self, red, green, blue):
        self._r = Color._check(red)
        self._g = Color._check(green)
        self._b = Color._check(blue)

    @staticmethod
    def _check(val):
        if not isinstance(val, int):
            raise TypeError(f"Value must be int, but was {type(val)}")
        if val < 0 or val > 255:
            raise ValueError(f"Value must be [0, 255], but was {val}")
        return val

    @classmethod
    def from_hexcode(cls, hex_val):
        return cls((hex_val >> 16) & 0xff, (hex_val >> 8) & 0xff, hex_val & 0xff)

    @classmethod
    def from_bytes(cls, b):
        return cls(*b[:3])  # Pass the first 3 bytes to the constructor

    @classmethod
    def unpack(cls, data):
        if isinstance(data, str):
            m = re.match(r'^(?:#|0x)?([A-Za-z0-9]{6})$', data)  # Parse hexcode format
            if m:
                return cls.from_hexcode(int(m.group(1), 16))
            # Match failed, fall through to error
        elif isinstance(data, int):
            return cls.from_hexcode(data)
        elif (isinstance(data, list) or isinstance(data, tuple)) and len(data) == 3:
            return cls(*data)  # Data is in a list, unpack the list into a color tuple
        raise ValueError(f"Invalid format for color data: {data!r}")

    @property
    def red(self):
        return self._r

    @property
    def green(self):
        return self._g

    @property
    def blue(self):
        return self._b

    def to_hexcode(self):
        return (self.red << 16) | (self.green << 8) | self.blue

    def to_hex_str(self):
        return f"0x{self.to_hexcode():06x}"

    def to_list(self):
        return [self.red, self.green, self.blue]

    def to_term_color(self):
        hexcode = self.to_hexcode()

        # Yes this is O(n) and yes this could be O(logn) but go fuck yourself
        closest_hex = min(Color._RGB_TO_TERM.keys(), key=lambda x: abs(x - hexcode))
        return Color._RGB_TO_TERM[closest_hex]

    def __bytes__(self):
        return bytes(self.to_list())

    def __str__(self):
        return f"({self.red}, {self.green}, {self.blue})"

    def __repr__(self):
        s = str(self)
        return f"<Color: {s}>"

    def __add__(self, other):
        if not isinstance(other, Color):
            raise TypeError("unsupported operand type(s) for +:"
                            f" '{type(self)}' and '{type(other)}'")
        r = coerce(self.red + other.red)
        g = coerce(self.green + other.green)
        b = coerce(self.blue + other.blue)
        return Color(r, g, b)

    def __sub__(self, other):
        if not isinstance(other, Color):
            raise TypeError("unsupported operand type(s) for -:"
                            f" '{type(self)}' and '{type(other)}'")
        r = coerce(self.red - other.red)
        g = coerce(self.green - other.green)
        b = coerce(self.blue - other.blue)
        return Color(r, g, b)

    def __mul__(self, coeff):
        if not isinstance(coeff, int) and not isinstance(coeff, float):
            raise TypeError("unsupported operand type(s) for *:"
                            f" '{type(self)}' and '{type(coeff)}'")
        r = coerce(self.red * coeff)
        g = coerce(self.green * coeff)
        b = coerce(self.blue * coeff)
        return Color(r, g, b)

    def blend(self, other, bias=0.5):
        """
        @brief      Blend this color with another one.

        @param      self   The object
        @param      other  The other color to blend with
        @param      bias   The bias to give towards this color in the blend [0, 1]

        @return     The blended color, as a new Color object
        """
        if bias < 0 or 1 < bias:
            raise ValueError(f"Bias must be in range [0, 1], but was {bias}")
        other_bias = 1.0 - bias

        def mix(this, other):
            return int(this * bias + other * other_bias)

        return Color(mix(self.red, other.red),
                     mix(self.green, other.green),
                     mix(self.blue, other.blue))

    def default(self):
        # Convert to JSON
        return [self.red, self.green, self.blue]


BLACK = Color(0, 0, 0)
RED = Color(255, 0, 0)
GREEN = Color(0, 255, 0)
BLUE = Color(0, 0, 255)
WHITE = Color(255, 255, 255)