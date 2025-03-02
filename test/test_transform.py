def handle_add_parse(args):
	if '+' in args.choose:
		#将choose中的所有合并一起
		result= [list(args.choose)]
	else:
		#每一项是否存在+
		result=[]
		for i in args.choose:
			if '+' in i:
				result.append([j for j in i.split('+') if j])
			else:
				result.append(i)
	return result


class A():
    choose=['11','1+2','2-5+']

print(handle_add_parse(A()))


