from xbmcswift2 import Plugin
import urllib2
import re

def get_projects(status):
	downloader = urllib2.urlopen('http://www.ftfansub.net/s/progetti/%s/' % status)
	page = downloader.read()
	projects = re.findall('<div class="imageWrapper"><div class="cornerLink">([A-Za-z0-9 ]*)</div>',page)
	
	items = [{
        'label': project,
        'path': plugin.url_for('show_episodes_info', status=status, url=project.replace(" ", "-")),
    	} for project in projects]
	return items


def get_episodes(url):
	downloader = urllib2.urlopen(url)
	page = downloader.read()
	episodes = re.findall('<a class="fancybox" title="Guarda in streaming  - ([^"]*)" .*javascript:loadVideo\(\'(http://www.ftfansub.net/s/ftf-get-file[_test]*.php\?id=[0-9]*&project=[a-z0-9-]*)' , page) 
	
	items = [{
        'label': episode[0],
        'path': plugin.url_for('play_episode',  url = episode[1]),
	'is_playable': True,
    	} for episode in episodes]
	return items
	



plugin = Plugin()


@plugin.route('/')
def main_menu():
	items = [
	   {'label': 'In corso', 'path': plugin.url_for('show_incorso')},
	   {'label': 'Conclusi', 'path': plugin.url_for('show_conclusi')},
	]
 	return items

@plugin.route('/incorso/')
def show_incorso():
	items= get_projects('in-corso')
	return items


@plugin.route('/conclusi/')
def show_conclusi():
	return get_projects('conclusi')
	pass


@plugin.route('/episodes/<status>/<url>/')
def show_episodes_info(status, url):
	return get_episodes("http://www.ftfansub.net/s/progetti/%s/%s/" % (status, url))


@plugin.route('/episode/<url>/')
def play_episode(url):
	plugin.log.info('Playing url: %s' % url)
	plugin.set_resolved_url(url)

if __name__ == '__main__':
	plugin.run()
