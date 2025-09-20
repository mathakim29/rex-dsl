# rex-dsl – A DSL for Regex

**rex-dsl** is a lightweight domain-specific language (DSL) for building regular expressions with readable syntax.
Instead of cryptic regex, you describe patterns using **literals**, **counts**, and operators **`and`** / **`or`**.
Optionally, add **portable regex flags** (`/i`, `/m`, `/s`, `/x`) just before the semicolon.

The DSL compiles into valid regex patterns via [`rply`](https://pypi.org/project/rply/) and the [`regex`](https://pypi.org/project/regex/) module.

---

## 📑 Table of Contents

1. [Features](#-features)
2. [Installation](#-installation)
3. [Quick Start](#-quick-start)
4. [Language Specification](#-language-specification)

   * [BNF Grammar](#bnf-grammar)
   * [Cheatsheet](#cheatsheet)
5. [API Reference](#-api-reference)
6. [License](#-license)

---

## Features

* ✅ Readable DSL for regex construction
* ✅ Operators: `and` (concatenation), `or` (alternation)
* ✅ Quantifiers: `'a' 3` → `"aaa"`
* ✅ Portable regex flags: `/i` (ignore case), `/m` (multiline), `/s` (dotall), `/x` (free-spacing)
* ✅ Generates **non-capturing groups** `(?: … )`
* ✅ `.find()` to return match object or `None`
* ✅ `.exists()` for quick boolean checks
* ✅ Syntax enforcement: semicolon (`;`) required at end

---

## 📦 Installation

We recommend using [**uv**](https://github.com/astral-sh/uv) for Python environment management:

```bash
# Create & activate a virtual environment
uv add rex-dsl
```

Or with plain pip:

```bash
pip install rex-dsl
```

---

## Quick Start

```python
from rexdsl.rex import Rex

# Example DSL block: "two 'a's then 'bc', or literal 'xyz', case-insensitive"
block = "'a' 2 and 'bc' or 'xyz' /i;"

rex = Rex(block)

print("Generated regex:", rex.pattern)
# => (?i)(?:(?:a){2}(?:bc))|(?:(?:xyz))

print(rex.exists("aabc"))   # ✅ True
print(rex.exists("XYZ"))    # ✅ True
print(rex.exists("abc"))    # ❌ False
```

---

## Language Specification

### BNF Grammar

```
<start>       ::= <sequences> "/" <flags> ";"
                | <sequences> ";"

<flags>       ::= one-or-more of [i m s x]  ; case-insensitive

<sequences>   ::= <sequence> "or" <sequences>
                | <sequence>

<sequence>    ::= <statement> "and" <sequence>
                | <statement>

<statement>   ::= <string> <number>
                | <string>

<string>      ::= "'" <chars> "'"
<chars>       ::= (any non-quote character)*

<number>      ::= [0-9]+
```

---

### Cheatsheet

| DSL Snippet                | Meaning              | Generated Regex        | Example Match         |               |
| -------------------------- | -------------------- | ---------------------- | --------------------- | ------------- |
| `'a';`                     | literal `a`          | `(?:a)`                | `a`                   |               |
| `'abc';`                   | literal `abc`        | `(?:abc)`              | `abc`                 |               |
| `'a' 3;`                   | `a` repeated 3 times | `(?:a){3}`             | `aaa`                 |               |
| `'a' and 'b';`             | concatenation        | `(?:a)(?:b)`           | `ab`                  |               |
| `'hi' or 'bye';`           | alternation          | \`(?:(?\:hi))          | (?:(?\:bye))\`        | `hi`, `bye`   |
| `'a' 2 and 'bc' or 'xyz';` | precedence demo      | \`(?:(?\:a){2}(?\:bc)) | (?:(?\:xyz))\`        | `aabc`, `xyz` |
| `'hello' /i;`              | ignore case          | `(?i)(?:hello)`        | `HELLO`, `Hello`      |               |
| `'start' and 'end' /s;`    | dotall               | `(?s)(?:start)(?:end)` | works across newlines |               |
| `'x' /xixms;`              | flags dedupe+sort    | `(?imsx)(?:x)`         | `x`                   |               |

---

## API Reference

### `Rex(block: str)`

Compile a RexDSL block into a regex.

* **Parameters**
  `block: str` — DSL string ending with `;`

* **Attributes**
  `.pattern: str` — Generated regex pattern (inline flags if present)

---

### `Rex.find(text: str) -> str | None`

Return the full match string if `text` matches, else `None`.

```python
rex = Rex("'a' 3;")
print(rex.find("aaa"))   # "aaa"
print(rex.find("aa"))    # None
```

---

### `Rex.exists(text: str) -> bool`

Return `True` if `text` fully matches the pattern.

```python
rex = Rex("'a' and 'b';")
print(rex.exists("ab"))  # ✅ True
print(rex.exists("a"))   # ❌ False
```

---

## License
MIT — free to use, modify, and distribute.

---
