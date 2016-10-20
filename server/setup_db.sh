#!/bin/bash

read -r -d '' VIEW_JSON <<'EOF'
{
    "_id": "_design/ced",
    "language": "javascript",
    "views": {
	"character-name": {
            "map": "function (doc) {\n  if (doc.type === 'character') {\n    emit(doc.name, doc);\n  }\n}"
        }
    }
}
EOF

curl -s -X PUT -u "${USER_INFO}" 'http://localhost:5984/ced' | python -m json.tool
curl -s -X PUT -u "${USER_INFO}" 'http://localhost:5984/ced/_design/ced' -d "${VIEW_JSON}" | python -m json.tool
