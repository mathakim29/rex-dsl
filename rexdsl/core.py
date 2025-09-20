from rply import LexerGenerator, ParserGenerator
import regex

class Rex:
    def __init__(self, block: str):
        self._build_lexer()
        self._build_parser()
        tokens = self.lexer.lex(block)
        self.pattern = self.parser.parse(tokens)

    def _build_lexer(self):
        rules = {
            "STRING":    r"'[^']*'",
            "NUMBER":    r"\d+",

            # keywords (case-insensitive)
            "OR":        r"(?i)or",
            "AND":       r"(?i)and",

            "SEMICOLON": r";",

            # NEW: portable flags syntax just before ';' → "/im", "/msx", etc.
            "SLASH":     r"/",
            "FLAGS":     r"(?i)[imsx]+",
        }

        lg = LexerGenerator()
        for name, pattern in rules.items():
            lg.add(name, pattern)

        lg.ignore(r"\s+")
        self.lexer = lg.build()

    def _build_parser(self):
        pg = ParserGenerator([
            "STRING", "NUMBER", "OR", "AND", "SEMICOLON",
            "SLASH", "FLAGS"
        ])

        # --- helpers ---
        def canon_flags(raw: str) -> str:
            s = raw.lower()
            s = "".join(ch for ch in s if ch in "imsx")
            return "".join(sorted(set(s)))

        def flags_prefix_from_token(tok) -> str:
            flags = canon_flags(tok.getstr())
            return f"(?{flags})" if flags else ""

        # --- start rules (flags optional) ---
        pg.production("start : sequences")(lambda p: (_ for _ in ()).throw(SyntaxError("Missing semicolon")))
        pg.production("start : sequences SLASH FLAGS SEMICOLON")(lambda p: f"{flags_prefix_from_token(p[2])}{p[0]}")
        pg.production("start : sequences SEMICOLON")(lambda p: p[0])

        # --- OR sequences ---
        pg.production("sequences : sequence OR sequences")(lambda p: f"(?:{p[0]})|(?:{p[2]})")
        pg.production("sequences : sequence")(lambda p: p[0])

        # --- AND sequences ---
        pg.production("sequence : statement AND sequence")(lambda p: f"{p[0]}{p[2]}")
        pg.production("sequence : statement")(lambda p: p[0])

        # --- unified statement handler ---
        def statement_core(p, x):
            tok_type = p[0].gettokentype()
            if tok_type == "STRING":
                text = p[0].getstr()[1:-1]
            else:
                raise ValueError(f"Unexpected token {tok_type}")

            count = int(p[1].getstr()) if x == 2 else 1
            return f"(?:{text}){{{count}}}"

        pg.production("statement : STRING NUMBER")(lambda p: statement_core(p, len(p)))
        pg.production("statement : STRING")(lambda p: statement_core(p, len(p)))

        self.parser = pg.build()

    def find(self, block: str) -> str | None:
        return regex.fullmatch(self.pattern, block)


    def exists(self, block: str) -> bool:
        return bool(self.find(block))
