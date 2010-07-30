#from __future__ import unicode_literals
import sys
sys.path.append("c:\python27\Lib")

import itertools
import os
import NHunspell
import re

path = u'C:\\Users\\octavio.rdz\\Documents\\SharpDevelop Projects\\typos\data'
aff_file = os.path.join(path, u'es_MX.aff')
dic_file = os.path.join(path, u'es_MX.dic')
speller = NHunspell.Hunspell(aff_file, dic_file)


def check_spelling(text):	
	words = text.split(u' ')
	for word in words:				
		if not speller.Spell(word):			
			list = speller.Suggest(word)
			yield word, list
	
	
def get_text(markup):		
	search_expressions = [u'Text="([\w+\s?]+?)"', u'HeaderText="([\w+\s?]+?)"',
							u'Description="([\w+\s?]+?)"', u'Title="([\w+\s?]+?)"'
							u'GroupingText="([\w+\s?]+?)"']
	matches = re.finditer(u'|'.join(search_expressions),
			markup, re.MULTILINE | re.LOCALE)
			
	for match in matches:
		groups = match.groups()
		if groups:    		    		
			yield u' '.join([group for group in groups if group])
	   
	   
def process_file(path):
	with open(path) as file:
		for line in file:
			for text in get_text(line):		
				header_msg = str.format(u'\nTypos in {0}', cwf)
				for word, suggestions in check_spelling(text):
					if header_msg:
						print(header_msg)
						header_msg = None					
					msg = str.format(u'Word: {0} Suggestions: {1}', word, u' '.join(suggestions))
					print(msg)
	

def is_valid_type(file):
	exts = [u'.aspx', u'.ascx']
	ext = os.path.splitext(file)[1]
	return ext in exts
		

work_path = u'C:\\Projects\\niki\\source\\WebSite'
#work_path = u'C:\\Projects\\CoachTool\\source\\WebSite'
#work_path = u'C:\\Projects\\Revenu\\source\\WebSite'
#work_path = u'C:\\Projects\\Revenu\\source\\PublicSite'
#work_path = u'C:\\Projects\\Bisimplex\\Colibri\\src\\Websites\\Colibri'
for dir, dirs, files in os.walk(work_path):
	cwd = os.path.join(work_path, dir)	
	for file in files:
		if is_valid_type(file):			
			cwf = os.path.join(cwd, file)			
			process_file(cwf)
			
print("========= Completed =========")
raw_input()