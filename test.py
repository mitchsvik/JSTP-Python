import jstp_python as api_jstp

test = "['Marcus Aurelius','AE127095',['1990-02-15','Rome'],['Ukraine','Kiev','03056','Pobedy','37','158','']]"
data = api_jstp.deserialize(test)
print(data)

test = "['Marcus Aurelius','AE127095',['1990-02-15','Rome'],['Ukraine','Kiev','03056','Pobedy',37,158]]"
data = api_jstp.deserialize(test)
print(data)

test = "['Marcus Aurelius','AE127095',['1990-02-15','Rome'],['Ukraine','Kiev','03056','Pobedy',-37,undefined],false,true]"
data = api_jstp.deserialize(test)
print(data)

test = "{'Marcus Aurelius', 'AE127095',['1990-02-15','Rome'],['Ukraine','Kiev','03056','Pobedy',-37,158]}"
data = api_jstp.parse(test)
print(data)
