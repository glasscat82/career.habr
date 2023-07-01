from datetime import datetime
from prettytable import PrettyTable
from career import career

def main():
	start = datetime.now()	
	
	# ----- 25
	links = career()
	html_ = links.get_html()
	links_ = links.get_all_links(html=html_)
	
    # the table
	x = PrettyTable()
	x.field_names = ["№", "Имя", "Ссылка", "Цена"]
	x.align["Имя"] = x.align["Ссылка"] = x.align["Цена"] = "l"

	for index, r_ in enumerate(links_, 1):
		x.add_row([index, r_['title'], r_['slug'], r_['prise']['prise_1']])

	print(x.get_string(title='25 expert for career.habr.com/experts'))
	# ----- end 25
 
	# links.p(links_)
	links.write_json(data=links_, path='./json/career.json')

	end = datetime.now()
	print(str(end-start))


if __name__ == '__main__':
	main()