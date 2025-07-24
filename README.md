# 🔍 Sybase Stored Procedure Indexer

A Python-based static analysis tool to **extract and index metadata from Sybase T-SQL stored procedures** using ANTLR. This tool helps developers understand procedural dependencies, parameter structures, and table usage from a SQL dump file.

---

## 📦 Folder Structure

```
.
├── proc_indexer.py              # Main logic for parsing and metadata extraction
├── test.sql                     # SQL file containing Sybase stored procedures (input)
├── index.json                   # Output metadata (procedure name, params, calls, tables)
├── TSqlLexer.g4 / .tokens       # ANTLR grammar for T-SQL lexer
├── TSqlParser.g4 / .tokens      # ANTLR grammar for T-SQL parser
├── TSqlLexer.py / .interp       # Generated lexer files
├── TSqlParser.py / .interp      # Generated parser files
├── TSqlParserListener.py        # Custom listener to walk the parse tree
├── tests.py                     # Placeholder for unit tests
├── utils.py                     # Utility functions (future support)
├── .gitignore

```

---

## ⚙️ Setup Instructions

### Prerequisites

- Python 3.7 or above
- Java (for ANTLR tool usage)
- ANTLR 4 (Python runtime)
- A terminal that supports PowerShell or Unix-style commands

---

### 1️⃣ Clone the Repository

```bash
git clone <your-repo-url>
cd <your-repo-name>
```

### 2️⃣ Install Dependencies

```bash
pip install antlr4-python3-runtime
```

---

### 3️⃣ Generate ANTLR Lexer and Parser (Only if `.g4` files are modified)

Make sure ANTLR jar is in your system path, then:

```bash
antlr4 -Dlanguage=Python3 TSqlLexer.g4
antlr4 -Dlanguage=Python3 TSqlParser.g4
```

This will generate:
- `TSqlLexer.py`
- `TSqlParser.py`
- `TSqlParserListener.py`
- `.tokens` and `.interp` files

---

### 4️⃣ Add Your Procedures

Add your stored procedures in `test.sql`. This file acts as the SQL dump input source.

---

### 5️⃣ Run the Indexer

```bash
python proc_indexer.py
```

After execution, you'll get a structured output like this:

```json
{
  "sp_get_customer": {
    "params": ["@cust_id INT"],
    "calls": ["sp_get_address"],
    "tables": ["customer", "address"]
  }
}
```

The result will be saved in `index.json`.

---

## 🛑 Known Limitations

- **Dynamic Execution Not Fully Supported**:
  ```sql
  EXEC (@dynamic_proc_name);
  ```
  Dynamic procedure calls like the above cannot be resolved at static analysis time and are therefore skipped or excluded from `calls`.

- **Complex JOIN Aliasing**: Some deep joins or nested subqueries may not be fully captured in the current table extraction logic.

- **Param Formatting**: Parameter output assumes a single-line declaration. Complex multi-line or constraint-based definitions may require fine-tuning.

---

## 🛠️ Future Improvements

- Handle dynamic EXEC resolution using inference or trace logs.
- Parse sub-procedures or functions within nested BEGIN...END blocks.
- Add support for table-valued parameters and output parameters.
- CLI and GUI support for interactive usage.

---

## 💬 Contact

If you have suggestions, issues, or improvements — feel free to open an issue or contact the developer directly:

📧 **adarshnaik1**

---

## 🪪 License

This project is licensed under the **MIT License** — use it freely, modify it boldly, and contribute it proudly!
