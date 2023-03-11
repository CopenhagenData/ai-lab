set subscription_id to "3c47e9f2-fe51-42f5-b512-750b6160b545"
set azure_storage_account to "spnlstest"
set azure_storage_key to "gpzXAjfP0ua+qdUZqFyEtfE5npxRWXdjCGggqEuYUXhyHjJTP3dT3NNUykFEpNTKVxs53iwaLlBU+AStVAbHxA=="

display dialog "Creating container..."
do shell script "az storage container create --account-name " & azure_storage_account & " --subscription " & subscription_id & " --name margies --public-access blob --auth-mode key --account-key " & azure_storage_key & " --output none"

display dialog "Uploading files..."
do shell script "az storage blob upload-batch -d margies -s data --account-name " & azure_storage_account & " --auth-mode key --account-key " & azure_storage_key & "  --output none"
