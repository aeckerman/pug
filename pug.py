import click
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style

#Message workflows
def importantMessageG(obj, before, after):
	print(Style.BRIGHT + Fore.RED + before + str(obj.text) + after + Style.RESET_ALL + Fore.RESET)

def normalMessageG(obj, before, after):
	print(Fore.RED + before + str(obj.text) + after + Fore.RESET)

def importantMessageN(obj, before, after):
	print(Style.BRIGHT + Fore.YELLOW + before + str(obj.text) + after + Style.RESET_ALL + Fore.RESET)

def normalMessageN(obj, before, after):
	print(Fore.YELLOW + before + str(obj.text) + after + Fore.RESET)

#Command group init
@click.group()
def pug():
	pass

#Gem search command
@click.command()
@click.argument("package_name")
def gem(package_name):
	url = "http://rubygems.org/gems/%s" % (package_name)
	r = requests.get(url)
	soup = BeautifulSoup(r.content, "html.parser")

	package_title = soup.find("a", {"href": "/gems/%s" % (package_name)})
	package_description = soup.find("div", {"class": "gem__desc"})
	package_author = soup.find("li", {"class": "t-list__item"})
	package_version = soup.find("i", {"class": "page__subheading"})
	package_downloads = soup.find("span", {"class": "gem__downloads"})
	package_license = soup.find("span", {"class": "gem__ruby-version"})

	importantMessageG(package_title, "", "")
	importantMessageG(package_description, "", "")
	normalMessageG(package_author, "Author(s):", "")
	normalMessageG(package_version, "Version:\n", "")
	normalMessageG(package_downloads, "Downloads:\n", "")
	normalMessageG(package_license, "License:", "")

#NPM search command
@click.command()
@click.argument("package_name")
def npm(package_name):
	url = "https://www.npmjs.com/package/%s" % (package_name)
	r = requests.get(url)
	soup = BeautifulSoup(r.content, "html.parser")

	package_title = soup.find("a", {"href": "/package/%s" % (package_name)})
	package_description = soup.find("p", {"class": "package-description"})
	#NPM makes it kinda of hard to parse the author names so I just used the last publisher. 
	package_author = soup.find("li", {"class": "last-publisher"})
	package_author = package_author.span
	#Same with version
	package_version = soup.find("ul", {"class": "box"})
	package_version = package_version.strong
	package_downloads = soup.find("strong", {"class": "pretty-number monthly-downloads"})
	package_license = "MIT"

	importantMessageN(package_title, "", "\n")
	importantMessageN(package_description, "", "\n")
	normalMessageN(package_author, "Author(s):\n", "\n")
	normalMessageN(package_version, "Version:\n", "")
	normalMessageN(package_downloads, "Downloads(last month):\n" , "")
	print(Fore.YELLOW + "License:\n" + package_license + Fore.RESET)


#Adding commands to "pug" group
pug.add_command(gem)
pug.add_command(npm)

#Starting app
if __name__ == "__main__":
	pug()