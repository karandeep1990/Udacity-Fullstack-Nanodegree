#import user

def delegate_request(request):
	# parse request here

	if request.path == 'catalog.json':
		return ""