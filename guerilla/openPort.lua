local tmpdir = os.getenv("TMP")
if tmpdir == nil then
	tmpdir = os.getenv("TMPDIR")
end
local tmpfile = tmpdir.."//port"
local tmpfile = io.open(tmpfile, "r")
io.input(tmpfile)
local port = io.read()
commandport.close()
commandport.open(37499)
print("port opened")