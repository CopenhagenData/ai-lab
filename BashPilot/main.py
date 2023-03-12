from util.request_manager import request_manager

rm = request_manager()
last_request = ""

while True:
  print('Waiting for input...')
  request = input()
  if request == "exit":
    break
  elif request == "code":
    print(last_request)
    continue

  rm.request = request
  rm.request_type = 'code'
  response = rm.query()
  print("\nYour request is being processed...\n")
  rm.exec_code(response)
  last_request = response

print("Finished...")
