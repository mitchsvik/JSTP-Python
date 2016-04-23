import jstp_python as api_jstp

test = "['Marcus Aurelius','AE127095',['1990-02-15','Rome'],['Ukraine','Kiev','03056','Pobedy','37','158']]"
out = api_jstp.deserialize(test)
data = out[0]
print(data)

test = "['Marcus Aurelius','AE127095',['1990-02-15','Rome'],['Ukraine','Kiev','03056','Pobedy',37,158]]"
out = api_jstp.deserialize(test)
data = out[0]
print(data)
