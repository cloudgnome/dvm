from catalog.models import Category
from json import loads

f = open('categories.json','r')
data = loads(f.read())

def create_categories(data,parent = None):
	for item in data:
		parent = Category.objects.create(name=item.get('name'),type=item.get('type'),class_icon=item.get('class'))

		if parent:
			parent.parent = parent
			parent.save()

	if item.get('children'):
		create_categories(item.get('children'), parent)

if __name__ == '__main__':
	create_categories(data)