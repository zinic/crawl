(function () {
    function KeyCodeConstants() {
        this.KEY_CANCEL = 3;
        this.KEY_HELP = 6;
        this.KEY_BACKSPACE = 8;
        this.KEY_TAB = 9;
        this.KEY_CLEAR = 12;
        this.KEY_ENTER = 13;
        this.KEY_ENTER_SPECIAL = 14;
        this.KEY_SHIFT = 16;
        this.KEY_CONTROL = 17;
        this.KEY_ALT = 18;
        this.KEY_PAUSE = 19;
        this.KEY_CAPS_LOCK = 20;
        this.KEY_KANA = 21;
        this.KEY_EISU = 22;
        this.KEY_JUNJA = 23;
        this.KEY_FINAL = 24;
        this.KEY_HANJA = 25;
        this.KEY_ESCAPE = 27;
        this.KEY_CONVERT = 28;
        this.KEY_NONCONVERT = 29;
        this.KEY_ACCEPT = 30;
        this.KEY_MODECHANGE = 31;
        this.KEY_SPACE = 32;
        this.KEY_PAGE_UP = 33;
        this.KEY_PAGE_DOWN = 34;
        this.KEY_END = 35;
        this.KEY_HOME = 36;
        this.KEY_LEFT = 37;
        this.KEY_UP = 38;
        this.KEY_RIGHT = 39;
        this.KEY_DOWN = 40;
        this.KEY_SELECT = 41;
        this.KEY_PRINT = 42;
        this.KEY_EXECUTE = 43;
        this.KEY_PRINTSCREEN = 44;
        this.KEY_INSERT = 45;
        this.KEY_DELETE = 46;
        this.KEY_NUM_0 = 48;
        this.KEY_NUM_1 = 49;
        this.KEY_NUM_2 = 50;
        this.KEY_NUM_3 = 51;
        this.KEY_NUM_4 = 52;
        this.KEY_NUM_5 = 53;
        this.KEY_NUM_6 = 54;
        this.KEY_NUM_7 = 55;
        this.KEY_NUM_8 = 56;
        this.KEY_NUM_9 = 57;
        this.KEY_COLON = 58;
        this.KEY_SEMICOLON = 59;
        this.KEY_LESS_THAN = 60;
        this.KEY_EQUALS = 61;
        this.KEY_GREATER_THAN = 62;
        this.KEY_QUESTION_MARK = 63;
        this.KEY_AT = 64;
        this.KEY_A = 65;
        this.KEY_B = 66;
        this.KEY_C = 67;
        this.KEY_D = 68;
        this.KEY_E = 69;
        this.KEY_F = 70;
        this.KEY_G = 71;
        this.KEY_H = 72;
        this.KEY_I = 73;
        this.KEY_J = 74;
        this.KEY_K = 75;
        this.KEY_L = 76;
        this.KEY_M = 77;
        this.KEY_N = 78;
        this.KEY_O = 79;
        this.KEY_P = 80;
        this.KEY_Q = 81;
        this.KEY_R = 82;
        this.KEY_S = 83;
        this.KEY_T = 84;
        this.KEY_U = 85;
        this.KEY_V = 86;
        this.KEY_W = 87;
        this.KEY_X = 88;
        this.KEY_Y = 89;
        this.KEY_Z = 90;
        this.KEY_WIN = 91;
        this.KEY_CONTEXT_MENU = 93;
        this.KEY_SLEEP = 95;
        this.KEY_NUMPAD0 = 96;
        this.KEY_NUMPAD1 = 97;
        this.KEY_NUMPAD2 = 98;
        this.KEY_NUMPAD3 = 99;
        this.KEY_NUMPAD4 = 100;
        this.KEY_NUMPAD5 = 101;
        this.KEY_NUMPAD6 = 102;
        this.KEY_NUMPAD7 = 103;
        this.KEY_NUMPAD8 = 104;
        this.KEY_NUMPAD9 = 105;
        this.KEY_MULTIPLY = 106;
        this.KEY_ADD = 107;
        this.KEY_SEPARATOR = 108;
        this.KEY_SUBTRACT = 109;
        this.KEY_DECIMAL = 110;
        this.KEY_DIVIDE = 111;
        this.KEY_F1 = 112;
        this.KEY_F2 = 113;
        this.KEY_F3 = 114;
        this.KEY_F4 = 115;
        this.KEY_F5 = 116;
        this.KEY_F6 = 117;
        this.KEY_F7 = 118;
        this.KEY_F8 = 119;
        this.KEY_F9 = 120;
        this.KEY_F10 = 121;
        this.KEY_F11 = 122;
        this.KEY_F12 = 123;
        this.KEY_F13 = 124;
        this.KEY_F14 = 125;
        this.KEY_F15 = 126;
        this.KEY_F16 = 127;
        this.KEY_F17 = 128;
        this.KEY_F18 = 129;
        this.KEY_F19 = 130;
        this.KEY_F20 = 131;
        this.KEY_F21 = 132;
        this.KEY_F22 = 133;
        this.KEY_F23 = 134;
        this.KEY_F24 = 135;
        this.KEY_NUM_LOCK = 144;
        this.KEY_SCROLL_LOCK = 145;
        this.KEY_WIN_OEM_FJ_JISHO = 146;
        this.KEY_WIN_OEM_FJ_MASSHOU = 147;
        this.KEY_WIN_OEM_FJ_TOUROKU = 148;
        this.KEY_WIN_OEM_FJ_LOYA = 149;
        this.KEY_WIN_OEM_FJ_ROYA = 150;
        this.KEY_CIRCUMFLEX = 160;
        this.KEY_EXCLAMATION = 161;
        this.KEY_DOUBLE_QUOTE = 162;
        this.KEY_HASH = 163;
        this.KEY_DOLLAR = 164;
        this.KEY_PERCENT = 165;
        this.KEY_AMPERSAND = 166;
        this.KEY_UNDERSCORE = 167;
        this.KEY_OPEN_PAREN = 168;
        this.KEY_CLOSE_PAREN = 169;
        this.KEY_ASTERISK = 170;
        this.KEY_PLUS = 171;
        this.KEY_PIPE = 172;
        this.KEY_HYPHEN_MINUS = 173;
        this.KEY_OPEN_CURLY_BRACKET = 174;
        this.KEY_CLOSE_CURLY_BRACKET = 175;
        this.KEY_TILDE = 176;
        this.KEY_VOLUME_MUTE = 181;
        this.KEY_VOLUME_DOWN = 182;
        this.KEY_VOLUME_UP = 183;
        this.KEY_COLON_SEMICOLON= 186;
        this.KEY_PLUS_EQUALS = 187;
        this.KEY_COMMA = 188;
        this.KEY_SUBTRACT_UNDERSCORE = 189;
        this.KEY_PERIOD = 190;
        this.KEY_SLASH = 191;
        this.KEY_BACK_QUOTE = 192;
        this.KEY_OPEN_BRACKET = 219;
        this.KEY_BACK_SLASH = 220;
        this.KEY_CLOSE_BRACKET = 221;
        this.KEY_QUOTE = 222;
        this.KEY_META = 224;
        this.KEY_ALTGR = 225;
        this.KEY_WIN_ICO_HELP = 227;
        this.KEY_WIN_ICO_00 = 228;
        this.KEY_WIN_ICO_CLEAR = 230;
        this.KEY_WIN_OEM_RESET = 233;
        this.KEY_WIN_OEM_JUMP = 234;
        this.KEY_WIN_OEM_PA1 = 235;
        this.KEY_WIN_OEM_PA2 = 236;
        this.KEY_WIN_OEM_PA3 = 237;
        this.KEY_WIN_OEM_WSCTRL = 238;
        this.KEY_WIN_OEM_CUSEL = 239;
        this.KEY_WIN_OEM_ATTN = 240;
        this.KEY_WIN_OEM_FINISH = 241;
        this.KEY_WIN_OEM_COPY = 242;
        this.KEY_WIN_OEM_AUTO = 243;
        this.KEY_WIN_OEM_ENLW = 244;
        this.KEY_WIN_OEM_BACKTAB = 245;
        this.KEY_ATTN = 246;
        this.KEY_CRSEL = 247;
        this.KEY_EXSEL = 248;
        this.KEY_EREOF = 249;
        this.KEY_PLAY = 250;
        this.KEY_ZOOM = 251;
        this.KEY_PA1 = 253;
        this.KEY_WIN_OEM_CLEAR = 254;
    }

    function KeyCodeTool(keycodes) {
        this.SPECIAL_KEYS = [
            keycodes.KEY_ALT,
            keycodes.KEY_SHIFT,
            keycodes.KEY_CONTROL,
            keycodes.KEY_WIN,
            keycodes.KEY_CAPS_LOCK,

            keycodes.KEY_UP,
            keycodes.KEY_DOWN,
            keycodes.KEY_LEFT,
            keycodes.KEY_RIGHT,
            keycodes.KEY_TAB,

            keycodes.KEY_BACKSPACE,
            keycodes.KEY_DELETE,
            keycodes.KEY_END,
            keycodes.KEY_HOME,
            keycodes.KEY_INSERT,
            keycodes.KEY_PAGE_UP,
            keycodes.KEY_PAGE_DOWN,

            keycodes.KEY_ENTER,
            keycodes.KEY_ESCAPE,

            keycodes.KEY_F1,
            keycodes.KEY_F2,
            keycodes.KEY_F3,
            keycodes.KEY_F4,
            keycodes.KEY_F5,
            keycodes.KEY_F6,
            keycodes.KEY_F7,
            keycodes.KEY_F8,
            keycodes.KEY_F9,
            keycodes.KEY_F10,
            keycodes.KEY_F11,
            keycodes.KEY_F12,
            keycodes.KEY_F13,
            keycodes.KEY_F14,
            keycodes.KEY_F15,
            keycodes.KEY_F16,
            keycodes.KEY_F17,
            keycodes.KEY_F18,
            keycodes.KEY_F19,
            keycodes.KEY_F21,
            keycodes.KEY_F22,
            keycodes.KEY_F23,
            keycodes.KEY_F24
        ];

        this.KEY_LOOKUP = [];

        var lookup_length = 0;
        for (var name in keycodes) {
            var keycode = keycodes[name];

            if (keycode > lookup_length) {
                lookup_length = keycode;
            }

            this.KEY_LOOKUP[keycode] = name;
        }

        this.KEY_REWRITE_LOOKUP = [];

        for (var i = 0; i < lookup_length; i++) {
            switch (i) {
                case keycodes.KEY_COMMA:
                    this.KEY_REWRITE_LOOKUP[i] = 44;
                    break;

                case keycodes.KEY_SUBTRACT:
                    this.KEY_REWRITE_LOOKUP[i] = 45;
                    break;

                case keycodes.KEY_PERIOD:
                    this.KEY_REWRITE_LOOKUP[i] = 46;
                    break;

                case keycodes.KEY_SLASH:
                    this.KEY_REWRITE_LOOKUP[i] = 47;
                    break;

                case keycodes.KEY_BACK_QUOTE:
                    this.KEY_REWRITE_LOOKUP[i] = 96;
                    break;

                case keycodes.KEY_BACK_SLASH:
                    this.KEY_REWRITE_LOOKUP[i] = 92;
                    break;

                case keycodes.KEY_QUOTE:
                    this.KEY_REWRITE_LOOKUP[i] = 39;
                    break;

                case keycodes.KEY_CLOSE_BRACKET:
                    this.KEY_REWRITE_LOOKUP[i] = 93;
                    break;

                case keycodes.KEY_OPEN_BRACKET:
                    this.KEY_REWRITE_LOOKUP[i] = 91;
                    break;

                case keycodes.KEY_HYPHEN_MINUS:
                    this.KEY_REWRITE_LOOKUP[i] = 45;
                    break;

                case keycodes.KEY_PLUS_EQUALS:
                    this.KEY_REWRITE_LOOKUP[i] = 61;
                    break;

                case keycodes.KEY_COLON_SEMICOLON:
                    this.KEY_REWRITE_LOOKUP[i] = 59;
                    break;

                case keycodes.KEY_SUBTRACT_UNDERSCORE:
                    this.KEY_REWRITE_LOOKUP[i] = 45;
                    break;

                default:
                    if (i >= keycodes.KEY_A && i <= keycodes.KEY_Z) {
                        this.KEY_REWRITE_LOOKUP[i] = i + 32;
                    } else {
                        this.KEY_REWRITE_LOOKUP[i] = i;
                    }
            }
        }

        this.SPECIAL_KEY_LOOKUP = [];

        for (var i = 0; i < lookup_length; i++) {
            this.SPECIAL_KEY_LOOKUP[i] = false;
        }

        for (var i in this.SPECIAL_KEYS) {
            var keycode = this.SPECIAL_KEYS[i];
            this.SPECIAL_KEY_LOOKUP[keycode] = true;
        }

        this.SHIFT_KEYS = [];

        for (var i = 0; i < lookup_length; i++) {
            switch (i) {
                case keycodes.KEY_NUM_1:
                    this.SHIFT_KEYS[i] = 33;
                    break;

                case keycodes.KEY_NUM_2:
                    this.SHIFT_KEYS[i] = 64;
                    break;

                case keycodes.KEY_NUM_3:
                    this.SHIFT_KEYS[i] = 35;
                    break;

                case keycodes.KEY_NUM_4:
                    this.SHIFT_KEYS[i] = 36;
                    break;

                case keycodes.KEY_NUM_5:
                    this.SHIFT_KEYS[i] = 37;
                    break;

                case keycodes.KEY_NUM_6:
                    this.SHIFT_KEYS[i] = 94;
                    break;

                case keycodes.KEY_NUM_7:
                    this.SHIFT_KEYS[i] = 38;
                    break;

                case keycodes.KEY_NUM_8:
                    this.SHIFT_KEYS[i] = 42;
                    break;

                case keycodes.KEY_NUM_9:
                    this.SHIFT_KEYS[i] = 40;
                    break;

                case keycodes.KEY_NUM_0:
                    this.SHIFT_KEYS[i] = 41;
                    break;

                case keycodes.KEY_BACK_QUOTE:
                    this.SHIFT_KEYS[i] = 126;
                    break;

                case keycodes.KEY_OPEN_BRACKET:
                    this.SHIFT_KEYS[i] = 123;
                    break;

                case keycodes.KEY_CLOSE_BRACKET:
                    this.SHIFT_KEYS[i] = 124;
                    break;

                case keycodes.KEY_BACK_SLASH:
                    this.SHIFT_KEYS[i] = 124;
                    break;

                case keycodes.KEY_SEMICOLON:
                    this.SHIFT_KEYS[i] = 58;
                    break;

                case keycodes.KEY_QUOTE:
                    this.SHIFT_KEYS[i] = 34;
                    break;

                case keycodes.KEY_COMMA:
                    this.SHIFT_KEYS[i] = 60;
                    break;

                case keycodes.KEY_PERIOD:
                    this.SHIFT_KEYS[i] = 62;
                    break;

                case keycodes.KEY_SLASH:
                    this.SHIFT_KEYS[i] = 63;
                    break;

                case keycodes.KEY_HYPHEN_MINUS:
                    this.SHIFT_KEYS[i] = 95;
                    break;

                case keycodes.KEY_EQUALS:
                    this.SHIFT_KEYS[i] = 43;
                    break;

                default:
                    if (i >= keycodes.KEY_A + 32 && i <= keycodes.KEY_Z + 32) {
                        this.SHIFT_KEYS[i] = i - 32;
                    } else {
                        this.SHIFT_KEYS[i] = i;
                    }
            }
        }

        this.keycode_name = function (keycode) {
            return this.KEY_LOOKUP[keycode];
        };

        this.is_special_key = function (keycode) {
            return this.SPECIAL_KEY_LOOKUP[keycode];
        };

        this.lookup_char = function (keycode) {
            return this.KEY_REWRITE_LOOKUP[keycode];
        };

        this.shift = function (keycode) {
            return this.SHIFT_KEYS[keycode];
        };
    }

    var keycodes = new KeyCodeConstants();

    // Set global scope
    window.gcm_keys = {
        codes: keycodes,
        tool: new KeyCodeTool(keycodes)
    };
})();
