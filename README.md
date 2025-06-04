# Unicode Tools

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Unicode](https://img.shields.io/badge/Unicode-15.0-green.svg)](https://unicode.org/)

A powerful command-line tool for searching and exploring Unicode characters, emoji sequences, and character properties.

## 🚀 Features

- **Search by name**: Find characters by their Unicode name
- **Search by code**: Look up characters by code point or range
- **Search by character**: Reverse lookup from character to details
- **Search by block**: Explore characters within Unicode blocks
- **Emoji support**: Full support for emoji sequences and ZWJ sequences
- **CJK details**: Enhanced descriptions for CJK characters using kDefinition
- **Flexible output**: Multiple output formats for different use cases

## 📖 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
- [Command Reference](#command-reference)
- [Database Management](#database-management)
- [Contributing](#contributing)
- [License](#license)

## 🛠 Installation

### Install from source

```bash
git clone https://github.com/mkyutani/unicode-tools.git
cd unicode-tools
pip install -e .
```

### Initialize database

Create the Unicode database (required for first use):

```bash
uccreatedatabase
```

This downloads Unicode 15.0 data and creates a local SQLite database (~13MB) at:
- Linux/macOS: `~/.local/share/unicode-tools/unicode.db`
- Root users: Automatically chooses between system (`/var/lib/unicode-tools/`) or personal location

## ⚡ Quick Start

```bash
# Search for ghost-related characters
ucsearch ghost

# Find characters in a code range
ucsearch -c 1F47A-1F480

# Search by character
ucsearch -x 👻

# Search within a Unicode block
ucsearch -b "Emoticons"
```

## 📋 Usage Examples

### Search by Name

```bash
ucsearch goblin
```
```
👺 1F47A JAPANESE GOBLIN
```

### Search by Code Range

```bash
ucsearch -c 1F479-1F47B
```
```
👹 1F479 JAPANESE OGRE
👺 1F47A JAPANESE GOBLIN
👻 1F47B GHOST
```

### Search by Character

```bash
ucsearch -x 👻
```
```
👻 1F47B GHOST
```

### Search by Unicode Block

```bash
ucsearch -b "Misc_Pictographs"
```

### Search with Details (CJK Characters)

```bash
ucsearch -d "pray for happiness"
```
```
祝 795D CJK UNIFIED IDEOGRAPH-#; PRAY FOR HAPPINESS OR BLESSINGS
```

### Output Formatting

```bash
# Simple format (characters only)
ucsearch ghost -f simple
👻

# UTF-8 format
ucsearch ghost -f utf8
👻 F0 9F 91 BB GHOST

# Custom delimiter
ucsearch ghost -D "|"
👻|1F47B|GHOST
```

## 🔧 Command Reference

### ucsearch

| Option | Short | Description |
|--------|-------|-------------|
| `--name` | | Search by character name (default) |
| `--code` | `-c` | Search by code point or range |
| `--char` | `-x` | Search by character |
| `--block` | `-b` | Search by Unicode block |
| `--detail` | `-d` | Search in character details |
| `--strict` | `-s` | Exact match (case insensitive) |
| `--first` | `-1` | Show first result only |
| `--format` | `-f` | Output format: `utf8`, `simple` |
| `--delimiter` | `-D` | Custom delimiter (default: space) |

### Database Management

| Command | Description |
|---------|-------------|
| `uccreatedatabase` | Create/update Unicode database |
| `ucdeletedatabase` | Remove Unicode database |
| `ucdatabaseinfo` | Show database location |

## 💾 Database Management

### Create Database
```bash
uccreatedatabase
```

### Check Database Location
```bash
ucdatabaseinfo
```

### Remove Database
```bash
ucdeletedatabase
```

### Environment Variables

- `UNICODE_DB_PATH`: Override default database location

```bash
export UNICODE_DB_PATH="/custom/path/unicode.db"
uccreatedatabase
```

## 🌟 Advanced Examples

### Finding Emoji Sequences

```bash
# National flags
ucsearch -b "RGI_Emoji_Flag_Sequence"

# Family emoji with ZWJ sequences
ucsearch family
```

### Terminal Display vs. Browser/Application Support

Many terminals don't properly display complex emoji sequences, but the characters work correctly when copied to browsers or applications.

#### National Flag Example

When searching for flags, you might see separate letters in your terminal:

```bash
ucsearch -b "RGI_Emoji_Flag_Sequence" | grep -i norway
```
```
🇳🇴 1F1F3 1F1F4 flag: Norway
```

![Sample to copy Norway's flag in twitter](img/ucsearch-block-flag-norway.png)

Even though you see two separate letters (🇳🇴) in the terminal, when you copy and paste them into a browser or application like Twitter, they combine to display the Norwegian flag 🇳🇴.

![Sample to paste Norway's flag in twitter](img/twitter-norway.png)

#### ZWJ Sequence Example

The same applies to Zero Width Joiner (ZWJ) sequences. Complex emoji like family groups or professional emoji might not render correctly in terminals:

```bash
ucsearch "polar bear"
```

In a terminal without proper font support:

![Sample to copy polar bear in twitter](img/ucsearch-polarbear.png)

But when pasted in Twitter or other applications:

![Sample to paste polar bear in twitter](img/twitter-polarbear.png)

> **💡 Tip**: This is expected behavior. The Unicode data is correct, and the characters will work properly in applications that support modern emoji rendering.

### Pipe Operations

```bash
# Get just the character
ucsearch ghost -f simple

# First match only
ucsearch snow -1

# Custom format for scripting
ucsearch ghost -D "," | cut -d',' -f1
```

### Complex Searches

```bash
# CJK characters with specific meanings
ucsearch -d "dragon"

# Characters in multiple blocks
ucsearch -b "Mathematical" | head -10
```

## 🏗 Data Sources

This tool uses official Unicode 15.0 data:

- [Unicode Character Database](https://www.unicode.org/Public/15.0.0/ucdxml/ucd.all.flat.zip)
- [Emoji Sequences](https://www.unicode.org/Public/emoji/15.0/emoji-sequences.txt)
- [Emoji ZWJ Sequences](https://www.unicode.org/Public/emoji/15.0/emoji-zwj-sequences.txt)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Unicode Consortium](https://unicode.org/) for maintaining Unicode standards
- Contributors and users of this project
