# Meta parameters
META_COLUMNS_MATCH_SET = {
    "notes": {
        "content": "Expect the columns to match an unordered set: {}",
        "format": "markdown"
    }
}

META_COLUMN_NOT_NULL = {
    "notes": {
        "content": "Expect {} column values to not be null",
        "format": "markdown"
    }
}

META_COMPOUND_UNIQUE = {
    "notes": {
        "content": "Expect compound columns {} to be unique",
        "format": "markdown"
    }
}

# Kwargs parameter
KWARGS_COlUMNS_MATCH_SET = {
    "column_set": {}
}

KWARGS_COLUMN_NOT_NULL = {
    "column": "{}",
    "mostly": 1.0
}

KWARGS_COMPOUND_UNIQUE = {
    "column_list": {},
    "ignore_row_if": "never"
}
