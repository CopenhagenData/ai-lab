set cstesturl to "https://cstest.search.windows.net"
set admin_key to "4GgojulLs4YSw8M85MfUXLUFzCiWq3G3zvs7jLF026AzSeCBnnCt"

display dialog "Updating the skillset..."
do shell script "curl -X PUT " & cstesturl & "/skillsets/margies-skillset?api-version=2020-06-30 -H 'Content-Type: application/json' -H 'api-key: " & admin_key & "' -d @skillset.json"
-- curl -X PUT 'https://cstest.search.windows.net/skillsets/margies-skillset?api-version=2020-06-30' -H 'Content-Type: application/json' -H 'api-key: 4GgojulLs4YSw8M85MfUXLUFzCiWq3G3zvs7jLF026AzSeCBnnCt' -d @skillset.json

display dialog "Updating the index..."
do shell script "curl -X PUT " & cstesturl & "/indexes/margies-index?api-version=2020-06-30 -H 'Content-Type: application/json' -H 'api-key: " & admin_key & "' -d @index.json"
-- curl -X PUT 'https://cstest.search.windows.net/indexes/margies-index?api-version=2020-06-30' -H 'Content-Type: application/json' -H 'api-key: 4GgojulLs4YSw8M85MfUXLUFzCiWq3G3zvs7jLF026AzSeCBnnCt' -d @index.json

display dialog "Updating the indexer..."
do shell script "curl -X PUT " & cstesturl & "/indexers/margies-indexer?api-version=2020-06-30 -H 'Content-Type: application/json' -H 'api-key: " & admin_key & "' -d @indexer.json"
-- curl -X PUT 'https://cstest.search.windows.net/indexers/margies-indexer?api-version=2020-06-30' -H 'Content-Type: application/json' -H 'api-key: 4GgojulLs4YSw8M85MfUXLUFzCiWq3G3zvs7jLF026AzSeCBnnCt' -d @indexer.json

display dialog "Resetting the indexer"
do shell script "curl -X POST " & cstesturl & "/indexers/margies-indexer/reset?api-version=2020-06-30 -H 'Content-Type: application/json' -H 'Content-Length: 0' -H 'api-key: " & admin_key & "'"
-- curl -X POST 'https://cstest.search.windows.net/indexers/margies-indexer/reset?api-version=2020-06-30' -H 'Content-Type: application/json' -H 'Content-Length: 0' -H 'api-key: " 4GgojulLs4YSw8M85MfUXLUFzCiWq3G3zvs7jLF026AzSeCBnnCt'

display dialog "Rerunning the indexer"
do shell script "curl -X POST " & cstesturl & "/indexers/margies-indexer/run?api-version=2020-06-30 -H 'Content-Type: application/json' -H 'Content-Length: 0' -H 'api-key: " & admin_key & "'"
-- curl -X POST 'https://cstest.search.windows.net/indexers/margies-indexer/run?api-version=2020-06-30' -H 'Content-Type: application/json' -H 'Content-Length: 0' -H 'api-key: 4GgojulLs4YSw8M85MfUXLUFzCiWq3G3zvs7jLF026AzSeCBnnCt'