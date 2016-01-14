from datetime import datetime, timedelta

def long_op(time=5):
	end = datetime.now() + timedelta(seconds=time)
	while (datetime.now() < end):
		pass

