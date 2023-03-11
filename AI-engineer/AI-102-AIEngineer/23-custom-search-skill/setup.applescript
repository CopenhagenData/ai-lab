set subscription_id to "3c47e9f2-fe51-42f5-b512-750b6160b545"
set resource_group to "test"
set location to "westeurope"

set unique_id to (random number from 10000 to 99999)

display dialog "Creating storage..."
do shell script "az storage account create --name ai102str" & unique_id & " --subscription " & subscription_id & " --resource-group " & resource_group & " --location " & location & " --sku Standard_LRS --encryption-services blob --default-action Allow --output none"

display dialog "Uploading files..."
set key_json to (do shell script "az storage account keys list --subscription " & subscription_id & " --resource-group " & resource_group & " --account-name ai102str" & unique_id & " --query \"[?keyName=='key1'].{keyName:keyName, permissions:permissions, value:value}\"")
set key_string to (key_json as string)
set AZURE_STORAGE_KEY to (key_string as string)
do shell script "az storage container create --account-name ai102str" & unique_id & " --name margies --public-access blob --auth-mode key --account-key " & AZURE_STORAGE_KEY & " --output none"
do shell script "az storage blob upload-batch -d margies -s data --account-name ai102str" & unique_id & " --auth-mode key --account-key " & AZURE_STORAGE_KEY & "  --output none"

display dialog "Creating cognitive services account..."
do shell script "az cognitiveservices account create --kind CognitiveServices --location " & location & " --name ai102cog" & unique_id & " --sku S0 --subscription " & subscription_id & " --resource-group " & resource_group & " --yes --output none"

display dialog "Creating search service..."
do shell script "az search service create --name ai102srch" & unique_id & " --subscription " & subscription_id & " --resource-group " & resource_group & " --location " & location & " --sku basic --output none"

display dialog "Storage account: ai102str" & unique_id
do shell script "az storage account show-connection-string --subscription " & subscription_id & " --resource-group " & resource_group & " --name ai102str" & unique_id
display dialog "Cognitive Services account: ai102cog" & unique_id
do shell script "az cognitiveservices account keys list --subscription " & subscription_id & " --resource-group " & resource_group & " --name ai102cog" & unique_id
display dialog "Search Service: ai102srch" & " Url: https://ai102srch" & unique_id & ".search.windows.net"
display dialog "Admin Keys:"
do shell script "az search admin-key show --subscription " & subscription_id & " --resource-group " & resource_group & " --service-name ai102srch" & unique_id
display dialog "Query Keys:"
do shell script "az search query-key list --subscription " & subscription_id & " --resource-group " & resource_group & " --service-name ai102srch!" & unique_id
