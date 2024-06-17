import mcon
import time

pretend_result = "4516E562C105713E, Ikea, 72 ms, team 0\n"#4516E562CZ05713E, Ga, 72 ms, team 0\n"

test = mcon.quirks.mordhau.PlayerlistCommand()
test.complete(pretend_result)

print(test.result)