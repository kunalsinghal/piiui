def tag(s):
	s = s.replace(',', ' , ').replace('.', ' . ')
	lis = s.split()
	ret = ""
	cnt = 1
	for x in lis:
		ret += '<span onclick="pop(' + str(cnt) + ')" id="' + str(cnt) + '" class="words">' + x + '</span> '
		cnt += 1

	return ret

def getTweet(): 
	s = "@JohnDoe, this is not a random tweet. #chill #fight"
	return tag(s)